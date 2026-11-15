# shared/store.py
import json
from pathlib import Path

DATA_DIR = Path("state_data")
ITEMS_FILE = DATA_DIR / "reading_list.json"
MEMORY_FILE = DATA_DIR / "preferences.json"

def init_store():
    DATA_DIR.mkdir(exist_ok=True)
    if not ITEMS_FILE.exists():
        ITEMS_FILE.write_text("[]", encoding="utf-8")
    if not MEMORY_FILE.exists():
        MEMORY_FILE.write_text("{}", encoding="utf-8")

def load_items() -> list[dict]:
    init_store()
    return json.loads(ITEMS_FILE.read_text(encoding="utf-8"))

def save_items(items: list[dict]):
    init_store()
    ITEMS_FILE.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")

def load_memory() -> dict:
    init_store()
    return json.loads(MEMORY_FILE.read_text(encoding="utf-8"))

def save_memory(mem: dict):
    init_store()
    MEMORY_FILE.write_text(json.dumps(mem, ensure_ascii=False, indent=2), encoding="utf-8")