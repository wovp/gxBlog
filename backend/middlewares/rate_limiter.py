from ctypes import Array
import time
from typing import Optional, Callable, Dict, Any

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import redis.asyncio as redis
import logging
import os
logger = logging.getLogger(__name__)
if os.getenv("DEBUG_MODE") == "false":
    logger.setLevel(logging.WARNING)


class RateLimiter(BaseHTTPMiddleware):
    """
    基于Redis的速率限制中间件，使用令牌桶算法
    支持自动将频繁触发限流的IP加入黑名单
    """
    def __init__(self, 
                 app, 
                 redis_url: str, 
                 redis_password: str,
                 rate_limit_per_minute: int = 60, 
                 burst_limit: int = 100, 
                 exempt_paths: list = None,
                 auto_blacklist_threshold: int = 5,
                 auto_blacklist_expire: int = 3600,
                 ip_blacklist: Array[str] = None):
        super().__init__(app)
        self.redis_url = redis_url
        self.redis_password = redis_password
        self.rate_limit_per_minute = rate_limit_per_minute
        self.burst_limit = burst_limit
        self.exempt_paths = exempt_paths or []
        self.auto_blacklist_threshold = auto_blacklist_threshold
        self.auto_blacklist_expire = auto_blacklist_expire
        self.ip_blacklist = ip_blacklist or []
        self.redis_pool = None
        self.limit_script = None
        self.custom_key_func = None
        logger.info(f"速率限制中间件已初始化，每分钟请求数: {rate_limit_per_minute}, 突发限制: {burst_limit}, "
                  f"豁免路径: {exempt_paths}, 自动黑名单阈值: {auto_blacklist_threshold}, "
                  f"自动黑名单过期时间: {auto_blacklist_expire}秒")

    async def init_redis_pool(self):
        """
        初始化Redis连接池
        """
        logger.info(f"初始化Redis连接池")
        if self.redis_pool is None:
            try:
                self.redis_pool = await redis.from_url(self.redis_url, encoding="utf-8", decode_responses=True, password=self.redis_password)
                # 加载Lua脚本
                self.limit_script = await self.redis_pool.script_load(self.LIMIT_SCRIPT)
                logger.info("Redis连接池已初始化")
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
                    # 加载Lua脚本
                    self.limit_script = await self.redis_pool.script_load(self.LIMIT_SCRIPT)
                    logger.info("Redis连接池已初始化（使用单独的密码参数）")
                except Exception as e2:
                    logger.error(f"Redis连接初始化第二次尝试失败: {str(e2)}")
                    # 设置为None以便下次请求重试
                    self.redis_pool = None

    # 令牌桶算法的Lua脚本实现
    LIMIT_SCRIPT = """
    local key = KEYS[1]
    local rate = tonumber(ARGV[1])
    local burst = tonumber(ARGV[2])
    local now = tonumber(ARGV[3])
    local requested = tonumber(ARGV[4])

    -- 获取当前桶中的令牌数和上次填充时间
    local tokens = tonumber(redis.call('hget', key, 'tokens') or burst)
    local last_time = tonumber(redis.call('hget', key, 'last_time') or 0)

    -- 计算从上次填充到现在应该添加的令牌数
    local fill_time = math.max(0, now - last_time)
    local fill_tokens = math.floor((fill_time * rate) / 60)
    tokens = math.min(burst, tokens + fill_tokens)

    -- 检查是否有足够的令牌
    local allowed = 0
    if tokens >= requested then
        tokens = tokens - requested
        allowed = 1
    end

    -- 更新令牌数和时间
    redis.call('hset', key, 'tokens', tokens)
    redis.call('hset', key, 'last_time', now)
    
    -- 设置过期时间（1小时）
    redis.call('expire', key, 3600)

    return { allowed, tokens }
    """

    def _get_client_ip(self, request: Request) -> str:
        """
        获取客户端真实IP地址
        """
        logger.info(f"获取客户端IP: {request.client.host}")
        # 首先检查X-Forwarded-For头
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            # 使用第一个IP地址（最接近用户的代理）
            return forwarded_for.split(",")[0].strip()
            
        # 如果没有X-Forwarded-For头，使用直接连接的客户端IP
        return request.client.host
        
    def get_rate_limit_key(self, request: Request) -> str:
        """
        生成速率限制的键
        默认使用客户端IP作为键
        可以通过custom_key_func自定义键生成逻辑
        """
        logger.info(f"生成速率限制键: {request.url.path}")
        if self.custom_key_func:
            return self.custom_key_func(request)
        
        # 默认使用IP作为键
        client_ip = self._get_client_ip(request)
        return f"rate_limit:{client_ip}"

    def is_path_exempt(self, path: str) -> bool:
        """
        检查路径是否豁免速率限制
        """
        logger.info(f"检查路径是否豁免速率限制: {path}")
        logger.info(f"全部豁免路径: {self.exempt_paths}")
        for exempt_path in self.exempt_paths:
            if path.startswith(exempt_path):
                logger.info(f"路径 {path} 有豁免速率限制")
                return True
        logger.info(f"路径 {path} 无豁免速率限制")
        return False
        
    async def increment_rate_limit_counter(self, client_ip: str) -> int:
        """
        增加IP的限流计数，并返回当前计数值
        如果计数超过阈值，将IP加入黑名单
        """
        if self.redis_pool is None:
            logger.info(f"初始化Redis连接池用于增加限流计数: {client_ip}")
            await self.init_redis_pool()
            
        counter_key = f"rate_limit_counter:{client_ip}"
        logger.info(f"增加IP限流计数: {counter_key}")
        
        try:
            # 增加计数并设置过期时间
            count = await self.redis_pool.incr(counter_key)
            logger.info(f"IP {client_ip} 当前限流计数: {count}/{self.auto_blacklist_threshold}")
            
            if count == 1:  # 如果是第一次计数，设置过期时间
                await self.redis_pool.expire(counter_key, self.auto_blacklist_expire)
                logger.info(f"设置计数器过期时间: {self.auto_blacklist_expire}秒")
                
            # 检查是否超过阈值
            if count >= self.auto_blacklist_threshold:
                logger.warning(f"IP {client_ip} 限流计数达到阈值 {count}/{self.auto_blacklist_threshold}，准备加入黑名单")
                await self.add_to_blacklist(client_ip)
                
            return count
        except Exception as e:
            logger.error(f"增加限流计数失败: {str(e)}")
            return 0
        
    async def add_to_blacklist(self, client_ip: str) -> None:
        """
        将IP加入黑名单
        """
        try:
            # 检查IP是否已在黑名单中
            if client_ip in self.ip_blacklist:
                logger.info(f"IP {client_ip} 已在内存黑名单中，无需重复添加")
                return
                
            # 将IP加入黑名单
            self.ip_blacklist.append(client_ip)
            logger.warning(f"IP {client_ip} 已被自动加入内存黑名单，触发限流次数过多")
            
            # 在Redis中记录黑名单状态和过期时间
            blacklist_key = f"ip_blacklist:{client_ip}"
            logger.info(f"将IP添加到Redis黑名单: {blacklist_key}, 过期时间: {self.auto_blacklist_expire}秒")
            
            # 确保Redis连接池已初始化
            if self.redis_pool is None:
                logger.info("初始化Redis连接池用于添加黑名单")
                await self.init_redis_pool()
                
            # 设置黑名单键值和过期时间
            result = await self.redis_pool.set(blacklist_key, "1", ex=self.auto_blacklist_expire)
            logger.info(f"Redis黑名单设置结果: {result}")
            
            # 验证黑名单设置是否成功
            exists = await self.redis_pool.exists(blacklist_key)
            logger.info(f"验证Redis黑名单键是否存在: {exists}")
        except Exception as e:
            logger.error(f"将IP {client_ip} 加入黑名单失败: {str(e)}")
            # 即使Redis操作失败，也保留内存中的黑名单记录
        
    async def is_in_auto_blacklist(self, client_ip: str) -> bool:
        """
        检查IP是否在自动黑名单中
        """
        try:
            # 首先检查内存中的黑名单
            if client_ip in self.ip_blacklist:
                logger.info(f"IP {client_ip} 在内存黑名单中")
                return True
                
            # 然后检查Redis中的黑名单
            if self.redis_pool is None:
                logger.info(f"初始化Redis连接池用于检查黑名单: {client_ip}")
                await self.init_redis_pool()
                
            blacklist_key = f"ip_blacklist:{client_ip}"
            logger.info(f"检查IP是否在Redis黑名单中: {blacklist_key}")
            
            exists = await self.redis_pool.exists(blacklist_key)
            logger.info(f"IP {client_ip} 在Redis黑名单中的状态是: {exists}")
            return exists
        except Exception as e:
            logger.error(f"检查IP {client_ip} 是否在黑名单中失败: {str(e)}")
            # 如果Redis检查失败，回退到内存黑名单检查
            return client_ip in self.ip_blacklist

    async def dispatch(self, request: Request, call_next) -> Response:
        logger.info(f"限流入口处理请求: {request.url.path}")
        # 初始化Redis连接池（如果尚未初始化）
        if self.redis_pool is None:
            await self.init_redis_pool()

        # 获取客户端IP
        client_ip = self._get_client_ip(request)
        
        # 检查IP是否在自动黑名单中
        if await self.is_in_auto_blacklist(client_ip):
            logger.warning(f"拒绝来自自动黑名单IP的请求: {client_ip}")
            return JSONResponse(
                status_code=403,
                content={"detail": "您的IP已被临时禁止访问此服务，请稍后再试"}
            )

        # 检查路径是否豁免
        if self.is_path_exempt(request.url.path):
            return await call_next(request)

        # 生成速率限制键
        rate_limit_key = self.get_rate_limit_key(request)
        
        # 执行Lua脚本检查速率限制
        now = int(time.time())
        requested = 1  # 每个请求消耗1个令牌
        
        try:
            logger.info(f"执行速率限制检查: {rate_limit_key}, 脚本ID: {self.limit_script}")
            result = await self.redis_pool.evalsha(
                self.limit_script,
                1,  # 键的数量
                rate_limit_key,  # KEYS[1]
                self.rate_limit_per_minute,  # ARGV[1] - 每分钟填充的令牌数
                self.burst_limit,  # ARGV[2] - 桶的最大容量
                now,  # ARGV[3] - 当前时间
                requested  # ARGV[4] - 请求的令牌数
            )
            
            logger.info(f"速率限制检查结果: {result}")
            allowed, remaining = result
            
            # 设置速率限制的响应头
            headers = {
                "X-RateLimit-Limit": str(self.rate_limit_per_minute),
                "X-RateLimit-Remaining": str(remaining),
                "X-RateLimit-Reset": str(now + 60)  # 下一分钟重置
            }
            
            if allowed == 1:
                # 允许请求
                response = await call_next(request)
                
                # 将速率限制头添加到响应中
                for name, value in headers.items():
                    response.headers[name] = value
                    
                return response
            else:
                # 拒绝请求 - 返回429 Too Many Requests
                logger.warning(f"速率限制触发: {rate_limit_key}")
                
                # 增加限流计数
                count = await self.increment_rate_limit_counter(client_ip)
                logger.info(f"IP {client_ip} 触发限流计数: {count}/{self.auto_blacklist_threshold}")
                
                return JSONResponse(
                    status_code=429,
                    content={"detail": "请求过于频繁，请稍后再试"},
                    headers=headers
                )
                
        except Exception as e:
            # 如果Redis出现问题，记录错误但允许请求通过
            logger.error(f"速率限制检查失败: {str(e)}")
            return await call_next(request)