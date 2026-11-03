#!/usr/bin/env python3
"""Change metadata of an existing video (title, description, tags, privacy, schedule).

Usage:
  python3 scripts/update_video.py VIDEO_URL_OR_ID changes.json               # dry run, shows before/after
  python3 scripts/update_video.py VIDEO_URL_OR_ID changes.json --confirm FP  # applies

changes.json holds only the fields you want to change. Omitted fields are kept.
Optional "thumbnail": path replaces the thumbnail too.
"""
from __future__ import annotations

import argparse
import json
import sys

import _common
from lib.approval import render_approval_card, verify_confirmation
from lib.metadata import validate_metadata, has_errors
from lib.url_parser import parse_youtube_url


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("changes")
    ap.add_argument("--confirm")
    args = ap.parse_args()

    vid = parse_youtube_url(args.video).video_id
    if not vid:
        _common.die(f"not a video URL or id: {args.video}")
    changes = _common.load_json(args.changes)

    from lib.youtube_client import ChannelClient

    client = ChannelClient()
    current = client.get_video(vid)
    before = {
        "title": current["snippet"]["title"],
        "description": current["snippet"].get("description", ""),
        "tags": current["snippet"].get("tags", []),
        "privacyStatus": current["status"]["privacyStatus"],
        "publishAt": current["status"].get("publishAt"),
        "madeForKids": current["status"].get("selfDeclaredMadeForKids", current["status"].get("madeForKids")),
    }
    after = {**before, **changes}
    if after.get("publishAt") is None:
        after.pop("publishAt", None)
    issues = validate_metadata(after, duration_seconds=None)
    payload = {"video_id": vid, **changes}

    if not verify_confirmation(payload, args.confirm):
        diff = {k: {"before": before.get(k), "after": v} for k, v in changes.items() if before.get(k) != v}
        print(render_approval_card(kind="metadata update", payload=payload, target=f"https://youtu.be/{vid}", issues=issues))
        print("\n**Diff:**\n```json\n" + json.dumps(diff, ensure_ascii=False, indent=2) + "\n```")
        if args.confirm:
            print("\nConfirmation did not match. Nothing changed.", file=sys.stderr)
        raise SystemExit(0 if not args.confirm else 2)
    if has_errors(issues):
        _common.die("Validation errors present. Nothing changed.")

    meta_changes = {k: v for k, v in changes.items() if k != "thumbnail"}
    if meta_changes:
        client.update_video(vid, meta_changes)
    if changes.get("thumbnail"):
        client.set_thumbnail(vid, changes["thumbnail"])
    print(json.dumps({"video_id": vid, "updated": sorted(changes)}, indent=2))


if __name__ == "__main__":
    main()
