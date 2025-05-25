from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, Response
from fastapi.responses import JSONResponse
import logging
import redis.asyncio as redis
from typing import List, Optional

logger = logging.getLogger(__name__)

class IPMiddleware(BaseHTTPMiddleware):
    """
    IP白名单和黑名单中间件
    支持静态黑名单和动态自动黑名单
    """
    def __init__(self, 
                 app, 
                 whitelist: List[str] = None, 
                 blacklist: List[str] = None,
                 redis_url: Optional[str] = None,
                 redis_password: Optional[str] = None,
                 check_auto_blacklist: bool = True):
        super().__init__(app)
        self.whitelist = whitelist or []
        self.blacklist = blacklist or []
        self.redis_url = redis_url
        self.redis_password = redis_password
        self.check_auto_blacklist = check_auto_blacklist
        self.redis_pool = None
        logger.info(f"IP中间件已初始化，白名单: {self.whitelist}, 黑名单: {self.blacklist}, 检查自动黑名单: {check_auto_blacklist}")
        
    async def init_redis_pool(self):
        """
        初始化Redis连接池
        """
        if self.redis_url and self.redis_pool is None:
            try:
                self.redis_pool = await redis.from_url(self.redis_url, encoding="utf-8", decode_responses=True, password=self.redis_password)
                logger.info("IP中间件Redis连接池已初始化")
                # 测试连接
                await self.redis_pool.ping()
                logger.info("Redis连接测试成功")
            except Exception as e:
                logger.error(f"Redis连接初始化失败: {str(e)}")
                # 重新尝试不使用URL中的密码，而是单独提供密码参数
                try:
                    # 从URL中移除可能的密码部分
                    clean_url = self.redis_url
                    if '@' in clean_url:
                        # 移除URL中可能存在的密码部分
                        protocol_part, rest = clean_url.split('://', 1)
                        if '@' in rest:
                            auth_part, host_part = rest.split('@', 1)
                            clean_url = f"{protocol_part}://{host_part}"
                    
                    logger.info(f"尝试使用清理后的URL连接Redis: {clean_url}")
                    self.redis_pool = await redis.from_url(clean_url, encoding="utf-8", decode_responses=True, password=self.redis_password)
                    logger.info("Redis连接池已初始化（使用单独的密码参数）")
                except Exception as e2:
                    logger.error(f"Redis连接初始化第二次尝试失败: {str(e2)}")
                    # 设置为None以便下次请求重试
                    self.redis_pool = None

    async def is_in_auto_blacklist(self, ip: str) -> bool:
        """
        检查IP是否在自动黑名单中
        """
        if not self.check_auto_blacklist or not self.redis_pool:
            return False
            
        try:
            # 检查Redis中的自动黑名单
            key = f"auto_blacklist:{ip}"
            exists = await self.redis_pool.exists(key)
            return bool(exists)
        except Exception as e:
            logger.error(f"检查自动黑名单失败: {str(e)}")
            return False
    
    async def dispatch(self, request: Request, call_next):
        # 初始化Redis连接池（如果尚未初始化）
        if self.redis_url and self.redis_pool is None:
            await self.init_redis_pool()
            
        # 获取客户端IP
        client_ip = self._get_client_ip(request)
        
        # 检查白名单
        if self.whitelist and client_ip in self.whitelist:
            return await call_next(request)
        
        # 检查静态黑名单
        if client_ip in self.blacklist:
            logger.warning(f"拒绝来自静态黑名单IP的请求: {client_ip}")
            return JSONResponse(
                status_code=403,
                content={"detail": "您的IP已被禁止访问此服务"}
            )
        
        # 检查自动黑名单
        if self.check_auto_blacklist and await self.is_in_auto_blacklist(client_ip):
            logger.warning(f"拒绝来自自动黑名单IP的请求: {client_ip}")
            return JSONResponse(
                status_code=403,
                content={"detail": "您的IP已被临时禁止访问此服务，请稍后再试"}
            )
        
        # 允许请求通过
        return await call_next(request)
    
    def _get_client_ip(self, request: Request) -> str:
        """
        获取客户端真实IP地址
        """
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            # 获取最原始的IP（最左侧的）
            return forwarded.split(",")[0]
        return request.client.host