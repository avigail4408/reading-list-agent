# API/harness/memory.py
from shared.store import load_memory

def get_relevant_memory(query: str) -> str:
    print(f"[memory.py] Fetching relevant memory for query...")
    mem = load_memory()
    if not mem:
        return "No saved preferences."
    formatted = "\n".join(f"- {k}: {v}" for k, v in mem.items())
    return f"User Persistent Memory:\n{formatted}"