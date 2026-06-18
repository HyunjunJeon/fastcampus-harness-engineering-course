from __future__ import annotations

import unittest

from gjc_rpc.protocol import (
    ContextUsage,
    parse_login_provider,
    parse_session_state,
    parse_unattended_accepted,
)


class TestContextUsage(unittest.TestCase):
    def test_session_state_parses_context_usage(self) -> None:
        state = parse_session_state(
            {
                "sessionId": "s1",
                "thinkingLevel": "high",
                "steeringMode": "all",
                "followUpMode": "all",
                "interruptMode": "wait",
                "contextUsage": {"tokens": 1234, "contextWindow": 200000, "percent": 0.6},
            }
        )
        self.assertIsInstance(state.context_usage, ContextUsage)
        assert state.context_usage is not None
        self.assertEqual(state.context_usage.tokens, 1234)
        self.assertEqual(state.context_usage.context_window, 200000)
        self.assertAlmostEqual(state.context_usage.percent, 0.6)

    def test_session_state_context_usage_absent(self) -> None:
        state = parse_session_state({"sessionId": "s1"})
        self.assertIsNone(state.context_usage)

    def test_session_state_context_usage_null_after_compaction(self) -> None:
        state = parse_session_state(
            {
                "sessionId": "s1",
                "contextUsage": {"tokens": None, "contextWindow": 200000, "percent": None},
            }
        )
        self.assertIsInstance(state.context_usage, ContextUsage)
        assert state.context_usage is not None
        self.assertIsNone(state.context_usage.tokens)
        self.assertEqual(state.context_usage.context_window, 200000)
        self.assertIsNone(state.context_usage.percent)


class TestUnattendedAccepted(unittest.TestCase):
    def test_parse(self) -> None:
        acc = parse_unattended_accepted(
            {
                "run_id": "r1",
                "actor": "hermes",
                "budget": {
                    "max_tokens": 100,
                    "max_tool_calls": 5,
                    "max_wall_time_ms": 1000,
                    "max_cost_usd": 2,
                },
                "scopes": ["prompt", "control"],
                "action_allowlist": ["command.prompt"],
                "accepted_at": "2026-01-01T00:00:00Z",
            }
        )
        self.assertEqual(acc.run_id, "r1")
        self.assertEqual(acc.actor, "hermes")
        self.assertEqual(acc.budget.max_tool_calls, 5)
        self.assertEqual(acc.scopes, ("prompt", "control"))
        self.assertEqual(acc.action_allowlist, ("command.prompt",))
        self.assertEqual(acc.accepted_at, "2026-01-01T00:00:00Z")


class TestLoginProvider(unittest.TestCase):
    def test_parse(self) -> None:
        provider = parse_login_provider(
            {"id": "anthropic", "name": "Anthropic", "available": True, "authenticated": False}
        )
        self.assertEqual(provider.id, "anthropic")
        self.assertEqual(provider.name, "Anthropic")
        self.assertTrue(provider.available)
        self.assertFalse(provider.authenticated)


if __name__ == "__main__":
    unittest.main()
