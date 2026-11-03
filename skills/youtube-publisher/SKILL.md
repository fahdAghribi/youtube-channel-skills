---
name: youtube-publisher
description: "Upload, schedule and update YouTube videos through the official Data API with a fingerprinted approval gate: dry run shows the exact payload, the user approves, only then it publishes. Handles thumbnail, playlist, scheduling, visibility changes and metadata edits on existing videos. Not for writing metadata (use youtube-metadata-optimizer)."
---

# YouTube Publisher

The only skill that writes to the channel's videos. Every action is two-pass: a dry
run that prints an approval card with a **fingerprint** of the exact payload, and a
confirmed run with `--confirm <fingerprint>` that refuses to act if anything changed.

## When to use

- "Upload this video", "schedule it for Tuesday 18:00", "make it public"
- "Change the title/description/thumbnail of this video"
- Bulk updates (e.g. adding a link to the last 20 descriptions), one approval per video

## Prerequisites

Tier 2 (owner). Check with `python3 scripts/check_config.py`. If not ready, walk the
user through `README.md` §Setup (Google Cloud project, OAuth Desktop client,
`python3 scripts/auth.py`). Without Tier 2, fall back to **manual mode**: give a
Studio checklist with every field ready to paste.

## Steps: new upload

1. Make sure a `video.json` exists and passes `python3 scripts/validate_metadata.py video.json`. If not, run `youtube-metadata-optimizer` first.
2. **Confirm the channel**: `check_config.py` / `auth.py` printed which channel the token controls. Say it to the user before the first write in the session.
3. **Dry run**: `python3 scripts/publish_video.py video.json`. Show the approval card to the user *verbatim* (title, description, fields, validation, fingerprint).
4. **Wait for explicit approval** ("yes", "sí", "publica", "dale"). Edits → update `video.json` → new dry run → new fingerprint.
5. **Confirmed run**: `python3 scripts/publish_video.py video.json --confirm <fingerprint from the card>`.
6. **Report** the video URL, visibility, scheduled time (in the user's time zone), thumbnail/playlist results.
7. **Studio-only handoff**: pinned comment, end screens, cards, Test & Compare variants, subtitles check. Give the checklist from the metadata step.

## Steps: update an existing video

1. Write `changes.json` with only the fields to change (`title`, `description`, `tags`, `privacyStatus`, `publishAt`, `madeForKids`, `thumbnail`).
2. Dry run: `python3 scripts/update_video.py <url> changes.json` shows a before/after diff and fingerprint.
3. Approval → `python3 scripts/update_video.py <url> changes.json --confirm <fingerprint>`.

## Scheduling rules

- `publishAt` is UTC ISO 8601 in the file; always tell the user the local time too.
- Scheduled uploads must be `private` until publish time (validator enforces it).
- Upload ≥ 24 h ahead so HD processing and checks finish.
- If the Google Cloud project is unaudited, uploads stay private regardless (see `../../references/api-quota.md` gotcha 1). Tell the user before uploading, and offer to schedule from Studio instead.

## Hard rules

- **Never run with `--confirm` without the user's explicit approval of that specific card in this conversation.** Never compute or guess a fingerprint yourself; copy it from the card the user saw.
- Approval for one video does not carry to the next one, nor to an edited payload.
- Never change `madeForKids` or make a video public as a side effect of another request.
- Bulk operations: one card per video, or one card listing every video with its own fingerprint; the user approves each.
- On failure, report the error as returned. Do not retry uploads blindly (each attempt costs quota).

## Files

- `scripts/publish_video.py`, `scripts/update_video.py`, `scripts/validate_metadata.py`, `scripts/check_config.py`, `scripts/auth.py`
- `../../references/api-quota.md`
- `../../references/metadata-limits.md`

## Related skills

- `youtube-metadata-optimizer` — produces the `video.json`
- `youtube-title-thumbnail` — the thumbnail file and title
- `youtube-comment-manager` — first-hours comment replies after publishing
