"""One possible solution for Lab 1."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Any, Protocol


class AdapterError(RuntimeError):
    """Base error for the customer adapter."""


class CustomerNotFound(AdapterError):
    """The requested customer does not exist."""


class PermanentUpstreamError(AdapterError):
    """The upstream rejected a request that should not be retried."""


class TransientUpstreamError(AdapterError):
    """The upstream remained unavailable after bounded retries."""


@dataclass(frozen=True)
class Response:
    status_code: int
    payload: Mapping[str, Any]


@dataclass(frozen=True)
class Customer:
    customer_id: str
    display_name: str


class Transport(Protocol):
    def get(self, path: str, *, timeout_seconds: float) -> Response: ...


def _parse_customer(payload: Mapping[str, Any]) -> Customer:
    raw = payload.get("customer")
    if not isinstance(raw, Mapping):
        raise PermanentUpstreamError("upstream response has no customer object")
    customer_id = raw.get("id")
    display_name = raw.get("display_name")
    if not isinstance(customer_id, str) or not isinstance(display_name, str):
        raise PermanentUpstreamError("upstream customer fields are invalid")
    return Customer(customer_id=customer_id, display_name=display_name)


def get_customer(
    transport: Transport,
    customer_id: str,
    *,
    attempts: int = 3,
    timeout_seconds: float = 2.0,
    on_attempt: Callable[[int, int], None] = lambda _attempt, _status: None,
) -> Customer:
    if not customer_id or "/" in customer_id:
        raise ValueError("customer_id must be a non-empty path-safe value")
    if attempts < 1:
        raise ValueError("attempts must be at least one")

    last_status: int | None = None
    for attempt in range(1, attempts + 1):
        response = transport.get(f"/customers/{customer_id}", timeout_seconds=timeout_seconds)
        last_status = response.status_code
        on_attempt(attempt, response.status_code)

        if response.status_code == 200:
            return _parse_customer(response.payload)
        if response.status_code == 404:
            raise CustomerNotFound(f"customer {customer_id!r} was not found")
        if response.status_code not in {408, 429, 500, 502, 503, 504}:
            raise PermanentUpstreamError(
                f"upstream returned terminal status {response.status_code}"
            )

    raise TransientUpstreamError(
        f"upstream unavailable after {attempts} attempts; last status={last_status}"
    )
