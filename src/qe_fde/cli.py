"""Dependency-free interactive command-line progress tracker."""

from __future__ import annotations

import argparse
import os
import sys
from datetime import UTC, datetime
from pathlib import Path

from qe_fde.progress import Curriculum, CurriculumError, PrerequisiteError, ProgressStore


def _find_curriculum(explicit: str | None) -> Path:
    if explicit:
        return Path(explicit).expanduser().resolve()
    environment_path = os.getenv("FDE_ROADMAP_FILE")
    if environment_path:
        return Path(environment_path).expanduser().resolve()
    current = Path.cwd().resolve()
    for candidate in (current, *current.parents):
        path = candidate / "curriculum.json"
        if path.exists():
            return path
    raise CurriculumError(
        "curriculum.json was not found; run from the repository or set FDE_ROADMAP_FILE"
    )


def _bar(done: int, total: int, width: int = 30) -> str:
    filled = round(width * done / total) if total else 0
    return "█" * filled + "░" * (width - filled)


def _status_symbol(store: ProgressStore, week: int) -> str:
    if store.is_complete(week):
        return "✓"
    if store.is_started(week):
        return "▶"
    return "·"


def _timestamp() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


def _print_module(curriculum: Curriculum, store: ProgressStore, week: int) -> None:
    module = curriculum.module(week)
    stage = curriculum.stage_names[module.stage]
    print(f"{_status_symbol(store, week)} Week {module.week:02d} · {stage} · {module.title}")
    print(f"  Outcome:   {module.outcome}")
    print(f"  Challenge: {module.challenge}")
    print(f"  Lab:       {module.lab}")
    print(f"  Evidence:  {module.evidence}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="fde-roadmap",
        description="Track evidence-based progress through the 24-week QE-to-FDE roadmap.",
    )
    parser.add_argument("--curriculum", help="Path to curriculum.json")
    parser.add_argument("--progress", default=".fde-progress.json", help="Local progress file")
    commands = parser.add_subparsers(dest="command", required=True)

    commands.add_parser("overview", help="Show stages and overall progress")
    list_parser = commands.add_parser("list", help="List modules")
    list_parser.add_argument("--stage", help="Stage ID, such as ai-engineering")
    commands.add_parser("next", help="Show the next incomplete module")
    start_parser = commands.add_parser("start", help="Mark a week started")
    start_parser.add_argument("week", type=int)
    complete_parser = commands.add_parser("complete", help="Complete a week with evidence")
    complete_parser.add_argument("week", type=int)
    complete_parser.add_argument("--evidence", required=True)
    commands.add_parser("status", help="Show progress and evidence")
    reset_parser = commands.add_parser("reset", help="Reset local progress")
    reset_parser.add_argument("--yes", action="store_true", help="Confirm reset")
    return parser


def run(args: argparse.Namespace) -> int:
    curriculum = Curriculum.load(_find_curriculum(args.curriculum))
    store = ProgressStore(Path(args.progress).expanduser().resolve())
    total = len(curriculum.modules)

    if args.command == "overview":
        done = sum(store.is_complete(module.week) for module in curriculum.modules)
        print("QE → Forward Deployed AI Engineer")
        print(f"[{_bar(done, total)}] {done}/{total} weeks ({done / total:.0%})")
        for stage_id, stage_name in curriculum.stage_names.items():
            modules = [module for module in curriculum.modules if module.stage == stage_id]
            stage_done = sum(store.is_complete(module.week) for module in modules)
            print(f"  {stage_name:<30} {stage_done}/{len(modules)}")
        return 0

    if args.command == "list":
        if args.stage and args.stage not in curriculum.stage_names:
            valid = ", ".join(curriculum.stage_names)
            raise ValueError(f"unknown stage {args.stage!r}; choose one of: {valid}")
        for module in curriculum.modules:
            if not args.stage or module.stage == args.stage:
                print(
                    f"{_status_symbol(store, module.week)} {module.week:02d} "
                    f"{curriculum.stage_names[module.stage]} — {module.title}"
                )
        return 0

    if args.command == "next":
        week = store.next_week(total)
        if week is None:
            print("All modules complete. Prepare your capstone defense.")
        else:
            _print_module(curriculum, store, week)
        return 0

    if args.command == "start":
        curriculum.module(args.week)
        store.start(args.week, _timestamp())
        print(f"Started Week {args.week}: {curriculum.module(args.week).title}")
        return 0

    if args.command == "complete":
        curriculum.module(args.week)
        store.complete(args.week, args.evidence, _timestamp())
        print(f"Completed Week {args.week} with evidence: {args.evidence.strip()}")
        return 0

    if args.command == "status":
        done = sum(store.is_complete(module.week) for module in curriculum.modules)
        print(f"[{_bar(done, total)}] {done}/{total}")
        for module in curriculum.modules:
            completion = store.completion(module.week)
            line = f"{_status_symbol(store, module.week)} Week {module.week:02d}: {module.title}"
            if completion:
                line += f" — {completion.evidence}"
            print(line)
        return 0

    if args.command == "reset":
        if not args.yes:
            print("Progress was not reset. Re-run with --yes to confirm.", file=sys.stderr)
            return 2
        store.reset()
        print("Local progress reset.")
        return 0

    raise ValueError(f"unsupported command: {args.command}")


def main() -> None:
    parser = build_parser()
    try:
        code = run(parser.parse_args())
    except (CurriculumError, PrerequisiteError, ValueError) as exc:
        parser.exit(2, f"error: {exc}\n")
    raise SystemExit(code)


if __name__ == "__main__":
    main()
