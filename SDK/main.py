# SDK/main.py
import json
import argparse
import asyncio
from pathlib import Path
from claude_code_sdk import query
from SDK.agent import build_options
from API.main import evaluate_assertions  # משתמשים בבדיקות האסרטשן המשותפות


async def run_sdk_session(session_def):
    session_id = session_def["session_id"]
    options = build_options(session_id)

    last_answer = ""
    turns_data = []

    for turn_text in session_def["turns"]:
        print(f"\n--- [SDK/main.py] Session {session_id}, Turn: '{turn_text}' ---")
        response_stream = query(prompt=turn_text, options=options)

        content_text = ""
        async for message in response_stream:
            if hasattr(message, "content"):
                content_text = message.content
            print(f"[SDK message]: {type(message)}")

        last_answer = content_text
        turns_data.append({
            "session_id": session_id,
            "turn": turn_text,
            "answer": last_answer,
            "tools_used": [],
            "usage": {"input_tokens": 0, "output_tokens": 0, "cache_read_tokens": 0, "cache_write_tokens": 0,
                      "total_cost_usd": 0.0}
        })
    return turns_data


async def main_async():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", default="scenario.json")
    parser.add_argument("--out", default="results/sdk.json")
    args = parser.parse_args()

    scenario_path = Path(args.scenario)
    if not scenario_path.exists():
        print(f"Error: Scenario file {scenario_path} not found.")
        return

    scenario = json.loads(scenario_path.read_text(encoding="utf-8"))
    all_turns = []

    for session_def in scenario["sessions"]:
        turns_data = await run_sdk_session(session_def)
        all_turns.extend(turns_data)

    assertion_results = evaluate_assertions(scenario.get("assertions", []))
    passed_tests = all(a["passed"] for a in assertion_results)

    output_data = {
        "framework": "SDK",
        "total_usage": {"input_tokens": 0, "output_tokens": 0, "cache_read_tokens": 0, "cache_write_tokens": 0,
                        "total_cost_usd": 0.0},
        "turns": all_turns,
        "assertions": assertion_results,
        "all_passed": passed_tests
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n[SDK/main.py] Finished successfully! Results saved to {out_path}")


def main():
    asyncio.run(main_async())


if __name__ == "__main__":
    main()