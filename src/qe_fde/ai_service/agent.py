"""Bounded, typed tool workflow with confirmation and idempotency."""

from __future__ import annotations

import hashlib
import json
import threading
from dataclasses import dataclass
from typing import Protocol


class ToolError(ValueError):
    """A tool request is invalid or failed safely."""


class UnsafeToolCall(ToolError):
    """A tool request violates an authorization or side-effect boundary."""


@dataclass(frozen=True)
class ExecutionContext:
    tenant_id: str
    user_id: str
    approved_tools: frozenset[str] = frozenset()
    idempotency_key: str | None = None


class ToolHandler(Protocol):
    def __call__(
        self, arguments: dict[str, object], context: ExecutionContext
    ) -> dict[str, object]: ...


@dataclass(frozen=True)
class ToolSpec:
    name: str
    description: str
    handler: ToolHandler
    read_only: bool = True
    requires_confirmation: bool = False


@dataclass(frozen=True)
class ToolCall:
    name: str
    arguments: dict[str, object]


@dataclass(frozen=True)
class ToolResult:
    name: str
    output: dict[str, object]


@dataclass(frozen=True)
class _IdempotencyRecord:
    request_hash: str
    output: dict[str, object]


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolSpec] = {}
        self._records: dict[tuple[str, str, str], _IdempotencyRecord] = {}
        self._lock = threading.RLock()

    def register(self, spec: ToolSpec) -> None:
        if not spec.name or not spec.name.replace("_", "").isalnum():
            raise ValueError("tool name must contain letters, numbers, or underscores")
        if spec.name in self._tools:
            raise ValueError(f"tool {spec.name!r} is already registered")
        self._tools[spec.name] = spec

    def names(self) -> tuple[str, ...]:
        return tuple(sorted(self._tools))

    @staticmethod
    def _request_hash(arguments: dict[str, object]) -> str:
        try:
            encoded = json.dumps(arguments, sort_keys=True, separators=(",", ":"))
        except (TypeError, ValueError) as exc:
            raise ToolError("tool arguments must be JSON serializable") from exc
        if len(encoded) > 4096:
            raise ToolError("tool arguments exceed the local demo limit")
        return hashlib.sha256(encoded.encode("utf-8")).hexdigest()

    def execute(
        self, name: str, arguments: dict[str, object], context: ExecutionContext
    ) -> dict[str, object]:
        spec = self._tools.get(name)
        if spec is None:
            raise UnsafeToolCall(f"tool {name!r} is not allowlisted")
        if not context.tenant_id or not context.user_id:
            raise UnsafeToolCall("tool execution requires tenant and user identity")
        if spec.requires_confirmation and name not in context.approved_tools:
            raise UnsafeToolCall(f"tool {name!r} requires explicit confirmation")

        request_hash = self._request_hash(arguments)
        record_key: tuple[str, str, str] | None = None
        if not spec.read_only:
            if not context.idempotency_key:
                raise UnsafeToolCall(f"side-effecting tool {name!r} requires an idempotency key")
            record_key = (context.tenant_id, name, context.idempotency_key)

        with self._lock:
            if record_key is not None and record_key in self._records:
                record = self._records[record_key]
                if record.request_hash != request_hash:
                    raise UnsafeToolCall("idempotency key was reused with different arguments")
                return {**record.output, "replayed": True}

            output = spec.handler(arguments, context)
            if not isinstance(output, dict):
                raise ToolError(f"tool {name!r} returned an invalid output")
            if record_key is not None:
                self._records[record_key] = _IdempotencyRecord(
                    request_hash=request_hash, output=dict(output)
                )
            return dict(output)


class AgentWorkflow:
    """Executes a validated plan; it never recursively trusts tool output."""

    def __init__(self, registry: ToolRegistry, *, max_steps: int = 3) -> None:
        if not 1 <= max_steps <= 10:
            raise ValueError("max_steps must be between 1 and 10")
        self.registry = registry
        self.max_steps = max_steps

    def run(self, calls: list[ToolCall], context: ExecutionContext) -> tuple[ToolResult, ...]:
        if len(calls) > self.max_steps:
            raise UnsafeToolCall(
                f"plan has {len(calls)} steps, exceeding the limit of {self.max_steps}"
            )
        results: list[ToolResult] = []
        for call in calls:
            output = self.registry.execute(call.name, call.arguments, context)
            results.append(ToolResult(name=call.name, output=output))
        return tuple(results)
