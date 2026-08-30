"""Curriculum loading and local progress persistence."""

from __future__ import annotations

import json
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any


class CurriculumError(ValueError):
    """The machine-readable roadmap is invalid."""


class PrerequisiteError(ValueError):
    """A learner attempted a module before its prerequisite."""


@dataclass(frozen=True)
class Module:
    week: int
    stage: str
    title: str
    outcome: str
    lab: str
    challenge: str
    evidence: str
    skills: tuple[str, ...]
    hours: int

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> Module:
        try:
            return cls(
                week=int(value["week"]),
                stage=str(value["stage"]),
                title=str(value["title"]),
                outcome=str(value["outcome"]),
                lab=str(value["lab"]),
                challenge=str(value["challenge"]),
                evidence=str(value["evidence"]),
                skills=tuple(str(skill) for skill in value["skills"]),
                hours=int(value["hours"]),
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise CurriculumError(f"invalid module: {value!r}") from exc


@dataclass(frozen=True)
class Curriculum:
    modules: tuple[Module, ...]
    stage_names: dict[str, str]

    @classmethod
    def load(cls, path: Path) -> Curriculum:
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise CurriculumError(f"cannot read curriculum from {path}") from exc
        if not isinstance(raw, dict):
            raise CurriculumError("curriculum root must be an object")
        modules_raw = raw.get("modules")
        stages_raw = raw.get("stages")
        if not isinstance(modules_raw, list) or not isinstance(stages_raw, list):
            raise CurriculumError("curriculum must contain stage and module lists")
        modules = tuple(Module.from_dict(item) for item in modules_raw if isinstance(item, dict))
        expected_weeks = list(range(1, len(modules) + 1))
        actual_weeks = [module.week for module in modules]
        if actual_weeks != expected_weeks:
            raise CurriculumError(
                f"module weeks must be consecutive; expected {expected_weeks}, got {actual_weeks}"
            )
        stage_names: dict[str, str] = {}
        for stage in stages_raw:
            if not isinstance(stage, dict) or "id" not in stage or "name" not in stage:
                raise CurriculumError(f"invalid stage: {stage!r}")
            stage_names[str(stage["id"])] = str(stage["name"])
        unknown = {module.stage for module in modules} - stage_names.keys()
        if unknown:
            raise CurriculumError(f"modules reference unknown stages: {sorted(unknown)}")
        return cls(modules=modules, stage_names=stage_names)

    def module(self, week: int) -> Module:
        if week < 1 or week > len(self.modules):
            raise ValueError(f"week must be between 1 and {len(self.modules)}")
        return self.modules[week - 1]


@dataclass(frozen=True)
class Completion:
    evidence: str
    completed_at: str


class ProgressStore:
    """Atomic, local-only progress store."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self._data = self._load()

    def _load(self) -> dict[str, Any]:
        if not self.path.exists():
            return {"started": {}, "completed": {}}
        try:
            value = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise CurriculumError(f"progress file is unreadable: {self.path}") from exc
        if not isinstance(value, dict):
            raise CurriculumError("progress file root must be an object")
        value.setdefault("started", {})
        value.setdefault("completed", {})
        if not isinstance(value["started"], dict) or not isinstance(value["completed"], dict):
            raise CurriculumError("progress started/completed values must be objects")
        return value

    def _save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(self._data, indent=2, sort_keys=True) + "\n"
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=f".{self.path.name}.", dir=self.path.parent, text=True
        )
        try:
            with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
                handle.write(payload)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary_name, self.path)
        except BaseException:
            Path(temporary_name).unlink(missing_ok=True)
            raise

    def _require_previous(self, week: int) -> None:
        if week > 1 and not self.is_complete(week - 1):
            raise PrerequisiteError(f"complete Week {week - 1} before starting Week {week}")

    def start(self, week: int, timestamp: str) -> None:
        self._require_previous(week)
        self._data["started"].setdefault(str(week), timestamp)
        self._save()

    def complete(self, week: int, evidence: str, timestamp: str) -> None:
        self._require_previous(week)
        clean_evidence = evidence.strip()
        if not clean_evidence:
            raise ValueError("evidence must not be empty")
        self._data["started"].setdefault(str(week), timestamp)
        self._data["completed"][str(week)] = {
            "completed_at": timestamp,
            "evidence": clean_evidence,
        }
        self._save()

    def is_started(self, week: int) -> bool:
        return str(week) in self._data["started"]

    def is_complete(self, week: int) -> bool:
        return str(week) in self._data["completed"]

    def completion(self, week: int) -> Completion | None:
        raw = self._data["completed"].get(str(week))
        if not isinstance(raw, dict):
            return None
        return Completion(
            evidence=str(raw.get("evidence", "")),
            completed_at=str(raw.get("completed_at", "")),
        )

    def next_week(self, total_weeks: int) -> int | None:
        for week in range(1, total_weeks + 1):
            if not self.is_complete(week):
                return week
        return None

    def reset(self) -> None:
        self._data = {"started": {}, "completed": {}}
        self._save()
