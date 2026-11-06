# ============================================================
# 颐邻通 V1.0 - 工单接口路由
# POST   /api/orders              提交咨询工单
# GET    /api/orders              查询工单列表
# PUT    /api/orders/{id}/cancel  取消工单
# PUT    /api/orders/{id}/assign  分派工单
# PUT    /api/orders/{id}/review  复核审批
# ============================================================

import random
from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import WorkOrder, User
from schemas import OrderCreateRequest, OrderReviewRequest, MessageResponse

router = APIRouter()


# ---------- 辅助函数 ----------
def _generate_order_no() -> str:
    """生成工单编号：WO + 年月日时分秒 + 3位随机数"""
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    rand = str(random.randint(100, 999))
    return f"WO{ts}{rand}"


def _order_to_dict(o: WorkOrder) -> dict:
    """把 ORM 对象转成前端要用的字典"""
    return {
        "id": o.id,
        "order_no": o.order_no,
        "elder_name": o.elder_name,
        "content": o.content,
        "status": o.status,
        "reply_content": o.reply_content,
        "submit_time": o.submit_time.strftime("%Y-%m-%d %H:%M:%S") if o.submit_time else None,
        "assign_time": o.assign_time.strftime("%Y-%m-%d %H:%M:%S") if o.assign_time else None,
        "review_time": o.review_time.strftime("%Y-%m-%d %H:%M:%S") if o.review_time else None,
    }


# ---------- POST /api/orders ----------
@router.post("/orders", summary="家属提交咨询工单")
def create_order(req: OrderCreateRequest, db: Session = Depends(get_db)):
    """
    家属在 consult.html 提交咨询内容后调用。
    V1.0 简化：submitter_id 固定为 1（fam01），后续再按登录态区分。
    """
    # 生成工单编号（直到生成不重复的为止）
    order_no = _generate_order_no()
    while db.query(WorkOrder).filter(WorkOrder.order_no == order_no).first():
        order_no = _generate_order_no()

    new_order = WorkOrder(
        order_no=order_no,
        submitter_id=req.submitter_id or 1,
        elder_name=req.elder_name.strip(),
        content=req.content.strip(),
        status="待分派",
        submit_time=datetime.now(),
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return {"code": 0, "msg": "工单提交成功", "data": {"id": new_order.id, "order_no": new_order.order_no}}


# ---------- GET /api/orders ----------
@router.get("/orders", summary="查询工单列表")
def list_orders(db: Session = Depends(get_db)):
    """
    工单处理台和家属端都调用此接口获取列表。
    V1.0 简化：返回全部工单，不做角色过滤。
    """
    orders = db.query(WorkOrder).order_by(WorkOrder.submit_time.desc()).all()
    return [_order_to_dict(o) for o in orders]


# ---------- PUT /api/orders/{id}/cancel ----------
@router.put("/orders/{order_id}/cancel", summary="取消工单")
def cancel_order(order_id: int, db: Session = Depends(get_db)):
    """
    家属在 consult.html 可取消自己未复核通过的工单。
    已进入"复核通过"、"已办结"、"已取消"的工单不能再取消。
    """
    order = db.query(WorkOrder).filter(WorkOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="工单不存在")

    # 已复核通过/已办结/已取消，不允许再取消
    if order.status in ("复核通过", "已办结", "已取消"):
        raise HTTPException(status_code=400, detail=f"当前状态【{order.status}】不可取消")

    order.status = "已取消"
    db.commit()
    return {"code": 0, "msg": "工单已取消"}


# ---------- PUT /api/orders/{id}/assign ----------
@router.put("/orders/{order_id}/assign", summary="分派工单")
def assign_order(order_id: int, db: Session = Depends(get_db)):
    """
    管理员 / 助老员在 workorder.html 把"待分派"的工单派给自己。
    只有状态为"待分派"的工单才能分派。
    """
    order = db.query(WorkOrder).filter(WorkOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="工单不存在")

    if order.status != "待分派":
        raise HTTPException(status_code=400, detail=f"只能分派状态为【待分派】的工单，当前为【{order.status}】")

    order.status = "处理协同中"
    order.assign_time = datetime.now()
    db.commit()
    return {"code": 0, "msg": "工单已分派，状态变更为【处理协同中】"}


# ---------- PUT /api/orders/{id}/review ----------
@router.put("/orders/{order_id}/review", summary="复核审批")
def review_order(order_id: int, req: OrderReviewRequest, db: Session = Depends(get_db)):
    """
    助老员 / 管理员在 workorder.html 对工单做复核。
    - review_result 只能填 "通过" 或 "驳回重议"
    - 通过 → 状态变"复核通过"，同时 reply_content 写入答复
    - 驳回 → 状态变"驳回重议"
    """
    order = db.query(WorkOrder).filter(WorkOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="工单不存在")

    # 只有"处理协同中"或"复核中"的工单才能复核
    if order.status not in ("处理协同中", "复核中"):
        raise HTTPException(status_code=400, detail=f"当前状态【{order.status}】不可复核")

    result = req.review_result.strip()
    if result not in ("通过", "驳回重议"):
        raise HTTPException(status_code=400, detail="review_result 只能填 '通过' 或 '驳回重议'")

    order.reply_content = req.reply_content or ""
    order.review_time = datetime.now()

    if result == "通过":
        order.status = "复核通过"
    else:
        order.status = "驳回重议"

    db.commit()
    return {"code": 0, "msg": f"复核完成，结果：{result}"}
