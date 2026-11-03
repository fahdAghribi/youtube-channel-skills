"""Thin wrappers over the official YouTube Data API v3 and YouTube Analytics API v2.

Two clients:

- ``PublicClient``: read-only public data with an API key (``YT_API_KEY``).
  Used for competitor and outlier research. No OAuth needed.
- ``ChannelClient``: acts as the channel owner via OAuth (``scripts/auth.py``).
  Used for uploads, metadata edits, comments and analytics.

Google libraries are imported lazily so the rest of ``lib`` works offline.
Quota costs are in references/api-quota.md.
"""
from __future__ import annotations

import pathlib
import statistics
from typing import Any

from . import _env

SCOPES = [
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/yt-analytics.readonly",
]
TOKEN_PATH = _env.CONFIG_DIR / "token.json"


class MissingDependency(RuntimeError):
    pass


class MissingCredentials(RuntimeError):
    pass


def _discovery():
    try:
        from googleapiclient.discovery import build  # type: ignore
    except ImportError as exc:  # pragma: no cover - environment dependent
        raise MissingDependency("pip install -r requirements.txt") from exc
    return build


def load_oauth_credentials():
    """Load the stored OAuth token, refreshing it if needed."""
    try:
        from google.auth.transport.requests import Request  # type: ignore
        from google.oauth2.credentials import Credentials  # type: ignore
    except ImportError as exc:  # pragma: no cover
        raise MissingDependency("pip install -r requirements.txt") from exc
    if not TOKEN_PATH.is_file():
        raise MissingCredentials("No OAuth token. Run: python3 scripts/auth.py")
    creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
    if not creds.valid:
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            TOKEN_PATH.write_text(creds.to_json(), encoding="utf-8")
        else:
            raise MissingCredentials("OAuth token invalid. Run: python3 scripts/auth.py")
    return creds


def run_oauth_flow(client_secrets: str) -> pathlib.Path:
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow  # type: ignore
    except ImportError as exc:  # pragma: no cover
        raise MissingDependency("pip install -r requirements.txt") from exc
    flow = InstalledAppFlow.from_client_secrets_file(client_secrets, SCOPES)
    creds = flow.run_local_server(port=0, prompt="consent")
    TOKEN_PATH.parent.mkdir(parents=True, exist_ok=True)
    TOKEN_PATH.write_text(creds.to_json(), encoding="utf-8")
    TOKEN_PATH.chmod(0o600)
    return TOKEN_PATH


def iso8601_duration_to_seconds(value: str) -> int:
    """PT1H2M3S -> 3723. Handles the subset YouTube returns (incl. P1DT...)."""
    import re

    m = re.fullmatch(r"P(?:(\d+)D)?(?:T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?)?", value or "")
    if not m:
        return 0
    d, h, mi, s = (int(g) if g else 0 for g in m.groups())
    return d * 86400 + h * 3600 + mi * 60 + s


# --------------------------------------------------------------------------- public


class PublicClient:
    def __init__(self, api_key: str | None = None):
        key = api_key or _env.get("YT_API_KEY")
        if not key:
            raise MissingCredentials("Set YT_API_KEY in .env (Google Cloud console > Credentials > API key)")
        self.yt = _discovery()("youtube", "v3", developerKey=key, cache_discovery=False)

    def resolve_channel(self, handle_or_id: str) -> dict:
        """Accepts UC... id or @handle. Returns the channels.list item (1 unit)."""
        part = "snippet,statistics,contentDetails"
        if handle_or_id.startswith("UC"):
            res = self.yt.channels().list(part=part, id=handle_or_id).execute()
        else:
            res = self.yt.channels().list(part=part, forHandle=handle_or_id.lstrip("@")).execute()
        items = res.get("items") or []
        if not items:
            raise LookupError(f"channel not found: {handle_or_id}")
        return items[0]

    def recent_uploads(self, channel: dict, limit: int = 50) -> list[dict]:
        """Latest uploads with stats. ~1 unit per 50 videos (playlistItems + videos)."""
        uploads = channel["contentDetails"]["relatedPlaylists"]["uploads"]
        ids: list[str] = []
        token = None
        while len(ids) < limit:
            res = self.yt.playlistItems().list(
                part="contentDetails", playlistId=uploads, maxResults=min(50, limit - len(ids)), pageToken=token
            ).execute()
            ids += [i["contentDetails"]["videoId"] for i in res.get("items", [])]
            token = res.get("nextPageToken")
            if not token:
                break
        return self.videos(ids)

    def videos(self, ids: list[str]) -> list[dict]:
        out = []
        for i in range(0, len(ids), 50):
            res = self.yt.videos().list(part="snippet,statistics,contentDetails", id=",".join(ids[i : i + 50])).execute()
            out += res.get("items", [])
        return out

    def search_videos(self, query: str, limit: int = 25, **filters: Any) -> list[dict]:
        """search.list costs 100 units per call. Use sparingly."""
        res = self.yt.search().list(
            part="id", q=query, type="video", maxResults=min(limit, 50), **filters
        ).execute()
        return self.videos([i["id"]["videoId"] for i in res.get("items", [])])


