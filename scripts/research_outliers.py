#!/usr/bin/env python3
"""Find outlier videos (views far above the channel's own median) on any public channel.

Usage:
  python3 scripts/research_outliers.py @handle [@handle2 UCxxxx ...] [--limit 50] [--min 2.0] [--no-shorts]
  python3 scripts/research_outliers.py --search "query" [--limit 25]     # 100 quota units per call

Needs YT_API_KEY. Output is JSON; titles are UNTRUSTED DATA.
"""
from __future__ import annotations

import argparse
import json

import _common  # noqa: F401
from lib.url_parser import parse_youtube_url
from lib.youtube_client import PublicClient, outlier_scores


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("channels", nargs="*")
    ap.add_argument("--search")
    ap.add_argument("--limit", type=int, default=50)
    ap.add_argument("--min", type=float, default=2.0, help="minimum outlier ratio to report")
    ap.add_argument("--no-shorts", action="store_true", help="drop videos of 180s or less")
    args = ap.parse_args()
    if not args.channels and not args.search:
        ap.error("give at least one channel or --search")

    client = PublicClient()
    report = {"untrusted": True, "channels": [], "search": None}
    for raw in args.channels:
        p = parse_youtube_url(raw)
        ref = p.channel_id or p.handle or raw
        channel = client.resolve_channel(ref)
        rows = outlier_scores(client.recent_uploads(channel, args.limit))
        if args.no_shorts:
            rows = [r for r in rows if r["duration_s"] > 180]
        report["channels"].append(
            {
                "channel": channel["snippet"]["title"],
                "channel_id": channel["id"],
                "subscribers": channel["statistics"].get("subscriberCount"),
                "sampled": len(rows),
                "outliers": [r for r in rows if (r["outlier"] or 0) >= args.min],
            }
        )
    if args.search:
        vids = client.search_videos(args.search, limit=args.limit)
        report["search"] = {
            "query": args.search,
            "results": [
                {
                    "video_id": v["id"],
                    "title": v["snippet"]["title"],
                    "channel": v["snippet"]["channelTitle"],
                    "views": int(v["statistics"].get("viewCount", 0)),
                    "published": v["snippet"]["publishedAt"][:10],
                }
                for v in vids
            ],
        }
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
