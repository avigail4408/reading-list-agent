# API/agent.py
import os
from anthropic import Anthropic
from API.harness.context import build_system_prompt
from API.harness.tools import TOOLS_SCHEMA
from API.harness.caching import apply_caching
from API.harness.compaction import compact_history
from API.harness.history import load_session_history, save_session_history
from API.harness.tokens import TokenTracker
from API.harness.loop import run_agent_loop


class APIAgent:
    def __init__(self, session_id: int, model: str = "claude-3-5-sonnet-20241022"):
        self.session_id = session_id
        self.model = model
        self.client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        self.token_tracker = TokenTracker()
        self.messages = load_session_history(session_id)

    def run_turn(self, user_query: str) -> tuple[str, dict, list]:
        print(f"[agent.py] Running turn for session {self.session_id} with query: '{user_query}'")

        # 1. הוספת הודעת המשתמש להיסטוריה
        self.messages.append({"role": "user", "content": user_query})

        # 2. דחיסת היסטוריה במידת הצורך (compaction)
        self.messages = compact_history(self.messages, threshold=12)

        # 3. בניית system prompt דינמי כולל זיכרון (context & memory)
        system_blocks = build_system_prompt(user_query)

        # 4. החלת Caching על הפרומפט והכלים
        cached_system, cached_tools = apply_caching(system_blocks, TOOLS_SCHEMA)

        # 5. הרצת לולאת הסוכן
        final_answer, calls, tools_used = run_agent_loop(
            client=self.client,
            model=self.model,
            system_blocks=cached_system,
            tools_schema=cached_tools,
            messages=self.messages,
            token_tracker=self.token_tracker
        )

        # 6. שמירת ההיסטוריה המעודכנת לדיסק (append-only)
        save_session_history(self.session_id, self.messages)

        return final_answer, self.token_tracker.get_summary(), tools_used