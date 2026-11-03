"""Approval gate.

Every write action (upload, metadata update, comment reply, moderation) runs in
two passes:

1. Dry run: the script prints an approval card that includes a fingerprint of
   the exact payload, and exits without touching YouTube.
2. Confirmed run: the script is re-run with ``--confirm <fingerprint>``. It
   recomputes the fingerprint and refuses to act if the payload changed.

So the user always approves the bytes that get published, not a summary of
them. The agent must never invent the fingerprint: it only ever copies it from
a dry-run card that the user has seen and approved.
"""
from __future__ import annotations

import hashlib
import json
from typing import Iterable

from .metadata import Issue


def fingerprint(payload: dict) -> str:
    blob = json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()[:12]


def verify_confirmation(payload: dict, confirm: str | None) -> bool:
    return bool(confirm) and confirm.strip().lower() == fingerprint(payload)


def render_approval_card(
    *,
    kind: str,
    payload: dict,
    target: str | None = None,
    issues: Iterable[Issue] = (),
    preview_fields: Iterable[str] = ("title", "description", "text"),
) -> str:
    fp = fingerprint(payload)
    issues = list(issues)
    lines = [f"## Ready for approval: {kind}", ""]
    if target:
        lines.append(f"**Target:** {target}")
    for field in preview_fields:
        value = payload.get(field)
        if not value:
            continue
        lines.append(f"**{field}** ({len(str(value))} chars):")
        for pl in str(value).splitlines() or [""]:
            lines.append(f"> {pl}")
        lines.append("")
    others = {k: v for k, v in payload.items() if k not in set(preview_fields)}
    if others:
        lines.append("**Other fields:**")
        for k, v in others.items():
            lines.append(f"- `{k}`: {json.dumps(v, ensure_ascii=False)}")
        lines.append("")
    if issues:
        lines.append("**Validation:**")
        lines.extend(f"- {i}" for i in issues)
        lines.append("")
    lines.append(f"**Fingerprint:** `{fp}`")
    lines.append("")
    if any(i.level == "error" for i in issues):
        lines.append("Fix the errors above before this can be published.")
    else:
        lines.append("Reply **yes** / **publica** to run it, or suggest edits.")
    return "\n".join(lines)
