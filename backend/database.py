from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 检查是否在测试环境中
TESTING = os.getenv("TESTING", "False").lower() in ("true", "1", "t")

# 如果在测试环境中，使用SQLite内存数据库，否则使用MySQL
if TESTING:
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///:memory:")
else:
    # 数据库连接配置
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_NAME = os.getenv("DB_NAME", "gxblog")
    
    # 构建数据库连接URL
    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 创建SQLAlchemy引擎
engine = create_engine(
    DATABASE_URL,
    echo=False,  # 设置为False以禁止打印SQL语句
    pool_pre_ping=True  # 自动检测连接是否有效
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基类
Base = declarative_base()

# 获取数据库会话的依赖函数
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()