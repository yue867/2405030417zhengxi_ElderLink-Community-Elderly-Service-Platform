# ============================================================
# 颐邻通 V1.0 - Pydantic 数据模型（请求体 / 响应体）
# ============================================================

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# ------- 登录相关 -------
class LoginRequest(BaseModel):
    """登录请求体"""
    account: str
    password: str


class LoginResponse(BaseModel):
    """登录响应体"""
    id: int
    account: str
    name: str
    role: str


# ------- 工单相关 -------
class OrderCreateRequest(BaseModel):
    """家属提交咨询工单的请求体"""
    elder_name: str
    content: str
    submitter_id: Optional[int] = 1  # V1.0 简化：默认提交人ID


class OrderReviewRequest(BaseModel):
    """复核审批请求体"""
    review_result: str           # 只能填 "通过" 或 "驳回重议"
    reply_content: Optional[str] = ""


class OrderCancelRequest(BaseModel):
    """取消工单请求体（可空请求体也行）"""
    reason: Optional[str] = ""


# ------- 通用响应 -------
class MessageResponse(BaseModel):
    """通用操作响应"""
    code: int = 0
    msg: str = ""
