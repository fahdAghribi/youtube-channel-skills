#!/usr/bin/env python3
"""Pull channel analytics for diagnosis (read-only, needs OAuth).

Usage:
  python3 scripts/analytics_report.py top        [--days 28] [--limit 25]
  python3 scripts/analytics_report.py retention  VIDEO [--days 90]
  python3 scripts/analytics_report.py traffic    [VIDEO] [--days 28]

Impressions and impressions CTR are NOT exposed by the Analytics API query
endpoint. Ask the user for a YouTube Studio export (Advanced mode > Export > CSV)
when the diagnosis needs CTR.
"""
from __future__ import annotations

import argparse
import json
from datetime import date, timedelta

import _common
from lib.url_parser import parse_youtube_url


def rows(report: dict) -> list[dict]:
    headers = [h["name"] for h in report.get("columnHeaders", [])]
    return [dict(zip(headers, r)) for r in report.get("rows", [])]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("kind", choices=["top", "retention", "traffic"])
    ap.add_argument("video", nargs="?")
    ap.add_argument("--days", type=int, default=28)
    ap.add_argument("--limit", type=int, default=25)
    args = ap.parse_args()

    end = date.today() - timedelta(days=2)  # analytics lag ~48h
    start = end - timedelta(days=args.days)
    vid = parse_youtube_url(args.video).video_id if args.video else None
    if args.kind == "retention" and not vid:
        _common.die("retention needs a video URL or id")

    from lib.youtube_client import ChannelClient

    client = ChannelClient()
    if args.kind == "top":
        data = rows(client.top_videos(start.isoformat(), end.isoformat(), args.limit))
        ids = [r["video"] for r in data]
        titles = {}
        for i in range(0, len(ids), 50):
            res = client.yt.videos().list(part="snippet", id=",".join(ids[i : i + 50])).execute()
            titles.update({v["id"]: v["snippet"]["title"] for v in res.get("items", [])})
        for r in data:
            r["title"] = titles.get(r["video"])
    elif args.kind == "retention":
        data = rows(client.retention_curve(vid, start.isoformat(), end.isoformat()))
    else:
        data = rows(client.traffic_sources(start.isoformat(), end.isoformat(), vid))
    print(json.dumps({"kind": args.kind, "video": vid, "start": start.isoformat(), "end": end.isoformat(), "rows": data}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
