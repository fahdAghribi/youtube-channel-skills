#!/usr/bin/env python3
"""One-time OAuth consent for the channel you want to manage.

Usage: python3 scripts/auth.py [--client-secrets path/to/client_secret.json]

Opens a browser, asks you to pick the Google account / Brand Account that owns
the channel, and stores the token in ~/.config/youtube-channel-skills/token.json
(chmod 600, outside the repo).
"""
from __future__ import annotations

import argparse

import _common  # noqa: F401
from lib import _env
from lib.youtube_client import run_oauth_flow, ChannelClient


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--client-secrets", default=_env.get("YT_CLIENT_SECRETS"))
    args = ap.parse_args()
    if not args.client_secrets:
        _common.die("Set YT_CLIENT_SECRETS in .env or pass --client-secrets (OAuth client of type 'Desktop app').")
    path = run_oauth_flow(args.client_secrets)
    channel = ChannelClient().my_channel()
    title = channel.get("snippet", {}).get("title", "?")
    print(f"Token saved to {path}\nAuthorised channel: {title} ({channel.get('id', '?')})")


if __name__ == "__main__":
    main()