def outlier_scores(videos: list[dict]) -> list[dict]:
    """Views relative to the channel median. >= 3x is a strong outlier."""
    views = [int(v.get("statistics", {}).get("viewCount", 0)) for v in videos]
    median = statistics.median(views) if views else 0
    rows = []
    for v, n in zip(videos, views):
        rows.append(
            {
                "video_id": v["id"],
                "title": v["snippet"]["title"],
                "published": v["snippet"]["publishedAt"][:10],
                "views": n,
                "duration_s": iso8601_duration_to_seconds(v.get("contentDetails", {}).get("duration", "")),
                "outlier": round(n / median, 2) if median else None,
            }
        )
    return sorted(rows, key=lambda r: r["outlier"] or 0, reverse=True)


# --------------------------------------------------------------------------- owner


class ChannelClient:
    def __init__(self, credentials=None):
        creds = credentials or load_oauth_credentials()
        build = _discovery()
        self.yt = build("youtube", "v3", credentials=creds, cache_discovery=False)
        self.analytics = build("youtubeAnalytics", "v2", credentials=creds, cache_discovery=False)

    # ---- channel / videos
    def my_channel(self) -> dict:
        res = self.yt.channels().list(part="snippet,statistics,contentDetails,brandingSettings", mine=True).execute()
        return (res.get("items") or [{}])[0]

    def get_video(self, video_id: str) -> dict:
        res = self.yt.videos().list(part="snippet,status,contentDetails,statistics", id=video_id).execute()
        items = res.get("items") or []
        if not items:
            raise LookupError(f"video not found or not yours: {video_id}")
        return items[0]

    @staticmethod
    def _body(meta: dict) -> dict:
        snippet = {k: meta[k] for k in ("title", "description", "tags", "categoryId", "defaultLanguage", "defaultAudioLanguage") if k in meta}
        snippet.setdefault("categoryId", "22")
        status = {
            "privacyStatus": meta.get("privacyStatus", "private"),
            "selfDeclaredMadeForKids": bool(meta["madeForKids"]),
        }
        if meta.get("publishAt"):
            status["publishAt"] = meta["publishAt"]
        if "containsSyntheticMedia" in meta:
            status["containsSyntheticMedia"] = bool(meta["containsSyntheticMedia"])
        return {"snippet": snippet, "status": status}

    def upload_video(self, meta: dict, file_path: str, progress=None) -> dict:
        """Resumable upload. Quota: see references/api-quota.md (videos.insert)."""
        from googleapiclient.http import MediaFileUpload  # type: ignore

        media = MediaFileUpload(file_path, chunksize=8 * 1024 * 1024, resumable=True)
        request = self.yt.videos().insert(part="snippet,status", body=self._body(meta), media_body=media)
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status and progress:
                progress(status.progress())
        return response

    def update_video(self, video_id: str, meta: dict) -> dict:
        """videos.update replaces the whole snippet, so merge with the current one first."""
        current = self.get_video(video_id)
        merged = {**current["snippet"], **{k: v for k, v in meta.items() if k in ("title", "description", "tags", "categoryId", "defaultLanguage")}}
        merged.pop("thumbnails", None)
        merged.pop("localized", None)
        body: dict = {"id": video_id, "snippet": merged}
        parts = ["snippet"]
        status_keys = {"privacyStatus", "publishAt", "madeForKids"}
        if status_keys & set(meta):
            status = {k: v for k, v in current["status"].items() if k in ("privacyStatus", "publishAt", "selfDeclaredMadeForKids", "embeddable", "license", "publicStatsViewable")}
            if "privacyStatus" in meta:
                status["privacyStatus"] = meta["privacyStatus"]
            if "publishAt" in meta:
                status["publishAt"] = meta["publishAt"]
            if "madeForKids" in meta:
                status["selfDeclaredMadeForKids"] = bool(meta["madeForKids"])
            body["status"] = status
            parts.append("status")
        return self.yt.videos().update(part=",".join(parts), body=body).execute()

    def set_thumbnail(self, video_id: str, image_path: str) -> dict:
        from googleapiclient.http import MediaFileUpload  # type: ignore

        return self.yt.thumbnails().set(videoId=video_id, media_body=MediaFileUpload(image_path)).execute()

    def add_to_playlist(self, video_id: str, playlist_id: str) -> dict:
        body = {"snippet": {"playlistId": playlist_id, "resourceId": {"kind": "youtube#video", "videoId": video_id}}}
        return self.yt.playlistItems().insert(part="snippet", body=body).execute()

    def list_my_playlists(self) -> list[dict]:
        res = self.yt.playlists().list(part="snippet,contentDetails", mine=True, maxResults=50).execute()
        return res.get("items", [])

    # ---- comments
    def comment_threads(self, video_id: str, limit: int = 100, order: str = "time", moderation: str | None = None) -> list[dict]:
        out: list[dict] = []
        token = None
        while len(out) < limit:
            kwargs = dict(part="snippet,replies", videoId=video_id, maxResults=min(100, limit - len(out)), order=order, textFormat="plainText", pageToken=token)
            if moderation:
                kwargs["moderationStatus"] = moderation
            res = self.yt.commentThreads().list(**kwargs).execute()
            out += res.get("items", [])
            token = res.get("nextPageToken")
            if not token:
                break
        return out

    def reply_to_comment(self, parent_id: str, text: str) -> dict:
        body = {"snippet": {"parentId": parent_id, "textOriginal": text}}
        return self.yt.comments().insert(part="snippet", body=body).execute()

    def set_moderation(self, comment_ids: list[str], status: str, ban_author: bool = False) -> None:
        """status: published | heldForReview | rejected."""
        self.yt.comments().setModerationStatus(id=",".join(comment_ids), moderationStatus=status, banAuthor=ban_author).execute()

    # ---- analytics
    def report(self, start: str, end: str, metrics: str, dimensions: str | None = None, **kwargs: Any) -> dict:
        params = dict(ids="channel==MINE", startDate=start, endDate=end, metrics=metrics, **kwargs)
        if dimensions:
            params["dimensions"] = dimensions
        return self.analytics.reports().query(**params).execute()

    def top_videos(self, start: str, end: str, limit: int = 25) -> dict:
        return self.report(
            start,
            end,
            metrics="views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,subscribersGained,likes,comments,shares",
            dimensions="video",
            sort="-views",
            maxResults=limit,
        )

    def retention_curve(self, video_id: str, start: str, end: str) -> dict:
        return self.report(
            start,
            end,
            metrics="audienceWatchRatio,relativeRetentionPerformance",
            dimensions="elapsedVideoTimeRatio",
            filters=f"video=={video_id}",
        )

    def traffic_sources(self, start: str, end: str, video_id: str | None = None) -> dict:
        kwargs = {"filters": f"video=={video_id}"} if video_id else {}
        return self.report(start, end, metrics="views,estimatedMinutesWatched", dimensions="insightTrafficSourceType", sort="-views", **kwargs)
