# API/harness/compaction.py

def compact_history(messages: list[dict], threshold: int = 10) -> list[dict]:
    print(f"[compaction.py] Checking history length: {len(messages)} messages (threshold: {threshold})")
    if len(messages) <= threshold:
        return messages

    head = messages[:2]
    tail = messages[-4:]
    summary_message = {
        "role": "user",
        "content": [
            {"type": "text", "text": "[Compacted History Summary]: Previous turns on reading preferences and items."}]
    }
    print("[compaction.py] History compacted.")
    return head + [summary_message] + tail