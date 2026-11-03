#!/usr/bin/env python3
"""Lint the bundle: frontmatter, description length, cross-references, script paths.

Usage: python3 scripts/check_skills.py     (exit 1 on any problem)
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DESC_MAX = 500
FRONT = re.compile(r"^---\n(.*?)\n---\n", re.S)
REF = re.compile(r"`((?:\.\./\.\./)?references/[\w./-]+\.md)`")
SCRIPT = re.compile(r"scripts/([\w-]+\.py)")
SKILL_REF = re.compile(r"`(youtube-[a-z-]+)`")


def frontmatter(text: str) -> dict:
    m = FRONT.match(text)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        k, _, v = line.partition(":")
        out[k.strip()] = v.strip().strip('"')
    return out


def main() -> int:
    problems: list[str] = []
    skills_dir = ROOT / "skills"
    names = {p.name for p in skills_dir.iterdir() if p.is_dir()}
    manifest = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
    announced = re.search(r"(\d+) ", manifest["description"])
    if announced and int(announced.group(1)) != len(names):
        problems.append(f"plugin.json announces {announced.group(1)} skills, found {len(names)}")

    docs = [ROOT / "SKILL.md"] + sorted(skills_dir.rglob("*.md"))
    for doc in docs:
        text = doc.read_text(encoding="utf-8")
        rel = doc.relative_to(ROOT)
        if doc.name == "SKILL.md":
            fm = frontmatter(text)
            if not fm.get("name") or not fm.get("description"):
                problems.append(f"{rel}: missing name/description frontmatter")
            if doc.parent != ROOT and fm.get("name") != doc.parent.name:
                problems.append(f"{rel}: name '{fm.get('name')}' != folder '{doc.parent.name}'")
            if len(fm.get("description", "")) > DESC_MAX:
                problems.append(f"{rel}: description {len(fm['description'])} chars > {DESC_MAX}")
            if "—" in fm.get("description", ""):
                problems.append(f"{rel}: em dash in description")
        base = doc.parent if doc.parent.name != "references" else doc.parent.parent
        for ref in REF.findall(text):
            if not (base / ref).resolve().is_file():
                problems.append(f"{rel}: broken reference {ref}")
        for script in SCRIPT.findall(text):
            if not (ROOT / "scripts" / script).is_file():
                problems.append(f"{rel}: missing script scripts/{script}")
        for skill in SKILL_REF.findall(text):
            if skill not in names and skill != "youtube-channel-skills":
                problems.append(f"{rel}: unknown skill `{skill}`")

    print("\n".join(problems) or f"OK: {len(names)} skills, {len(docs)} docs checked.")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
