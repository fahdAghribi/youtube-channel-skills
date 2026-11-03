"""Minimal .env loader (no python-dotenv dependency).

Shell variables always win over .env values.
"""
from __future__ import annotations

import os
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONFIG_DIR = pathlib.Path(
    os.environ.get("YT_SKILLS_CONFIG_DIR", pathlib.Path.home() / ".config" / "youtube-channel-skills")
)


def load_env(path: pathlib.Path | None = None) -> None:
    env_file = path or ROOT / ".env"
    if not env_file.is_file():
        return
    for raw in env_file.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def get(name: str, default: str | None = None) -> str | None:
    load_env()
    value = os.environ.get(name, default)
    return value or default
