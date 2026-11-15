# shared/domain_tools.py
import httpx
from shared.store import load_items, save_items, load_memory, save_memory

def add_reading_item(title: str, category: str, priority: str = "medium") -> str:
    items = load_items()
    item_id = len(items) + 1
    items.append({"id": item_id, "title": title, "category": category, "priority": priority, "status": "unread"})
    save_items(items)
    return f"Added #{item_id}: {title} [{category}, {priority}]"

def list_reading_items(status: str = "unread", category: str = "") -> str:
    items = load_items()
    filtered = [
        i for i in items
        if (not status or i["status"] == status) and (not category or i["category"] == category)
    ]
    if not filtered:
        return "No matching items."
    return "\n".join(f"#{i['id']} | {i['title']} | {i['category']} | {i['priority']}" for i in filtered)

def update_preference(key: str, value: str) -> str:
    mem = load_memory()
    mem[key] = value
    save_memory(mem)
    return f"Saved pref: {key}={value}"

def fetch_topic_summary(topic: str) -> str:
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic.replace(' ', '_')}"
    try:
        resp = httpx.get(url, timeout=5.0, headers={"User-Agent": "ReadingListAgent/1.0"})
        if resp.status_code != 200:
            return f"Error: Topic '{topic}' not found."
        extract = resp.json().get("extract", "")
        return extract[:250] + ("..." if len(extract) > 250 else "")
    except Exception as e:
        return f"External API error: {str(e)}"