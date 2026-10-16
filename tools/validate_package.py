#!/usr/bin/env python3
"""Validate installable metadata and local resource links, not scientific quality."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "paper-to-idea"
LINK = re.compile(r"(?<!!)\[[^\]\n]+\]\(([^)\n]+)\)")


def validate(root: Path = ROOT) -> tuple[list[str], list[str]]:
    root = root.resolve()
    skill = root / "skills" / "paper-to-idea"
    errors: list[str] = []
    checks: list[str] = []
    entry = skill / "SKILL.md"
    if not entry.is_file():
        return checks, ["Missing skills/paper-to-idea/SKILL.md"]
    content = entry.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---(?:\n|$)", content, re.S)
    meta = None
    try:
        meta = yaml.safe_load(match.group(1)) if match else None
    except yaml.YAMLError as exc:
        errors.append(f"Invalid SKILL.md YAML: {exc}")
    if not isinstance(meta, dict):
        errors.append("SKILL.md needs mapping YAML frontmatter")
    else:
        if meta.get("name") != skill.name:
            errors.append("Skill name must match its installation folder")
        description = meta.get("description")
        if not isinstance(description, str) or not 1 <= len(description) <= 1024:
            errors.append("Description must contain 1..1024 characters")
        elif "<" in description or ">" in description:
            errors.append("Description contains unsupported angle brackets")
    if "[TODO:" in content:
        errors.append("Unfinished initializer scaffold in SKILL.md")
    checks.append("skill frontmatter and installation name")

    ui_path = skill / "agents" / "openai.yaml"
    try:
        ui = yaml.safe_load(ui_path.read_text(encoding="utf-8"))
        interface = ui.get("interface", {}) if isinstance(ui, dict) else {}
        for key in ("display_name", "short_description", "default_prompt"):
            if not isinstance(interface.get(key), str) or not interface[key].strip():
                errors.append(f"Missing UI interface.{key}")
        short = interface.get("short_description", "")
        if not 25 <= len(short) <= 64:
            errors.append("UI short_description must be 25..64 characters")
        if "$paper-to-idea" not in interface.get("default_prompt", ""):
            errors.append("UI prompt must invoke $paper-to-idea")
    except (OSError, yaml.YAMLError) as exc:
        errors.append(f"Cannot read UI metadata: {exc}")
    checks.append("UI metadata and invocation prompt")

    template_dir = skill / "assets" / "templates"
    required_templates = {
        "paper-triage.md", "deep-reading.md", "research-gaps.md",
        "idea-candidates.md", "idea-evaluation.md", "experiment-plan.md",
        "literature-map.md",
    }
    for name in sorted(required_templates):
        if not (template_dir / name).is_file():
            errors.append(f"Missing output template: {name}")
    checks.append("seven public output templates")

    count = 0
    for document in sorted(root.rglob("*.md")):
        if any(part in {".git", ".venv", "dist", "__pycache__"} for part in document.relative_to(root).parts):
            continue
        for target in LINK.findall(document.read_text(encoding="utf-8")):
            target = target.strip().removeprefix("<").removesuffix(">")
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            destination = (document.parent / unquote(parsed.path)).resolve()
            count += 1
            if not destination.is_relative_to(root) or not destination.exists():
                errors.append(f"Broken or external local link in {document.relative_to(root)}: {target}")
            elif document.is_relative_to(skill) and not destination.is_relative_to(skill):
                errors.append(f"Installable Skill depends on repository-only file: {target}")
    checks.append(f"{count} local resource links and self-contained Skill paths")
    return checks, errors


def main() -> int:
    checks, errors = validate()
    if errors:
        for error in errors:
            print(f"FAIL {error}")
        return 1
    for check in checks:
        print(f"PASS {check}")
    print("Structural checks only; no scientific or independent behavioral certification.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
