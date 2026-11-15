# tests/test_offline.py
import pytest
from API.harness.compaction import compact_history
from API.harness.tokens import TokenTracker


def test_compaction_threshold():
    messages = [{"role": "user", "content": f"msg {i}"} for i in range(15)]
    compacted = compact_history(messages, threshold=10)
    assert len(compacted) < len(messages)
    assert compacted[0]["content"] == "msg 0"


def test_token_tracker():
    tracker = TokenTracker()

    class DummyUsage:
        input_tokens = 100
        output_tokens = 50
        cache_read_input_tokens = 200
        cache_creation_input_tokens = 10

    tracker.record(DummyUsage())
    summary = tracker.get_summary()
    assert summary["input_tokens"] == 100
    assert summary["output_tokens"] == 50
    assert summary["cache_read_tokens"] == 200
    assert summary["total_cost_usd"] > 0