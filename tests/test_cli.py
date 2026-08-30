from __future__ import annotations

from pathlib import Path

import pytest

from qe_fde.cli import build_parser, run

ROOT = Path(__file__).parents[1]


def _run(tmp_path: Path, *arguments: str) -> int:
    parser = build_parser()
    args = parser.parse_args(
        [
            "--curriculum",
            str(ROOT / "curriculum.json"),
            "--progress",
            str(tmp_path / "progress.json"),
            *arguments,
        ]
    )
    return run(args)


def test_overview_list_and_next(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert _run(tmp_path, "overview") == 0
    assert "0/24" in capsys.readouterr().out

    assert _run(tmp_path, "list", "--stage", "foundation") == 0
    listed = capsys.readouterr().out
    assert "Python for builders" in listed
    assert "Docker" not in listed

    assert _run(tmp_path, "next") == 0
    assert "Week 01" in capsys.readouterr().out


def test_start_complete_status_and_reset(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert _run(tmp_path, "start", "1") == 0
    assert "Started Week 1" in capsys.readouterr().out

    assert _run(tmp_path, "complete", "1", "--evidence", "PR #1") == 0
    assert "Completed Week 1" in capsys.readouterr().out

    assert _run(tmp_path, "start", "2") == 0
    assert _run(tmp_path, "status") == 0
    output = capsys.readouterr().out
    assert "PR #1" in output
    assert "▶ Week 02" in output

    assert _run(tmp_path, "reset") == 2
    assert "not reset" in capsys.readouterr().err
    assert _run(tmp_path, "reset", "--yes") == 0
    assert "reset" in capsys.readouterr().out


def test_cli_rejects_unknown_stage_and_week(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="unknown stage"):
        _run(tmp_path, "list", "--stage", "missing")
    with pytest.raises(ValueError, match="between 1 and 24"):
        _run(tmp_path, "start", "25")
