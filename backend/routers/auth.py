# ============================================================
# 颐邻通 V1.0 - 登录接口路由
# POST /api/login
# ============================================================

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import User
from schemas import LoginRequest, LoginResponse

router = APIRouter()


@router.post("/login", response_model=LoginResponse, summary="用户登录")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    """
    用户登录校验。
    - 校验账号密码是否匹配
    - 校验账号状态是否启用
    - 登录成功返回用户信息（含 role 字段供前端按角色跳转）
    """
    # 1. 根据账号查用户
    user = db.query(User).filter(User.account == req.account).first()
    if not user:
        raise HTTPException(status_code=400, detail="账号不存在")

    # 2. 校验密码
    if user.password != req.password:
        raise HTTPException(status_code=400, detail="密码错误")

    # 3. 校验账号状态
    if user.status != "启用":
        raise HTTPException(status_code=400, detail="账号已停用，请联系管理员")

    # 4. 登录成功，返回用户信息
    return LoginResponse(
        id=user.id,
        account=user.account,
        name=user.name,
        role=user.role,
    )
