#!/usr/bin/env python3
"""Validate a video.json against YouTube limits, offline.

Usage: python3 scripts/validate_metadata.py video.json [--duration SECONDS]

Exit code 0 = no errors (warnings allowed), 1 = at least one error.
If "file" in video.json points to a real video and ffprobe is installed, the
duration is read from it so chapter and Shorts-length checks run too.
"""
from __future__ import annotations

import argparse
import json

import _common
from lib.metadata import validate_metadata, has_errors, parse_chapters, tags_length, count_hashtags


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("meta")
    ap.add_argument("--duration", type=int)
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args()

    meta = _common.load_json(args.meta)
    duration = args.duration or _common.probe_duration(meta.get("file"))
    issues = validate_metadata(meta, duration_seconds=duration)
    summary = {
        "title_chars": len(meta.get("title", "")),
        "description_bytes": len((meta.get("description") or "").encode("utf-8")),
        "tags_chars": tags_length(meta.get("tags") or []),
        "hashtags": count_hashtags(meta.get("description") or ""),
        "chapters": len(parse_chapters(meta.get("description") or "")),
        "duration_s": duration,
    }
    if args.json:
        print(json.dumps({"summary": summary, "issues": [i.__dict__ for i in issues]}, ensure_ascii=False, indent=2))
    else:
        for k, v in summary.items():
            print(f"{k:18}: {v}")
        print()
        print("\n".join(str(i) for i in issues) or "No issues.")
    raise SystemExit(1 if has_errors(issues) else 0)


if __name__ == "__main__":
    main()
