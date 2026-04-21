"""
小红书文案配图生成工具
"""

import os
import requests
from datetime import datetime
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
        生成图片的本地文件路径，失败时返回错误信息
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

            # 下载图片到本地
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"xiaohongshu_image_{timestamp}.jpg"
            filepath = os.path.join("/tmp", filename)

            img_response = requests.get(image_url, timeout=30)
            img_response.raise_for_status()

            with open(filepath, 'wb') as f:
                f.write(img_response.content)

            return f"图片生成成功！已保存到：{filepath}"
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
        所有生成图片的本地文件路径列表，每张图一行，失败时返回错误信息

    注意事项：
    - 生成图文时，请在prompt中详细描述需要显示的文字内容
    - 描述应该包含：背景图案、文字内容、排版布局、装饰元素（如卡通人物）
    - 例如："ins风渐变背景，中心位置展示标题'夏日续命水'，使用手写体字体，浅色文字，右下角添加可爱的卡通人物装饰"
    - 图片会自动下载到 /tmp 目录，可以直接保存到手机相册使用
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

                # 下载图片到本地
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"xiaohongshu_image_{i}_{timestamp}.jpg"
                filepath = os.path.join("/tmp", filename)

                img_response = requests.get(image_url, timeout=30)
                img_response.raise_for_status()

                with open(filepath, 'wb') as f:
                    f.write(img_response.content)

                results.append(filepath)
            else:
                error_msg = ", ".join(response.error_messages) if response.error_messages else "未知错误"
                results.append(f"图片{i}生成失败：{error_msg}")

        # 返回所有图片的文件路径，每行一个
        return "\n".join(results)

    except Exception as e:
        return f"图片生成异常：{str(e)}"
