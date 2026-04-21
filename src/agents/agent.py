import os
import json
from typing import Annotated
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage
from coze_coding_utils.runtime_ctx.context import default_headers
from storage.memory.memory_saver import get_memory_saver

# 导入工具
from tools.image_generation_tool import generate_post_image, generate_post_images

LLM_CONFIG = "config/agent_llm_config.json"
TEMPLATES_FILE = "assets/xiaohongshu_templates.json"

# 默认保留最近 20 轮对话 (40 条消息)
MAX_MESSAGES = 40

def _windowed_messages(old, new):
    """滑动窗口: 只保留最近 MAX_MESSAGES 条消息"""
    return add_messages(old, new)[-MAX_MESSAGES:] # type: ignore

class AgentState(MessagesState):
    messages: Annotated[list[AnyMessage], _windowed_messages]

def load_templates():
    """
    加载小红书话术资源库

    Returns:
        dict: 话术资源数据，如果加载失败返回空字典
    """
    workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
    templates_path = os.path.join(workspace_path, TEMPLATES_FILE)

    try:
        if os.path.exists(templates_path):
            with open(templates_path, 'r', encoding='utf-8') as f:
                templates = json.load(f)
                return templates
        return {}
    except Exception as e:
        print(f"加载话术资源库失败: {e}")
        return {}

def enhance_system_prompt(base_prompt, templates):
    """
    将话术资源库注入到system prompt中

    Args:
        base_prompt: 基础system prompt
        templates: 话术资源数据

    Returns:
        str: 增强后的system prompt
    """
    if not templates:
        return base_prompt

    # 构建话术资源库的提示部分
    templates_section = "\n\n# 🎨 爆款文案话术资源库（请灵活使用哦！）\n\n"

    # 开头句式
    if "openings" in templates:
        templates_section += "## 💫 亲切开头句式\n"
        for i, opening in enumerate(templates["openings"], 1):
            templates_section += f"{i}. {opening}\n"
        templates_section += "\n"

    # 结尾句式
    if "closings" in templates:
        templates_section += "## 💗 温暖结尾句式\n"
        for i, closing in enumerate(templates["closings"], 1):
            templates_section += f"{i}. {closing}\n"
        templates_section += "\n"

    # 互动引导
    if "interaction_prompts" in templates:
        templates_section += "## 💬 互动引导话术\n"
        for i, prompt in enumerate(templates["interaction_prompts"], 1):
            templates_section += f"{i}. {prompt}\n"
        templates_section += "\n"

    # 过渡短语
    if "transition_phrases" in templates:
        templates_section += "## 🔄 过渡短语\n"
        for i, phrase in enumerate(templates["transition_phrases"], 1):
            templates_section += f"{i}. {phrase}\n"
        templates_section += "\n"

    # 语气修饰词
    if "tone_modifiers" in templates:
        templates_section += "## ✨ 语气修饰词\n"
        for i, modifier in enumerate(templates["tone_modifiers"], 1):
            templates_section += f"{i}. {modifier}\n"
        templates_section += "\n"

    # Emoji分类
    if "emojis" in templates:
        templates_section += "## 🎭 Emoji使用指南\n"
        emojis = templates["emojis"]
        for category, emoji_list in emojis.items():
            if isinstance(emoji_list, list):
                templates_section += f"### {category}\n"
                templates_section += f"{', '.join(emoji_list)}\n\n"

    # 标题模板
    if "title_templates" in templates:
        templates_section += "## 📌 标题模板\n"
        templates_section += "使用 {keyword} 替换关键词，{emotion} 替换情感词，{description} 替换描述词：\n"
        for i, template in enumerate(templates["title_templates"], 1):
            templates_section += f"{i}. {template}\n"
        templates_section += "\n"

    # 标签分类
    if "tag_categories" in templates:
        templates_section += "## 🏷️ 标签分类参考\n"
        for category, tags in templates["tag_categories"].items():
            templates_section += f"### {category}\n"
            templates_section += f"{', '.join(tags)}\n\n"

    templates_section += "---\n"
    templates_section += "\n💡 **使用小贴士**：\n"
    templates_section += "- 这些话术资源是参考，要灵活运用哦～\n"
    templates_section += "- 不要生硬套用，要结合具体场景调整\n"
    templates_section += "- 让每篇文案都有自己的温度和个性！\n"

    return base_prompt + templates_section

def build_agent(ctx=None):
    workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
    config_path = os.path.join(workspace_path, LLM_CONFIG)

    # 加载配置
    with open(config_path, 'r', encoding='utf-8') as f:
        cfg = json.load(f)

    # 加载话术资源库
    templates = load_templates()

    # 增强system prompt
    enhanced_prompt = enhance_system_prompt(cfg.get("sp", ""), templates)

    api_key = os.getenv("COZE_WORKLOAD_IDENTITY_API_KEY")
    base_url = os.getenv("COZE_INTEGRATION_MODEL_BASE_URL")

    llm = ChatOpenAI(
        model=cfg['config'].get("model"),
        api_key=api_key,
        base_url=base_url,
        temperature=cfg['config'].get('temperature', 0.7),
        streaming=True,
        timeout=cfg['config'].get('timeout', 600),
        extra_body={
            "thinking": {
                "type": cfg['config'].get('thinking', 'disabled')
            }
        },
        default_headers=default_headers(ctx) if ctx else {}
    )

    return create_agent(
        model=llm,
        system_prompt=enhanced_prompt,
        tools=[generate_post_image, generate_post_images],
        checkpointer=get_memory_saver(),
        state_schema=AgentState,
    )
