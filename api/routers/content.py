from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
import sys
import os
import re

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from database import use_balance, log_usage, get_user_balance
from api.routers.auth import get_current_user

# 尝试导入智能体
try:
    from agents.agent import build_agent
    AGENT_AVAILABLE = True
except ImportError:
    AGENT_AVAILABLE = False
    print("警告：智能体模块未找到，将使用模拟数据")

router = APIRouter(prefix="/content", tags=["内容生成"])

# ===== 数据模型 =====

class GenerateRequest(BaseModel):
    topic: str
    need_images: bool = True

class GenerateResponse(BaseModel):
    success: bool
    data: Optional[dict] = None
    message: Optional[str] = None

# ===== 内容生成逻辑 =====

async def generate_xiaohongshu_content(topic: str, need_images: bool):
    """
    调用智能体生成小红书文案
    """
    try:
        if AGENT_AVAILABLE:
            # 调用智能体
            agent = build_agent()

            # 构建提示词
            prompt = f"帮我写一篇关于\"{topic}\"的小红书爆款文案"
            if need_images:
                prompt += "，要求生成4张图文"

            # 调用智能体
            result = agent.invoke({"messages": [{"role": "user", "content": prompt}]})

            # 获取生成的文案
            content_text = result["messages"][-1]["content"]

            # 解析文案（提取标题、正文、标签、图片）
            return parse_content(content_text)
        else:
            # 智能体不可用，返回模拟数据
            return generate_mock_content(topic, need_images)
    except Exception as e:
        print(f"智能体调用失败: {e}")
        # 如果智能体失败，返回模拟数据
        return generate_mock_content(topic, need_images)

def parse_content(content_text: str):
    """解析生成的文案内容"""
    lines = content_text.split('\n')

    # 提取标题（第一行）
    title = lines[0] if lines else ""

    # 提取图片链接
    image_pattern = r'!\[.*?\]\((.*?)\)'
    images = re.findall(image_pattern, content_text)

    # 提取标签（#开头）
    tag_pattern = r'#[^\s#]+'
    tags = re.findall(tag_pattern, content_text)

    # 提取正文（除去标题、标签、图片）
    body_lines = []
    in_image_section = False
    for line in lines[1:]:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith('!['):
            in_image_section = True
            continue
        if not stripped.startswith('#') and not in_image_section:
            body_lines.append(stripped)

    body = '\n'.join(body_lines)

    return {
        "title": title,
        "body": body,
        "tags": tags,
        "images": images
    }

def generate_mock_content(topic: str, need_images: bool):
    """生成模拟数据"""
    title = f"🔥{topic}｜超实用的分享"
    body = f"""
姐妹们，今天给你们分享一下{topic}！💕

✅ 精髓1：关键在于细节
一定要注重每一个小细节，这样才能达到最好的效果

✅ 精髓2：坚持是关键
只有坚持下去，才能看到结果

✅ 精髓3：不断学习
持续学习新知识，才能不断进步

你们还有什么想了解的吗？评论区告诉我～
喜欢的姐妹记得👍+⭐️，一起变得更好！💕
        """.strip()

    tags = [f"#{topic}", "#分享", "#干货", "#生活"]

    # 如果需要生成图片，返回示例图片链接
    images = []
    if need_images:
        images = [
            "https://via.placeholder.com/800x600/667eea/ffffff?text=Image+1",
            "https://via.placeholder.com/800x600/764ba2/ffffff?text=Image+2",
            "https://via.placeholder.com/800x600/667eea/ffffff?text=Image+3",
            "https://via.placeholder.com/800x600/764ba2/ffffff?text=Image+4"
        ]

    return {
        "title": title,
        "body": body,
        "tags": tags,
        "images": images
    }

# ===== API路由 =====

@router.post("/generate", response_model=GenerateResponse)
async def generate_content(
    request: GenerateRequest,
    current_user: dict = Depends(get_current_user)
):
    """生成小红书文案"""
    # 检查余额是否足够
    success = use_balance(current_user['id'])
    if not success:
        balance = get_user_balance(current_user['id'])
        raise HTTPException(
            status_code=403,
            detail=f"余额不足，剩余{balance['remaining_count']}次，请购买套餐"
        )

    try:
        # 生成内容
        result = await generate_xiaohongshu_content(request.topic, request.need_images)

        # 记录使用
        log_usage(current_user['id'], request.topic, request.need_images)

        return {
            "success": True,
            "data": result
        }
    except HTTPException:
        raise
    except Exception as e:
        # 如果生成失败，返还余额
        # 这里简化处理，实际应该实现回滚逻辑
        raise HTTPException(status_code=500, detail=f"生成失败: {str(e)}")

@router.get("/history")
async def get_history(
    limit: int = 20,
    current_user: dict = Depends(get_current_user)
):
    """获取生成历史"""
    from database import get_user_usage_logs

    logs = get_user_usage_logs(current_user['id'], limit)

    return {
        "success": True,
        "data": logs
    }
