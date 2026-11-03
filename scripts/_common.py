"""Shared bootstrap for scripts: puts the repo root on sys.path and offers small helpers."""
from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def load_json(path: str) -> dict:
    return json.loads(pathlib.Path(path).read_text(encoding="utf-8"))


def probe_duration(file_path: str | None) -> int | None:
    """Duration in seconds via ffprobe, or None if ffprobe/file is unavailable."""
    if not file_path or not pathlib.Path(file_path).is_file() or not shutil.which("ffprobe"):
        return None
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", file_path],
            capture_output=True, text=True, timeout=30, check=True,
        ).stdout.strip()
        return int(float(out))
    except (subprocess.SubprocessError, ValueError):
        return None


def die(message: str, code: int = 1) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(code)
