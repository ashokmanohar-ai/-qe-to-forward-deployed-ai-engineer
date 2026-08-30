from __future__ import annotations

import json
from pathlib import Path

import pytest

from qe_fde.progress import Curriculum, CurriculumError, PrerequisiteError, ProgressStore

ROOT = Path(__file__).parents[1]


def test_curriculum_has_24_consecutive_weeks() -> None:
    curriculum = Curriculum.load(ROOT / "curriculum.json")
    assert [module.week for module in curriculum.modules] == list(range(1, 25))
    assert len(curriculum.stage_names) == 5


def test_progress_requires_previous_week_and_keeps_evidence(tmp_path: Path) -> None:
    store = ProgressStore(tmp_path / "progress.json")
    with pytest.raises(PrerequisiteError):
        store.start(2, "2026-01-01T00:00:00+00:00")

    store.complete(1, "PR #1", "2026-01-01T00:00:00+00:00")
    store.start(2, "2026-01-02T00:00:00+00:00")

    reloaded = ProgressStore(tmp_path / "progress.json")
    assert reloaded.is_complete(1)
    assert reloaded.is_started(2)
    assert reloaded.completion(1) is not None
    assert reloaded.completion(1).evidence == "PR #1"  # type: ignore[union-attr]


def test_progress_rejects_empty_evidence(tmp_path: Path) -> None:
    store = ProgressStore(tmp_path / "progress.json")
    with pytest.raises(ValueError, match="evidence"):
        store.complete(1, "  ", "2026-01-01T00:00:00+00:00")


def test_invalid_curriculum_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "curriculum.json"
    path.write_text(json.dumps({"stages": [], "modules": [{"week": 2}]}), encoding="utf-8")
    with pytest.raises(CurriculumError):
        Curriculum.load(path)
