# API/main.py
import json
import argparse
from pathlib import Path
from API.agent import APIAgent
from shared.store import load_items, load_memory


def evaluate_assertions(assertions: list) -> list[dict]:
    results = []
    items = load_items()
    memory = load_memory()

    for assertion in assertions:
        a_type = assertion["type"]
        passed = False
        details = ""

        if a_type == "memory_key_exists":
            key = assertion["key"]
            passed = key in memory
            details = f"Memory key '{key}' exists: {passed}"

        elif a_type == "item_exists":
            title_part = assertion["title_contains"].lower()
            passed = any(title_part in item["title"].lower() for item in items)
            details = f"Item containing '{title_part}' exists: {passed}"

        elif a_type == "min_items_count":
            min_c = assertion["count"]
            passed = len(items) >= min_c
            details = f"Items count {len(items)} >= {min_c}: {passed}"

        results.append({"assertion": assertion, "passed": passed, "details": details})
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", default="scenario.json")
    parser.add_argument("--out", default="results/api.json")
    args = parser.parse_args()

    scenario_path = Path(args.scenario)
    if not scenario_path.exists():
        print(f"Error: Scenario file {scenario_path} not found.")
        return

    scenario = json.loads(scenario_path.read_text(encoding="utf-8"))

    all_turns_data = []
    total_tokens_all = {"input_tokens": 0, "output_tokens": 0, "cache_read_tokens": 0, "cache_write_tokens": 0,
                        "total_cost_usd": 0.0}

    # איפוס נתונים קודמים או סשנים חדשים
    for session_def in scenario["sessions"]:
        session_id = session_def["session_id"]
        agent = APIAgent(session_id=session_id)

        for turn_idx, turn_text in enumerate(session_def["turns"]):
            print(f"\n--- [API/main.py] Session {session_id}, Turn {turn_idx + 1} ---")
            answer, usage, tools_used = agent.run_turn(turn_text)

            # צבירת טוקנים
            for k in total_tokens_all:
                if k == "total_cost_usd":
                    total_tokens_all[k] += usage[k]
                else:
                    total_tokens_all[k] += usage[k]

            all_turns_data.append({
                "session_id": session_id,
                "turn": turn_text,
                "answer": answer,
                "tools_used": tools_used,
                "usage": usage
            })

    # בדיקות אוטומטיות (assertions)
    assertion_results = evaluate_assertions(scenario.get("assertions", []))
    passed_tests = all(a["passed"] for a in assertion_results)

    output_data = {
        "framework": "API",
        "total_usage": total_tokens_all,
        "turns": all_turns_data,
        "assertions": assertion_results,
        "all_passed": passed_tests
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n[API/main.py] Finished successfully! Results saved to {out_path}")


if __name__ == "__main__":
    main()