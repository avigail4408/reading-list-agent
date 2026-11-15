# API/harness/context.py
from API.harness.memory import get_relevant_memory

def build_system_prompt(latest_query: str) -> list[dict]:
    print("[context.py] Building dynamic system prompt with memory")
    memory_snippet = get_relevant_memory(latest_query)
    system_text = (
        "You are an intelligent reading list assistant.\n"
        "Use tools to manage items and preferences.\n"
        f"{memory_snippet}\n"
        "Be concise."
    )
    return [{"type": "text", "text": system_text}]