# ============================================================
# 颐邻通 V1.0 社区养老便民服务平台 - 数据库连接配置
# 数据库：MySQL 8.0，本机 root 密码为 123456
# ============================================================

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# --- 数据库连接信息 ---
DB_USER    = "root"
DB_PASSWORD = "123456"
DB_HOST    = "localhost"
DB_PORT    = "3306"
DB_NAME    = "elderlink_v10"

# 构造 SQLAlchemy 连接串（使用 pymysql 驱动）
SQLALCHEMY_DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
)

# 创建引擎（pool_pre_ping=True 防止长时间空闲连接断开）
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

# SessionLocal：每次请求会拿到一个独立的数据库会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base：所有 ORM 模型要继承这个类
Base = declarative_base()


def get_db():
    """FastAPI 依赖函数：为每个请求提供一个数据库会话，请求结束后自动关闭。"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
