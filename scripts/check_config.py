#!/usr/bin/env python3
"""Report which tier is available: 0 (draft only), 1 (research, API key), 2 (owner, OAuth).

Never prints secret values.
"""
from __future__ import annotations

import importlib.util

import _common  # noqa: F401
from lib import _env
from lib.youtube_client import TOKEN_PATH


def main() -> None:
    deps = all(importlib.util.find_spec(m) for m in ("googleapiclient", "google_auth_oauthlib"))
    api_key = bool(_env.get("YT_API_KEY"))
    secrets = _env.get("YT_CLIENT_SECRETS")
    token = TOKEN_PATH.is_file()

    print(f"google client libraries : {'ok' if deps else 'missing (pip install -r requirements.txt)'}")
    print(f"YT_API_KEY              : {'set' if api_key else 'not set'}")
    print(f"YT_CLIENT_SECRETS       : {'set' if secrets else 'not set'}")
    print(f"OAuth token             : {'present' if token else 'missing (python3 scripts/auth.py)'}")
    tier = 2 if (deps and token) else 1 if (deps and api_key) else 0
    labels = {
        0: "Tier 0: draft only. Every skill works; you paste results into YouTube Studio yourself.",
        1: "Tier 1: public research (outliers, competitor stats) via API key.",
        2: "Tier 2: owner mode. Upload, schedule, edit metadata, reply to comments, analytics.",
    }
    print(f"\n{labels[tier]}")


if __name__ == "__main__":
    main()
