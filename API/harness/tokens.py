# API/harness/tokens.py

class TokenTracker:
    def __init__(self):
        self.total_input = 0
        self.total_output = 0
        self.cache_read = 0
        self.cache_write = 0
        self.total_cost = 0.0

    def record(self, usage):
        inp = getattr(usage, "input_tokens", 0)
        out = getattr(usage, "output_tokens", 0)
        c_read = getattr(usage, "cache_read_input_tokens", 0)
        c_write = getattr(usage, "cache_creation_input_tokens", 0)

        self.total_input += inp
        self.total_output += out
        self.cache_read += c_read
        self.cache_write += c_write

        # חישוב עלות משוערך למודלי Claude (לפי תעריפי Opus/Sonnet)
        cost = (inp * 15.0 + out * 75.0 + c_read * 1.5 + c_write * 18.75) / 1_000_000
        self.total_cost += cost
        print(f"[tokens.py] Usage recorded: +{inp} in, +{out} out. Cost so far: ${self.total_cost:.5f}")

    def get_summary(self):
        return {
            "input_tokens": self.total_input,
            "output_tokens": self.total_output,
            "cache_read_tokens": self.cache_read,
            "cache_write_tokens": self.cache_write,
            "total_cost_usd": round(self.total_cost, 5)
        }