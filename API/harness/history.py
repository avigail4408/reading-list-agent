# API/harness/history.py
import json
from pathlib import Path

SESSION_DIR = Path("state_data/sessions")

def save_session_history(session_id: int, messages: list[dict]):
    SESSION_DIR.mkdir(parents=True, exist_ok=True)
    file_path = SESSION_DIR / f"session_{session_id}.jsonl"
    print(f"[history.py] Saving session history append-only to {file_path}")
    with open(file_path, "w", encoding="utf-8") as f:
        for m in messages:
            f.write(json.dumps(m, ensure_ascii=False) + "\n")

def load_session_history(session_id: int) -> list[dict]:
    file_path = SESSION_DIR / f"session_{session_id}.jsonl"
    if not file_path.exists():
        print(f"[history.py] No history found for session {session_id}")
        return []
    print(f"[history.py] Loading history for session {session_id}")
    messages = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                messages.append(json.loads(line))
    return messages