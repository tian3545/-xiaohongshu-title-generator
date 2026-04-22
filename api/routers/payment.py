from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from typing import Optional
import sys
import os
import hashlib
import time
import random
import string

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from database import create_order, get_order_by_no, update_order_status, add_balance, get_user_balance, get_all_packages, get_package_by_id, get_user_orders
from api.routers.auth import get_current_user
from config.settings import settings

router = APIRouter(prefix="/payment", tags=["支付"])

# ===== 数据模型 =====

class CreateOrderRequest(BaseModel):
    package_id: int

class CreateOrderResponse(BaseModel):
    success: bool
    order_no: Optional[str] = None
    payment_params: Optional[dict] = None
    message: Optional[str] = None

# ===== 支付工具函数 =====

def generate_sign(params: dict, api_key: str) -> str:
    """生成签名（微信支付）"""
    sorted_params = sorted(params.items())
    sign_str = '&'.join([f"{k}={v}" for k, v in sorted_params if k != 'sign' and v])
    sign_str += f"&key={api_key}"
    return hashlib.md5(sign_str.encode('utf-8')).hexdigest().upper()

def generate_nonce_str() -> str:
    """生成随机字符串"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=32))

# ===== API路由 =====

@router.get("/packages")
async def get_packages():
    """获取所有套餐"""
    packages = get_all_packages()
    return {
        "success": True,
        "data": packages
    }

@router.post("/create-order", response_model=CreateOrderResponse)
async def create_payment_order(
    request: CreateOrderRequest,
    current_user: dict = Depends(get_current_user)
):
    """创建支付订单"""
    # 检查套餐是否存在
    package = get_package_by_id(request.package_id)
    if not package:
        raise HTTPException(status_code=404, detail="套餐不存在")

    # 创建订单
    order = create_order(current_user['id'], request.package_id)

    # 这里应该调用微信支付API获取支付参数
    # 由于需要真实的微信支付账号，这里返回模拟数据
    payment_params = {
        "order_no": order['order_no'],
        "amount": float(order['amount']),
        "description": f"购买{package['name']} - {package['count']}次",
        # 实际开发中这里返回微信支付或支付宝的支付参数
        "payment_url": f"https://example.com/pay?order_no={order['order_no']}",
        "qr_code": f"weixin://wxpay/bizpayurl?pr={order['order_no']}",
    }

    return {
        "success": True,
        "order_no": order['order_no'],
        "payment_params": payment_params,
        "message": "订单创建成功"
    }

@router.post("/mock-pay/{order_no}")
async def mock_payment(order_no: str):
    """
    模拟支付成功（仅用于测试，生产环境删除）
    实际环境中应该由微信/支付宝回调
    """
    order = get_order_by_no(order_no)
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")

    if order['status'] == 'paid':
        return {"success": True, "message": "订单已支付"}

    # 更新订单状态
    update_order_status(order_no, 'paid', 'mock_payment')

    # 增加用户余额
    add_balance(order['user_id'], order['count'])

    return {
        "success": True,
        "message": "支付成功",
        "data": {
            "order_no": order_no,
            "count": order['count']
        }
    }

@router.get("/notify")
async def payment_notify(request: Request):
    """
    支付回调（微信支付/支付宝）
    实际开发中需要根据支付平台的回调格式解析
    """
    # 这里需要实现具体的支付回调逻辑
    # 1. 验证签名
    # 2. 检查订单
    # 3. 更新订单状态
    # 4. 增加用户余额
    # 5. 返回成功响应

    return {"code": "SUCCESS", "message": "OK"}

@router.get("/orders")
async def get_user_payment_orders(
    limit: int = 20,
    current_user: dict = Depends(get_current_user)
):
    """获取用户订单列表"""
    orders = get_user_orders(current_user['id'], limit)

    return {
        "success": True,
        "data": orders
    }
