# API/harness/tools.py
from shared.domain_tools import (
    add_reading_item,
    list_reading_items,
    update_preference,
    fetch_topic_summary
)

TOOLS_SCHEMA = [
    {
        "name": "add_reading_item",
        "description": "Add an item to the reading list.",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "category": {"type": "string"},
                "priority": {"type": "string", "enum": ["low", "medium", "high"]}
            },
            "required": ["title", "category"]
        }
    },
    {
        "name": "list_reading_items",
        "description": "List filtered reading items.",
        "input_schema": {
            "type": "object",
            "properties": {
                "status": {"type": "string"},
                "category": {"type": "string"}
            }
        }
    },
    {
        "name": "update_preference",
        "description": "Save user preference to memory.",
        "input_schema": {
            "type": "object",
            "properties": {
                "key": {"type": "string"},
                "value": {"type": "string"}
            },
            "required": ["key", "value"]
        }
    },
    {
        "name": "fetch_topic_summary",
        "description": "Fetch short summary from Wikipedia API.",
        "input_schema": {
            "type": "object",
            "properties": {
                "topic": {"type": "string"}
            },
            "required": ["topic"]
        }
    }
]

def dispatch_tool(name: str, args: dict) -> tuple[str, bool]:
    print(f"[tools.py] Dispatching tool '{name}' with args {args}")
    try:
        if name == "add_reading_item":
            return add_reading_item(**args), False
        elif name == "list_reading_items":
            return list_reading_items(**args), False
        elif name == "update_preference":
            return update_preference(**args), False
        elif name == "fetch_topic_summary":
            return fetch_topic_summary(**args), False
        else:
            return f"Unknown tool: {name}", True
    except Exception as e:
        return f"Tool error: {str(e)}", True