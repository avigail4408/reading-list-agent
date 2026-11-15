# SDK/tools.py
from claude_code_sdk import tool, create_sdk_mcp_server  # replaces: tools.py
from shared.domain_tools import (
    add_reading_item,
    list_reading_items,
    update_preference,
    fetch_topic_summary
)

@tool("add_reading_item", "Add an item to the reading list.", {"title": str, "category": str, "priority": str})  # replaces: tools.py
async def sdk_add_item(args):
    return {"content": [{"type": "text", "text": add_reading_item(**args)}]}

@tool("list_reading_items", "List filtered reading items.", {"status": str, "category": str})  # replaces: tools.py
async def sdk_list_items(args):
    return {"content": [{"type": "text", "text": list_reading_items(**args)}]}

@tool("update_preference", "Save user preference to memory.", {"key": str, "value": str})  # replaces: tools.py
async def sdk_update_pref(args):
    return {"content": [{"type": "text", "text": update_preference(**args)}]}

@tool("fetch_topic_summary", "Fetch short summary from Wikipedia API.", {"topic": str})  # replaces: tools.py
async def sdk_fetch_topic(args):
    return {"content": [{"type": "text", "text": fetch_topic_summary(**args)}]}

mcp_server = create_sdk_mcp_server(  # replaces: tools.py
    name="reading_tools",
    tools=[sdk_add_item, sdk_list_items, sdk_update_pref, sdk_fetch_topic]
)