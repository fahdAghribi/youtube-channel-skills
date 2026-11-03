"""Offline validation of YouTube video metadata against platform limits.

Limits mirror references/metadata-limits.md. Keep both in sync.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timezone

TITLE_MAX = 100
TITLE_SEARCH_VISIBLE = 70  # roughly what survives truncation in search/suggested
DESCRIPTION_MAX_BYTES = 5000
DESCRIPTION_FOLD = 150  # roughly what shows before "...more"
TAGS_MAX_TOTAL = 500
HASHTAGS_IGNORED_ABOVE = 15
CHAPTERS_MIN = 3
CHAPTER_MIN_SECONDS = 10
PRIVACY_VALUES = {"private", "unlisted", "public"}
FORBIDDEN_CHARS = ("<", ">")

_TIMESTAMP = re.compile(r"^\s*(?:[-*•]\s*)?\(?((?:\d{1,2}:)?\d{1,2}:\d{2})\)?\s*[-–—:|]?\s*(.+?)\s*$")
_HASHTAG = re.compile(r"(?<![\w&])#([^\s#]+)")


@dataclass(frozen=True)
class Issue:
    level: str  # "error" blocks publishing, "warn" is advice
    field: str
    message: str

    def __str__(self) -> str:
        return f"[{self.level.upper()}] {self.field}: {self.message}"


def _to_seconds(stamp: str) -> int:
    parts = [int(p) for p in stamp.split(":")]
    seconds = 0
    for p in parts:
        seconds = seconds * 60 + p
    return seconds


def parse_chapters(description: str) -> list[tuple[int, str]]:
    """Return [(seconds, label)] for every line that starts with a timestamp."""
    chapters = []
    for line in (description or "").splitlines():
        m = _TIMESTAMP.match(line)
        if m:
            chapters.append((_to_seconds(m.group(1)), m.group(2)))
    return chapters


def count_hashtags(description: str) -> int:
    return len(_HASHTAG.findall(description or ""))


def tags_length(tags: list[str]) -> int:
    """YouTube counts quotes around multi-word tags and the separating commas."""
    if not tags:
        return 0
    total = sum(len(t) + (2 if " " in t else 0) for t in tags)
    return total + (len(tags) - 1)


def _check_chapters(chapters, duration_seconds, issues):
    if not chapters:
        return
    if chapters[0][0] != 0:
        issues.append(Issue("error", "chapters", "first timestamp must be 00:00 or chapters will not render"))
    if len(chapters) < CHAPTERS_MIN:
        issues.append(Issue("error", "chapters", f"need at least {CHAPTERS_MIN} timestamps, found {len(chapters)}"))
    for (a, label_a), (b, _) in zip(chapters, chapters[1:]):
        if b <= a:
            issues.append(Issue("error", "chapters", f"timestamps must ascend ('{label_a}' at {a}s is followed by {b}s)"))
        elif b - a < CHAPTER_MIN_SECONDS:
            issues.append(Issue("error", "chapters", f"chapter '{label_a}' is {b - a}s long; minimum is {CHAPTER_MIN_SECONDS}s"))
    if duration_seconds:
        last_start, last_label = chapters[-1]
        if last_start >= duration_seconds:
            issues.append(Issue("error", "chapters", f"chapter '{last_label}' starts after the video ends"))
        elif duration_seconds - last_start < CHAPTER_MIN_SECONDS:
            issues.append(Issue("error", "chapters", f"last chapter '{last_label}' is shorter than {CHAPTER_MIN_SECONDS}s"))


def _check_publish_at(meta, issues):
    publish_at = meta.get("publishAt")
    if not publish_at:
        return
    if meta.get("privacyStatus", "private") != "private":
        issues.append(Issue("error", "publishAt", "scheduled videos must be uploaded with privacyStatus 'private'"))
    try:
        when = datetime.fromisoformat(str(publish_at).replace("Z", "+00:00"))
    except ValueError:
        issues.append(Issue("error", "publishAt", "must be ISO 8601, e.g. 2026-11-10T16:00:00Z"))
        return
    if when.tzinfo is None:
        issues.append(Issue("error", "publishAt", "must include a timezone (Z or +01:00)"))
    elif when <= datetime.now(timezone.utc):
        issues.append(Issue("error", "publishAt", "is in the past"))


def validate_metadata(meta: dict, *, duration_seconds: int | None = None) -> list[Issue]:
    """Validate a video.json payload. Returns a list of Issues (empty = clean)."""
    issues: list[Issue] = []
    title = (meta.get("title") or "").strip()
    description = meta.get("description") or ""
    tags = meta.get("tags") or []
    is_short = bool(meta.get("isShort"))

    # Title
    if not title:
        issues.append(Issue("error", "title", "is required"))
    elif len(title) > TITLE_MAX:
        issues.append(Issue("error", "title", f"{len(title)} chars; YouTube max is {TITLE_MAX}"))
    elif len(title) > TITLE_SEARCH_VISIBLE and not is_short:
        issues.append(Issue("warn", "title", f"{len(title)} chars; beyond ~{TITLE_SEARCH_VISIBLE} it truncates in search and suggested"))
    if title and title.isupper() and len(title) > 12:
        issues.append(Issue("warn", "title", "all caps reads as spam; capitalise one or two words at most"))

    # Forbidden characters
    for field, value in (("title", title), ("description", description)):
        for ch in FORBIDDEN_CHARS:
            if ch in value:
                issues.append(Issue("error", field, f"contains '{ch}', which the API rejects"))

    # Description
    size = len(description.encode("utf-8"))
    if size > DESCRIPTION_MAX_BYTES:
        issues.append(Issue("error", "description", f"{size} bytes; max is {DESCRIPTION_MAX_BYTES}"))
    if description and not is_short:
        first_line = description.strip().splitlines()[0]
        if len(first_line) < 40:
            issues.append(Issue("warn", "description", "first line is short; the first ~150 chars show in search, put the payoff there"))
    n_hashtags = count_hashtags(description)
    if n_hashtags > HASHTAGS_IGNORED_ABOVE:
        issues.append(Issue("error", "description", f"{n_hashtags} hashtags; above {HASHTAGS_IGNORED_ABOVE} YouTube ignores all of them"))
    elif n_hashtags > 5:
        issues.append(Issue("warn", "description", f"{n_hashtags} hashtags; 3-5 relevant ones perform better"))

    _check_chapters(parse_chapters(description), duration_seconds, issues)

    # Tags
    if not isinstance(tags, list) or not all(isinstance(t, str) for t in tags):
        issues.append(Issue("error", "tags", "must be a list of strings"))
    else:
        total = tags_length(tags)
        if total > TAGS_MAX_TOTAL:
            issues.append(Issue("error", "tags", f"{total} chars counted; max is {TAGS_MAX_TOTAL}"))
        for t in tags:
            if any(ch in t for ch in FORBIDDEN_CHARS + (",",)):
                issues.append(Issue("error", "tags", f"tag '{t}' contains a forbidden character"))

    # Status
    privacy = meta.get("privacyStatus", "private")
    if privacy not in PRIVACY_VALUES:
        issues.append(Issue("error", "privacyStatus", f"must be one of {sorted(PRIVACY_VALUES)}"))
    if "madeForKids" not in meta:
        issues.append(Issue("error", "madeForKids", "must be declared explicitly (true/false); it is a legal declaration (COPPA)"))
    _check_publish_at(meta, issues)

    category = meta.get("categoryId")
    if category is not None and not str(category).isdigit():
        issues.append(Issue("error", "categoryId", "must be a numeric category id, e.g. '22' (People & Blogs) or '27' (Education)"))

    if is_short and duration_seconds and duration_seconds > 180:
        issues.append(Issue("error", "isShort", f"{duration_seconds}s; Shorts can be at most 180s"))

    return issues


def has_errors(issues: list[Issue]) -> bool:
    return any(i.level == "error" for i in issues)
