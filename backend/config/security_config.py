# 安全配置文件
import os
from typing import List, Dict, Any
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# Redis配置
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)
# 速率限制配置
RATE_LIMIT_PER_MINUTE = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))  # 默认每分钟60个请求
BURST_LIMIT = int(os.getenv("BURST_LIMIT", "10"))  # 默认突发请求限制

# 自动黑名单配置
AUTO_BLACKLIST_THRESHOLD = int(os.getenv("AUTO_BLACKLIST_THRESHOLD", "5"))  # 默认触发限流5次后加入黑名单
AUTO_BLACKLIST_EXPIRE = int(os.getenv("AUTO_BLACKLIST_EXPIRE", "3600"))  # 默认黑名单过期时间（秒）

# IP白名单和黑名单
# 从环境变量中读取，格式为逗号分隔的IP地址
IP_WHITELIST = os.getenv("IP_WHITELIST", "").split(",") if os.getenv("IP_WHITELIST") else []
IP_BLACKLIST = os.getenv("IP_BLACKLIST", "").split(",") if os.getenv("IP_BLACKLIST") else []

# 豁免速率限制的路径
EXEMPT_PATHS = [
    "/",  # 健康检查端点
    "/docs",  # Swagger文档
    "/redoc",  # ReDoc文档
    "/openapi.json",  # OpenAPI规范
]

# 安全配置字典
SECURITY_CONFIG = {
    "redis_url": REDIS_URL,
    "redis_password": REDIS_PASSWORD,
    "rate_limit": {
        "per_minute": RATE_LIMIT_PER_MINUTE,
        "burst": BURST_LIMIT,
        "exempt_paths": EXEMPT_PATHS,
    },
    "ip_filter": {
        "whitelist": IP_WHITELIST,
        "blacklist": IP_BLACKLIST,
        "auto_blacklist": {
            "threshold": AUTO_BLACKLIST_THRESHOLD,
            "expire": AUTO_BLACKLIST_EXPIRE
        }
    },
}

# 打印安全配置（调试用）
def print_security_config():
    """打印安全配置信息（敏感信息会被隐藏）"""
    import json
    # 创建配置的副本，隐藏敏感信息
    config_copy = SECURITY_CONFIG.copy()
    
    # 隐藏Redis URL中的密码（如果有）
    if "redis_url" in config_copy:
        redis_url = config_copy["redis_url"]
        if "@" in redis_url:
            # 格式可能是: redis://user:password@host:port/db
            parts = redis_url.split("@")
            auth_part = parts[0].split("://")[1]
            if ":" in auth_part:
                user = auth_part.split(":")[0]
                config_copy["redis_url"] = f"redis://{user}:****@{parts[1]}"
    
    print(json.dumps(config_copy, indent=2))

if __name__ == "__main__":
    # 如果直接运行此文件，打印配置信息
    print_security_config()