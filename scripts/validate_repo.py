#!/usr/bin/env python3
"""Validate curriculum structure, required artifacts, and local Markdown links."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)\s]+)(?:\s+[^)]*)?\)")
REQUIRED = (
    "README.md",
    "ROADMAP.md",
    "curriculum.json",
    "pyproject.toml",
    "Dockerfile",
    "docker-compose.yml",
    "mkdocs.yml",
    "SECURITY.md",
    "docs/interview/roadmap.md",
    "docs/scenarios/customer-scenarios.md",
    "projects/08-customer-capstone/README.md",
    "infra/kubernetes/deployment.yaml",
    "infra/terraform/main.tf",
    ".github/workflows/quality.yml",
)


def validate_curriculum(errors: list[str]) -> None:
    path = ROOT / "curriculum.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"curriculum.json is unreadable: {exc}")
        return
    modules = data.get("modules", [])
    stages = data.get("stages", [])
    weeks = [module.get("week") for module in modules if isinstance(module, dict)]
    if weeks != list(range(1, 25)):
        errors.append(f"curriculum weeks must be 1..24, got {weeks}")
    stage_ids = {stage.get("id") for stage in stages if isinstance(stage, dict)}
    if len(stage_ids) != 5:
        errors.append(f"curriculum must have five unique stages, got {stage_ids}")
    required_module_fields = {
        "week",
        "stage",
        "title",
        "outcome",
        "lab",
        "challenge",
        "evidence",
        "skills",
        "hours",
    }
    for module in modules:
        if not isinstance(module, dict):
            errors.append(f"module is not an object: {module!r}")
            continue
        missing = required_module_fields - module.keys()
        if missing:
            errors.append(f"Week {module.get('week')} missing fields: {sorted(missing)}")
        if module.get("stage") not in stage_ids:
            errors.append(f"Week {module.get('week')} has unknown stage {module.get('stage')}")


def validate_required_files(errors: list[str]) -> None:
    for relative in REQUIRED:
        if not (ROOT / relative).exists():
            errors.append(f"required artifact missing: {relative}")


def validate_markdown_links(errors: list[str]) -> None:
    for markdown in sorted(ROOT.rglob("*.md")):
        if any(part.startswith(".") and part not in {".github"} for part in markdown.parts):
            continue
        text = markdown.read_text(encoding="utf-8")
        for raw_target in MARKDOWN_LINK.findall(text):
            target = unquote(raw_target.strip("<>"))
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            relative_target = target.split("#", 1)[0]
            if not relative_target:
                continue
            resolved = (markdown.parent / relative_target).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                errors.append(f"{markdown.relative_to(ROOT)} links outside repository: {target}")
                continue
            if not resolved.exists():
                errors.append(f"{markdown.relative_to(ROOT)} has broken link: {target}")


def main() -> int:
    errors: list[str] = []
    validate_required_files(errors)
    validate_curriculum(errors)
    validate_markdown_links(errors)
    if errors:
        print("Repository validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Repository validation passed: structure, curriculum, and local links are valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
