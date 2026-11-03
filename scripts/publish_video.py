#!/usr/bin/env python3
"""Upload (and optionally schedule) a video described by a video.json.

Usage:
  python3 scripts/publish_video.py video.json                 # dry run: prints approval card + fingerprint
  python3 scripts/publish_video.py video.json --confirm FP    # uploads, only if FP matches

video.json fields: file, title, description, tags, categoryId, privacyStatus,
publishAt, madeForKids, containsSyntheticMedia, defaultLanguage,
defaultAudioLanguage, thumbnail, playlistId, isShort.

The fingerprint covers every field plus the video file's size, so editing the
metadata or swapping the file after approval invalidates the confirmation.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

import _common
from lib.approval import render_approval_card, verify_confirmation
from lib.metadata import validate_metadata, has_errors


def build_payload(meta: dict) -> dict:
    payload = dict(meta)
    f = pathlib.Path(meta.get("file", ""))
    payload["_file_bytes"] = f.stat().st_size if f.is_file() else None
    t = pathlib.Path(meta.get("thumbnail", "")) if meta.get("thumbnail") else None
    payload["_thumbnail_bytes"] = t.stat().st_size if t and t.is_file() else None
    return payload


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("meta")
    ap.add_argument("--confirm")
    args = ap.parse_args()

    meta = _common.load_json(args.meta)
    payload = build_payload(meta)
    issues = validate_metadata(meta, duration_seconds=_common.probe_duration(meta.get("file")))
    if payload["_file_bytes"] is None:
        from lib.metadata import Issue

        issues.append(Issue("error", "file", f"video file not found: {meta.get('file')}"))
    if meta.get("thumbnail") and payload["_thumbnail_bytes"] is None:
        from lib.metadata import Issue

        issues.append(Issue("error", "thumbnail", f"thumbnail not found: {meta.get('thumbnail')}"))
    elif payload["_thumbnail_bytes"] and payload["_thumbnail_bytes"] > 2 * 1024 * 1024:
        from lib.metadata import Issue

        issues.append(Issue("error", "thumbnail", "larger than 2 MB"))

    if not verify_confirmation(payload, args.confirm):
        print(render_approval_card(kind="video upload", payload=payload, target="your channel (OAuth)", issues=issues))
        if args.confirm:
            print("\nConfirmation did not match the current payload. Nothing was uploaded.", file=sys.stderr)
        raise SystemExit(0 if not args.confirm else 2)
    if has_errors(issues):
        _common.die("Validation errors present. Nothing was uploaded.")

    from lib.youtube_client import ChannelClient

    client = ChannelClient()
    video = client.upload_video(meta, meta["file"], progress=lambda p: print(f"  uploaded {p:.0%}", file=sys.stderr))
    vid = video["id"]
    result = {"video_id": vid, "url": f"https://youtu.be/{vid}", "privacyStatus": video["status"]["privacyStatus"], "publishAt": video["status"].get("publishAt")}
    if meta.get("thumbnail"):
        try:
            client.set_thumbnail(vid, meta["thumbnail"])
            result["thumbnail"] = "set"
        except Exception as exc:  # noqa: BLE001 - report, do not lose the upload result
            result["thumbnail"] = f"failed: {exc} (custom thumbnails need a verified channel)"
    if meta.get("playlistId"):
        try:
            client.add_to_playlist(vid, meta["playlistId"])
            result["playlist"] = "added"
        except Exception as exc:  # noqa: BLE001
            result["playlist"] = f"failed: {exc}"
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
