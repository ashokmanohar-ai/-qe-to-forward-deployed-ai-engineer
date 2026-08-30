"""Small in-process metrics and traces for learning and tests."""

from __future__ import annotations

import threading
import time
from collections import defaultdict
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass


@dataclass(frozen=True)
class Span:
    trace_id: str
    name: str
    duration_seconds: float
    status: str
    attributes: dict[str, str]


class Observability:
    def __init__(self, *, max_spans: int = 1000) -> None:
        self.max_spans = max_spans
        self._counters: dict[tuple[str, tuple[tuple[str, str], ...]], int] = defaultdict(int)
        self._durations: dict[str, list[float]] = defaultdict(list)
        self._spans: list[Span] = []
        self._lock = threading.RLock()

    def increment(self, name: str, **labels: str) -> None:
        safe_labels = tuple(sorted((key, value) for key, value in labels.items()))
        with self._lock:
            self._counters[(name, safe_labels)] += 1

    def observe(self, name: str, value: float) -> None:
        with self._lock:
            values = self._durations[name]
            values.append(value)
            if len(values) > 10_000:
                del values[: len(values) - 10_000]

    @contextmanager
    def span(self, trace_id: str, name: str, **attributes: str) -> Iterator[None]:
        started = time.perf_counter()
        status = "ok"
        try:
            yield
        except BaseException:
            status = "error"
            raise
        finally:
            duration = time.perf_counter() - started
            span = Span(
                trace_id=trace_id,
                name=name,
                duration_seconds=duration,
                status=status,
                attributes=dict(attributes),
            )
            with self._lock:
                self._spans.append(span)
                if len(self._spans) > self.max_spans:
                    del self._spans[: len(self._spans) - self.max_spans]
            self.observe(f"{name}_duration_seconds", duration)

    def spans(self, trace_id: str | None = None) -> tuple[Span, ...]:
        with self._lock:
            if trace_id is None:
                return tuple(self._spans)
            return tuple(span for span in self._spans if span.trace_id == trace_id)

    def prometheus(self) -> str:
        lines: list[str] = []
        with self._lock:
            for (name, labels), value in sorted(self._counters.items()):
                label_text = ""
                if labels:
                    label_text = "{" + ",".join(f'{key}="{value}"' for key, value in labels) + "}"
                lines.append(f"{name}{label_text} {value}")
            for name, values in sorted(self._durations.items()):
                lines.append(f"{name}_count {len(values)}")
                lines.append(f"{name}_sum {sum(values):.6f}")
        return "\n".join(lines) + "\n"
