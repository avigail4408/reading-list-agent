# API/harness/caching.py

def apply_caching(system_blocks: list, tools_schema: list) -> tuple[list, list]:
    print("[caching.py] Applying cache_control ephemeral to system and tools")

    cached_system = []
    for block in system_blocks:
        if isinstance(block, str):
            cached_system.append({
                "type": "text",
                "text": block,
                "cache_control": {"type": "ephemeral"}
            })
        elif isinstance(block, dict):
            block["cache_control"] = {"type": "ephemeral"}
            cached_system.append(block)

    cached_tools = []
    for i, tool in enumerate(tools_schema):
        t_copy = tool.copy()
        if i == len(tools_schema) - 1:
            t_copy["cache_control"] = {"type": "ephemeral"}
        cached_tools.append(t_copy)

    return cached_system, cached_tools