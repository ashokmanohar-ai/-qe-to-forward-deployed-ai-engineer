from __future__ import annotations

import pytest

from qe_fde.ai_service.agent import (
    AgentWorkflow,
    ExecutionContext,
    ToolCall,
    ToolRegistry,
    ToolSpec,
    UnsafeToolCall,
)


def _registry() -> ToolRegistry:
    registry = ToolRegistry()

    def lookup(arguments: dict[str, object], context: ExecutionContext) -> dict[str, object]:
        return {"tenant": context.tenant_id, "value": arguments.get("value")}

    def create(arguments: dict[str, object], context: ExecutionContext) -> dict[str, object]:
        return {"created": True, "value": arguments.get("value")}

    registry.register(ToolSpec(name="lookup", description="lookup", handler=lookup))
    registry.register(
        ToolSpec(
            name="create",
            description="create",
            handler=create,
            read_only=False,
            requires_confirmation=True,
        )
    )
    return registry


def test_unknown_tool_is_denied() -> None:
    registry = _registry()
    with pytest.raises(UnsafeToolCall, match="allowlisted"):
        registry.execute(
            "delete_everything",
            {},
            ExecutionContext(tenant_id="demo", user_id="u1"),
        )


def test_side_effect_requires_confirmation_and_idempotency() -> None:
    registry = _registry()
    unapproved = ExecutionContext(tenant_id="demo", user_id="u1")
    with pytest.raises(UnsafeToolCall, match="confirmation"):
        registry.execute("create", {"value": "x"}, unapproved)

    approved_without_key = ExecutionContext(
        tenant_id="demo", user_id="u1", approved_tools=frozenset({"create"})
    )
    with pytest.raises(UnsafeToolCall, match="idempotency"):
        registry.execute("create", {"value": "x"}, approved_without_key)


def test_side_effect_replay_and_conflict() -> None:
    registry = _registry()
    context = ExecutionContext(
        tenant_id="demo",
        user_id="u1",
        approved_tools=frozenset({"create"}),
        idempotency_key="request-123",
    )
    first = registry.execute("create", {"value": "x"}, context)
    replay = registry.execute("create", {"value": "x"}, context)
    assert first["created"] is True
    assert replay["replayed"] is True
    with pytest.raises(UnsafeToolCall, match="different arguments"):
        registry.execute("create", {"value": "y"}, context)


def test_agent_enforces_step_budget() -> None:
    workflow = AgentWorkflow(_registry(), max_steps=1)
    calls = [ToolCall("lookup", {}), ToolCall("lookup", {})]
    with pytest.raises(UnsafeToolCall, match="exceeding"):
        workflow.run(calls, ExecutionContext(tenant_id="demo", user_id="u1"))
