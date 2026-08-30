from __future__ import annotations

from collections.abc import Iterator

import pytest

from qe_fde.ai_service.config import Settings
from qe_fde.ai_service.observability import Observability


def test_settings_load_and_validation(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FDE_API_KEY", "a-long-development-key")
    monkeypatch.setenv("FDE_ENVIRONMENT", "test")
    monkeypatch.setenv("FDE_MAX_DOCUMENTS", "50")
    monkeypatch.setenv("FDE_MAX_TOOL_STEPS", "2")
    settings = Settings.from_env()
    assert settings.environment == "test"
    assert settings.max_documents == 50
    assert settings.max_tool_steps == 2

    monkeypatch.setenv("FDE_API_KEY", "short")
    with pytest.raises(RuntimeError, match="at least 16"):
        Settings.from_env()


@pytest.mark.parametrize(
    ("key", "value", "message"),
    [
        ("FDE_ENVIRONMENT", "unknown", "development, test, or production"),
        ("FDE_MAX_DOCUMENTS", "nope", "numeric"),
        ("FDE_MAX_DOCUMENTS", "0", "between 1 and 100000"),
        ("FDE_MAX_TOOL_STEPS", "11", "between 1 and 10"),
    ],
)
def test_settings_reject_bad_values(
    monkeypatch: pytest.MonkeyPatch, key: str, value: str, message: str
) -> None:
    monkeypatch.setenv("FDE_API_KEY", "a-long-development-key")
    monkeypatch.setenv(key, value)
    with pytest.raises(RuntimeError, match=message):
        Settings.from_env()


def _failing_operation() -> Iterator[None]:
    yield


def test_observability_records_metrics_spans_and_errors() -> None:
    telemetry = Observability(max_spans=2)
    telemetry.increment("requests_total", status="ok")
    with telemetry.span("trace-1", "rag", tenant="demo"):
        pass
    with pytest.raises(RuntimeError), telemetry.span("trace-2", "tool"):
        raise RuntimeError("simulated")
    with telemetry.span("trace-3", "api"):
        pass

    # max_spans=2 evicts the oldest trace.
    assert telemetry.spans("trace-1") == ()
    assert telemetry.spans("trace-2")[0].status == "error"
    assert len(telemetry.spans()) == 2
    metrics = telemetry.prometheus()
    assert 'requests_total{status="ok"} 1' in metrics
    assert "rag_duration_seconds_count 1" in metrics
