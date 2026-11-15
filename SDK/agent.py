# SDK/agent.py
from claude_code_sdk import ClaudeSDKClient, ClaudeCodeOptions  # replaces: loop.py, tokens.py
from SDK.tools import mcp_server

def build_options(session_id: int) -> ClaudeCodeOptions:  # replaces: context.py, caching.py
    return ClaudeCodeOptions(
        model="claude-3-5-sonnet-20241022",
        system_prompt="You are a concise reading list assistant. Use tools to manage items and preferences.",  # replaces: context.py
        mcp_servers={"reading": mcp_server},  # replaces: tools.py
        allowed_tools=[  # replaces: context.py
            "mcp__reading__add_reading_item",
            "mcp__reading__list_reading_items",
            "mcp__reading__update_preference",
            "mcp__reading__fetch_topic_summary"
        ],
        strict_mcp_config=True,
        setting_sources=["project"],  # replaces: memory.py
        resume=str(session_id),  # replaces: history.py, compaction.py, caching.py
    )