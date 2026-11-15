# API/harness/loop.py
from API.harness.tools import dispatch_tool

def run_agent_loop(client, model, system_blocks, tools_schema, messages, token_tracker):
    print("[loop.py] Starting agent loop execution")
    calls = 0
    tools_used = []
    while True:
        calls += 1
        response = client.messages.create(
            model=model,
            max_tokens=1024,
            system=system_blocks,
            tools=tools_schema,
            messages=messages,
        )
        token_tracker.record(response.usage)
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason != "tool_use":
            final_text = "".join(b.text for b in response.content if hasattr(b, "text") and b.text)
            print(f"[loop.py] Loop finished in {calls} calls.")
            return final_text, calls, tools_used

        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                tools_used.append(block.name)
                result_text, is_err = dispatch_tool(block.name, block.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result_text,
                    "is_error": is_err
                })
        messages.append({"role": "user", "content": tool_results})