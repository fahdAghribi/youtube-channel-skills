"""Parse YouTube URLs into video / channel / comment / playlist identifiers."""
from __future__ import annotations

import re
from dataclasses import dataclass
from urllib.parse import parse_qs, urlparse

_VIDEO_ID = re.compile(r"^[A-Za-z0-9_-]{11}$")
_CHANNEL_ID = re.compile(r"^UC[A-Za-z0-9_-]{22}$")
_HOSTS = {"youtube.com", "www.youtube.com", "m.youtube.com", "music.youtube.com", "youtu.be", "www.youtu.be"}


@dataclass(frozen=True)
class ParsedYouTubeUrl:
    kind: str  # "video" | "short" | "live" | "channel" | "handle" | "playlist" | "unknown"
    video_id: str | None = None
    channel_id: str | None = None
    handle: str | None = None
    playlist_id: str | None = None
    comment_id: str | None = None
    start_seconds: int | None = None


def _start(qs) -> int | None:
    raw = (qs.get("t") or qs.get("start") or [None])[0]
    if not raw:
        return None
    m = re.fullmatch(r"(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s?)?", raw)
    if not m or not any(m.groups()):
        return None
    h, mi, s = (int(g) if g else 0 for g in m.groups())
    return h * 3600 + mi * 60 + s


def parse_youtube_url(url: str) -> ParsedYouTubeUrl:
    """Accepts watch, youtu.be, shorts, live, embed, channel, @handle and playlist URLs.

    A bare 11-char video id, a UC... channel id, or an @handle is accepted too.
    """
    url = (url or "").strip()
    if _VIDEO_ID.match(url):
        return ParsedYouTubeUrl(kind="video", video_id=url)
    if _CHANNEL_ID.match(url):
        return ParsedYouTubeUrl(kind="channel", channel_id=url)
    if url.startswith("@"):
        return ParsedYouTubeUrl(kind="handle", handle=url)

    if "://" not in url:
        url = "https://" + url
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    if host not in _HOSTS:
        return ParsedYouTubeUrl(kind="unknown")
    qs = parse_qs(parsed.query)
    parts = [p for p in parsed.path.split("/") if p]
    comment_id = (qs.get("lc") or [None])[0]
    start = _start(qs)

    if host.endswith("youtu.be"):
        vid = parts[0] if parts else None
        if vid and _VIDEO_ID.match(vid):
            return ParsedYouTubeUrl(kind="video", video_id=vid, comment_id=comment_id, start_seconds=start)
        return ParsedYouTubeUrl(kind="unknown")

    if parts[:1] == ["watch"] and "v" in qs and _VIDEO_ID.match(qs["v"][0]):
        return ParsedYouTubeUrl(
            kind="video",
            video_id=qs["v"][0],
            playlist_id=(qs.get("list") or [None])[0],
            comment_id=comment_id,
            start_seconds=start,
        )
    if len(parts) >= 2 and parts[0] in {"shorts", "live", "embed", "v"} and _VIDEO_ID.match(parts[1]):
        kind = {"shorts": "short", "live": "live"}.get(parts[0], "video")
        return ParsedYouTubeUrl(kind=kind, video_id=parts[1], comment_id=comment_id, start_seconds=start)
    if parts[:1] == ["playlist"] and "list" in qs:
        return ParsedYouTubeUrl(kind="playlist", playlist_id=qs["list"][0])
    if len(parts) >= 2 and parts[0] == "channel" and _CHANNEL_ID.match(parts[1]):
        return ParsedYouTubeUrl(kind="channel", channel_id=parts[1])
    if parts and parts[0].startswith("@"):
        return ParsedYouTubeUrl(kind="handle", handle=parts[0])
    return ParsedYouTubeUrl(kind="unknown")
