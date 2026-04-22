from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from database import get_user_balance
from api.routers.auth import get_current_user

router = APIRouter(prefix="/user", tags=["用户管理"])

# ===== 数据模型 =====

class BalanceResponse(BaseModel):
    success: bool
    data: Optional[dict] = None

class DashboardResponse(BaseModel):
    success: bool
    data: Optional[dict] = None

# ===== API路由 =====

@router.get("/balance", response_model=BalanceResponse)
async def get_user_balance_info(current_user: dict = Depends(get_current_user)):
    """获取用户余额"""
    balance = get_user_balance(current_user['id'])

    return {
        "success": True,
        "data": {
            "remaining_count": balance['remaining_count'],
            "total_purchased": balance['total_purchased'],
            "total_used": balance['total_used']
        }
    }

@router.get("/dashboard", response_model=DashboardResponse)
async def get_user_dashboard(current_user: dict = Depends(get_current_user)):
    """获取用户仪表盘数据"""
    from database import get_user_usage_logs, get_user_orders

    # 获取余额
    balance = get_user_balance(current_user['id'])

    # 获取最近使用记录
    recent_usage = get_user_usage_logs(current_user['id'], 5)

    # 获取最近订单
    recent_orders = get_user_orders(current_user['id'], 5)

    return {
        "success": True,
        "data": {
            "balance": {
                "remaining_count": balance['remaining_count'],
                "total_purchased": balance['total_purchased'],
                "total_used": balance['total_used']
            },
            "recent_usage": recent_usage,
            "recent_orders": recent_orders
        }
    }
