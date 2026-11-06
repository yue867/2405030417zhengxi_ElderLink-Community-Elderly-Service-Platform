# ============================================================
# 颐邻通 V1.0 - SQLAlchemy ORM 模型
# 仅 V1.0 两张表：user / work_order
# ============================================================

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    """用户表：家属 / 助老员 / 管理员"""
    __tablename__ = "user"

    id        = Column(Integer, primary_key=True, autoincrement=True, comment="用户编号")
    account   = Column(String(50), nullable=False, unique=True, comment="登录账号")
    name      = Column(String(50), nullable=False, comment="姓名")
    role      = Column(String(20), nullable=False, comment="角色")
    community = Column(String(100), nullable=False, default="", comment="所属社区")
    password  = Column(String(100), nullable=False, comment="登录密码")
    status    = Column(String(20), nullable=False, default="启用", comment="账号状态")


class WorkOrder(Base):
    """工单表：咨询工单 V1.0 版本"""
    __tablename__ = "work_order"

    id            = Column(Integer, primary_key=True, autoincrement=True, comment="工单主键")
    order_no      = Column(String(30), nullable=False, unique=True, comment="工单编号")
    submitter_id  = Column(Integer, ForeignKey("user.id"), nullable=False, comment="提交人ID")
    elder_name    = Column(String(50), nullable=False, comment="老人姓名")
    content       = Column(Text, nullable=False, comment="咨询内容")
    status        = Column(String(20), nullable=False, default="待分派", comment="工单状态")
    reply_content = Column(Text, nullable=True, comment="答复内容")
    submit_time   = Column(DateTime, nullable=False, comment="提交时间")
    assign_time   = Column(DateTime, nullable=True, comment="分派时间")
    review_time   = Column(DateTime, nullable=True, comment="复核时间")

    # 提交人关联（方便查询时拿到提交人信息）
    submitter = relationship("User")
