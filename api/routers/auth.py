from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from pydantic import BaseModel, EmailStr
from typing import Optional
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from database import create_user, get_user_by_email, update_user_last_login, get_user_balance
from email_verification import send_code, verify_code, get_remaining_time
from config.settings import settings

router = APIRouter(prefix="/auth", tags=["认证"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# ===== 数据模型 =====

class SendCodeRequest(BaseModel):
    email: EmailStr

class LoginRequest(BaseModel):
    email: EmailStr
    code: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict

class UserInfo(BaseModel):
    id: int
    email: str
    remaining_count: int
    total_purchased: int
    total_used: int

# ===== JWT工具函数 =====

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """创建访问令牌"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    """验证令牌"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        if email is None or user_id is None:
            raise HTTPException(status_code=401, detail="无效的令牌")
        return {"email": email, "user_id": user_id}
    except JWTError:
        raise HTTPException(status_code=401, detail="无效的令牌")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """获取当前用户"""
    credentials = verify_token(token)
    user = get_user_by_email(credentials["email"])
    if user is None:
        raise HTTPException(status_code=401, detail="用户不存在")
    return user

# ===== API路由 =====

@router.post("/send-code")
async def send_verification_code(request: SendCodeRequest):
    """发送验证码"""
    # 检查剩余时间
    remaining = get_remaining_time(request.email)
    if remaining and remaining > 0:
        return {
            "success": False,
            "message": f"请等待{remaining}秒后再发送",
            "remaining_seconds": remaining
        }

    # 发送验证码
    success, message = send_code(request.email)

    if success:
        return {
            "success": True,
            "message": message
        }
    else:
        return {
            "success": False,
            "message": message
        }

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """验证码登录"""
    # 验证验证码
    if not verify_code(request.email, request.code):
        raise HTTPException(status_code=400, detail="验证码错误或已过期")

    # 检查用户是否存在
    user = get_user_by_email(request.email)
    if not user:
        # 自动注册
        user_id = create_user(request.email)
        user = get_user_by_id(user_id)

    # 更新最后登录时间
    update_user_last_login(user['id'])

    # 获取用户余额
    balance = get_user_balance(user['id'])

    # 创建访问令牌
    access_token = create_access_token(
        data={
            "sub": user['email'],
            "user_id": user['id']
        },
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user['id'],
            "email": user['email'],
            "remaining_count": balance['remaining_count'],
            "total_purchased": balance['total_purchased'],
            "total_used": balance['total_used']
        }
    }

@router.get("/me", response_model=UserInfo)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """获取当前用户信息"""
    balance = get_user_balance(current_user['id'])

    return {
        "id": current_user['id'],
        "email": current_user['email'],
        "remaining_count": balance['remaining_count'],
        "total_purchased": balance['total_purchased'],
        "total_used": balance['total_used']
    }
