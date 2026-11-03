---
name: youtube-metadata-optimizer
description: "Write and validate a video's metadata: search-aware description (first 150 chars), chapters from the script or transcript, tags, hashtags, playlist, category, end screen and pinned comment text. Produces a video.json that passes the offline validator. Not for titles and thumbnails (use youtube-title-thumbnail) or for uploading (use youtube-publisher)."
---

# YouTube Metadata Optimizer

Everything below the title, packaged as a `video.json` that
`python3 scripts/validate_metadata.py` accepts and `youtube-publisher` can upload.

## When to use

- "Write the description", "make chapters", "tags for this video"
- Before every upload (the publisher expects a validated `video.json`)
- Fixing metadata on old videos (then hand the diff to `youtube-publisher` update mode)

## Input

- Final title (from `youtube-title-thumbnail`)
- Script with section times, or a transcript/SRT with timestamps, or the user's own chapter list
- Video file path and duration (for chapter validation)
- Links allowed by the profile (§Packaging style) and any sponsor/affiliate disclosures

## Steps

1. **Load the profile** for language, links, defaults (category, madeForKids, synthetic media, playlist).
2. **Description**, in this order (`references/description-template.md`):
   1. Lines 1-2 (~150 chars): what the viewer gets, with the main search phrase used naturally.
   2. Short expansion (2-4 lines) with secondary phrases.
   3. Links block (only profile-approved links; disclosures first if any).
   4. Chapters.
   5. 3-5 hashtags at the end.
3. **Chapters**: start at `00:00`, ≥ 3 entries, each ≥ 10 s, labelled with the viewer's words ("Cómo elegir el micrófono", not "Parte 2"). Derive from section times or transcript; if neither exists, ask.
4. **Tags**: 5-15 tags, 300-450 chars total: exact topic, variants, common misspellings, creator/brand name. Low weight, do not overthink.
5. **Status fields**: `madeForKids` (ask if not in profile, never guess), `containsSyntheticMedia` when realistic AI/altered content is shown, `categoryId`, `defaultLanguage`, `defaultAudioLanguage`, `privacyStatus`, optional `publishAt`.
6. **Studio-only extras** (not in the API): pinned comment text (a question that invites specific answers), end screen plan (1 best-for-viewer video + 1 specific video + subscribe), cards (max 1-2, at moments the viewer would otherwise leave).
7. **Write `video.json`** and run `python3 scripts/validate_metadata.py video.json`. Fix every error; explain any remaining warning.
8. Return the file, the validator output, and the Studio-only checklist.

## Output

- `video.json` (schema in `references/description-template.md`)
- Validator output
- Pinned comment text, end screen + cards checklist

## Hard rules

Global voice rules: see root SKILL.md §Voice rules.

- No keyword stuffing: a phrase used more than twice in the description reads as spam to people and systems.
- No links in the first two lines unless the video's purpose is that link.
- Never add a link, code or handle the user did not approve.
- `madeForKids` is a legal declaration: ask, do not infer.

## Files

- `references/description-template.md` — description layout and `video.json` schema
- `../../references/metadata-limits.md` — limits the validator enforces
- `scripts/validate_metadata.py`

## Related skills

- `youtube-title-thumbnail` — the title this metadata supports
- `youtube-publisher` — uploads the validated `video.json`
- `youtube-script-writer` — source of chapter times
