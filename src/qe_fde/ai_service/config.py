"""Environment configuration with fail-fast production validation."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    api_key: str
    environment: str = "development"
    log_level: str = "INFO"
    max_documents: int = 1000
    max_tool_steps: int = 3

    @classmethod
    def from_env(cls) -> Settings:
        api_key = os.getenv("FDE_API_KEY", "")
        if len(api_key) < 16:
            raise RuntimeError("FDE_API_KEY must be configured with at least 16 characters")
        environment = os.getenv("FDE_ENVIRONMENT", "development").lower()
        if environment not in {"development", "test", "production"}:
            raise RuntimeError("FDE_ENVIRONMENT must be development, test, or production")
        try:
            max_documents = int(os.getenv("FDE_MAX_DOCUMENTS", "1000"))
            max_tool_steps = int(os.getenv("FDE_MAX_TOOL_STEPS", "3"))
        except ValueError as exc:
            raise RuntimeError("numeric FDE settings contain an invalid value") from exc
        if not 1 <= max_documents <= 100_000:
            raise RuntimeError("FDE_MAX_DOCUMENTS must be between 1 and 100000")
        if not 1 <= max_tool_steps <= 10:
            raise RuntimeError("FDE_MAX_TOOL_STEPS must be between 1 and 10")
        return cls(
            api_key=api_key,
            environment=environment,
            log_level=os.getenv("FDE_LOG_LEVEL", "INFO").upper(),
            max_documents=max_documents,
            max_tool_steps=max_tool_steps,
        )
