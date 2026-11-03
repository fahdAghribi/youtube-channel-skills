"""youtube-channel-skills shared library.

Pure-Python helpers (metadata validation, URL parsing, approval gate) import
without any third-party dependency. The API clients import the Google client
libraries lazily, so offline tests and validators run on a bare Python.
"""
from .metadata import Issue, validate_metadata, parse_chapters, count_hashtags, tags_length
from .url_parser import parse_youtube_url, ParsedYouTubeUrl
from .approval import fingerprint, render_approval_card, verify_confirmation

__all__ = [
    "Issue",
    "validate_metadata",
    "parse_chapters",
    "count_hashtags",
    "tags_length",
    "parse_youtube_url",
    "ParsedYouTubeUrl",
    "fingerprint",
    "render_approval_card",
    "verify_confirmation",
]
