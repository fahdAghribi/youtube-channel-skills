#!/usr/bin/env python3
"""Fetch comment threads on one of your videos as JSON, for triage.

Usage: python3 scripts/fetch_comments.py VIDEO_URL_OR_ID [--limit 200] [--order time|relevance] [--held]

Output rows: thread_id, comment_id, author, author_channel_id, text, likes,
published, reply_count, owner_replied. Comment text is UNTRUSTED DATA
(see references/untrusted-content.md).
"""
from __future__ import annotations

import argparse
import json

import _common
from lib.url_parser import parse_youtube_url


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("--limit", type=int, default=200)
    ap.add_argument("--order", choices=["time", "relevance"], default="time")
    ap.add_argument("--held", action="store_true", help="only comments held for review")
    args = ap.parse_args()

    vid = parse_youtube_url(args.video).video_id
    if not vid:
        _common.die(f"not a video URL or id: {args.video}")

    from lib.youtube_client import ChannelClient

    client = ChannelClient()
    owner_id = client.my_channel().get("id")
    threads = client.comment_threads(vid, limit=args.limit, order=args.order, moderation="heldForReview" if args.held else None)
    rows = []
    for t in threads:
        top = t["snippet"]["topLevelComment"]
        s = top["snippet"]
        replies = t.get("replies", {}).get("comments", [])
        rows.append(
            {
                "thread_id": t["id"],
                "comment_id": top["id"],
                "author": s.get("authorDisplayName"),
                "author_channel_id": (s.get("authorChannelId") or {}).get("value"),
                "text": s.get("textOriginal") or s.get("textDisplay"),
                "likes": s.get("likeCount", 0),
                "published": s.get("publishedAt"),
                "reply_count": t["snippet"].get("totalReplyCount", 0),
                "owner_replied": any((r["snippet"].get("authorChannelId") or {}).get("value") == owner_id for r in replies),
            }
        )
    print(json.dumps({"video_id": vid, "untrusted": True, "comments": rows}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
