# 安全工具类
import re
import hashlib
import logging
from typing import Dict, Any, Optional, List
from fastapi import Request, HTTPException
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class SecurityUtils:
    """
    安全工具类，提供各种安全相关的工具方法
    """
    
    @staticmethod
    def sanitize_input(input_str: str) -> str:
        """
        清理输入字符串，防止XSS攻击
        """
        if not input_str:
            return ""
            
        # 移除可能的HTML标签
        sanitized = re.sub(r'<[^>]*>', '', input_str)
        
        # 移除JavaScript事件
        sanitized = re.sub(r'on\w+=["\']?[^>]*', '', sanitized)
        
        # 移除危险的CSS表达式
        sanitized = re.sub(r'expression\([^)]*\)', '', sanitized)
        
        # 移除危险的URL协议
        sanitized = re.sub(r'javascript:', '', sanitized, flags=re.IGNORECASE)
        sanitized = re.sub(r'vbscript:', '', sanitized, flags=re.IGNORECASE)
        
        return sanitized
    
    @staticmethod
    def validate_request_params(request_data: Dict[str, Any], required_fields: List[str]) -> bool:
        """
        验证请求参数是否包含所有必需字段
        """
        for field in required_fields:
            if field not in request_data or request_data[field] is None:
                return False
        return True
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        使用SHA-256哈希密码
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        验证密码是否匹配
        """
        return SecurityUtils.hash_password(plain_password) == hashed_password
    
    @staticmethod
    def get_client_ip(request: Request) -> str:
        """
        获取客户端真实IP地址
        """
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            # 获取最原始的IP（最左侧的）
            return forwarded.split(",")[0]
        return request.client.host
    
    @staticmethod
    def log_security_event(event_type: str, details: Dict[str, Any], request: Optional[Request] = None) -> None:
        """
        记录安全事件
        """
        log_data = {
            "event_type": event_type,
            "details": details
        }
        
        if request:
            log_data["client_ip"] = SecurityUtils.get_client_ip(request)
            log_data["user_agent"] = request.headers.get("User-Agent")
            log_data["path"] = request.url.path
            log_data["method"] = request.method
        
        logger.warning(f"安全事件: {log_data}")

# 安全相关的依赖项
def validate_search_keyword(keyword: str) -> str:
    """
    验证并清理搜索关键词
    可以作为FastAPI的依赖项使用
    """
    if not keyword or len(keyword) < 1:
        raise HTTPException(status_code=400, detail="搜索关键词不能为空")
        
    if len(keyword) > 100:
        raise HTTPException(status_code=400, detail="搜索关键词过长")
    
    # 清理输入
    sanitized = SecurityUtils.sanitize_input(keyword)
    
    # 如果清理后为空，则拒绝请求
    if not sanitized:
        raise HTTPException(status_code=400, detail="搜索关键词包含不允许的字符")
    
    return sanitized