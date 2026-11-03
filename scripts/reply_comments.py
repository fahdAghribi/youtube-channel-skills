#!/usr/bin/env python3
"""Post approved replies and moderation actions in one batch.

Usage:
  python3 scripts/reply_comments.py actions.json                 # dry run, approval card
  python3 scripts/reply_comments.py actions.json --confirm FP    # executes

actions.json:
{
  "video_id": "abc123def45",
  "replies": [{"parent_id": "<thread or top-level comment id>", "text": "..."}],
  "moderation": [{"comment_id": "...", "status": "published|heldForReview|rejected", "ban_author": false}]
}

YouTube threads are 1 level deep: always reply to the TOP-LEVEL comment id,
even when answering someone inside the thread (mention them with @handle).
"""
from __future__ import annotations

import argparse
import json
import sys

import _common
from lib.approval import fingerprint, verify_confirmation

MAX_REPLY = 10000


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("actions")
    ap.add_argument("--confirm")
    args = ap.parse_args()

    actions = _common.load_json(args.actions)
    replies = actions.get("replies", [])
    moderation = actions.get("moderation", [])
    problems = [f"reply {i}: empty or longer than {MAX_REPLY} chars" for i, r in enumerate(replies) if not r.get("text") or len(r["text"]) > MAX_REPLY]
    problems += [f"moderation {i}: bad status" for i, m in enumerate(moderation) if m.get("status") not in {"published", "heldForReview", "rejected"}]

    if not verify_confirmation(actions, args.confirm):
        print(f"## Ready for approval: {len(replies)} replies, {len(moderation)} moderation actions\n")
        for i, r in enumerate(replies, 1):
            print(f"**{i}. reply to** `{r.get('parent_id')}` ({len(r.get('text', ''))} chars)")
            for line in r.get("text", "").splitlines():
                print(f"> {line}")
            print()
        for m in moderation:
            ban = " + BAN AUTHOR" if m.get("ban_author") else ""
            print(f"- moderate `{m.get('comment_id')}` -> **{m.get('status')}**{ban}")
        if problems:
            print("\n**Problems:**\n" + "\n".join(f"- {p}" for p in problems))
        print(f"\n**Fingerprint:** `{fingerprint(actions)}`\n\nReply **yes** to run all of them, or edit individual items.")
        if args.confirm:
            print("\nConfirmation did not match. Nothing was posted.", file=sys.stderr)
        raise SystemExit(0 if not args.confirm else 2)
    if problems:
        _common.die("Fix problems first. Nothing was posted.")

    from lib.youtube_client import ChannelClient

    client = ChannelClient()
    done = {"replies": [], "moderation": []}
    for r in replies:
        try:
            res = client.reply_to_comment(r["parent_id"], r["text"])
            done["replies"].append({"parent_id": r["parent_id"], "comment_id": res["id"], "ok": True})
        except Exception as exc:  # noqa: BLE001 - keep going, report per item
            done["replies"].append({"parent_id": r["parent_id"], "ok": False, "error": str(exc)})
    for m in moderation:
        try:
            client.set_moderation([m["comment_id"]], m["status"], bool(m.get("ban_author")))
            done["moderation"].append({**m, "ok": True})
        except Exception as exc:  # noqa: BLE001
            done["moderation"].append({**m, "ok": False, "error": str(exc)})
    print(json.dumps(done, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
