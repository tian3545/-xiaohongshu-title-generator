"""
小红书文案配图生成工具
"""

from langchain.tools import tool
from coze_coding_utils.log.write_log import request_context
from coze_coding_utils.runtime_ctx.context import new_context
from coze_coding_dev_sdk import ImageGenerationClient


@tool
def generate_post_image(prompt: str, size: str = "2K") -> str:
    """
    为小红书文案生成配图

    Args:
        prompt: 图片描述，用于生成符合小红书风格的配图
        size: 图片尺寸，可选 "2K" 或 "4K"，默认 "2K"

    Returns:
        生成图片的URL，失败时返回错误信息
    """
    ctx = request_context.get() or new_context(method="generate_post_image")

    try:
        client = ImageGenerationClient(ctx=ctx)

        response = client.generate(
            prompt=prompt,
            size=size,
            model="doubao-seedream-5-0-260128"
        )

        if response.success:
            image_url = response.image_urls[0]
            return f"图片生成成功！图片链接：{image_url}"
        else:
            error_msg = ", ".join(response.error_messages) if response.error_messages else "未知错误"
            return f"图片生成失败：{error_msg}"

    except Exception as e:
        return f"图片生成异常：{str(e)}"
