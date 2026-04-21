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
    为小红书文案生成配图（单张）

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


@tool
def generate_post_images(prompts: list, size: str = "2K") -> str:
    """
    为小红书文案生成多张配图

    Args:
        prompts: 图片描述列表，每个描述生成一张图，用于生成符合小红书风格的图文内容
        size: 图片尺寸，可选 "2K" 或 "4K"，默认 "2K"

    Returns:
        所有生成图片的URL列表，失败时返回错误信息

    注意事项：
    - 生成图文时，请在prompt中详细描述需要显示的文字内容
    - 描述应该包含：背景图案、文字内容、排版布局、装饰元素（如卡通人物）
    - 例如："ins风渐变背景，中心位置展示标题'夏日续命水'，使用手写体字体，浅色文字，右下角添加可爱的卡通人物装饰"
    """
    ctx = request_context.get() or new_context(method="generate_post_images")

    try:
        client = ImageGenerationClient(ctx=ctx)
        results = []

        for i, prompt in enumerate(prompts, 1):
            response = client.generate(
                prompt=prompt,
                size=size,
                model="doubao-seedream-5-0-260128"
            )

            if response.success:
                image_url = response.image_urls[0]
                results.append(f"图片{i}：{image_url}")
            else:
                error_msg = ", ".join(response.error_messages) if response.error_messages else "未知错误"
                results.append(f"图片{i}生成失败：{error_msg}")

        return "\n".join(results)

    except Exception as e:
        return f"图片生成异常：{str(e)}"
