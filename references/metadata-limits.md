# YouTube metadata limits (enforced by `lib/metadata.py`)

`python3 scripts/validate_metadata.py video.json` checks all of these offline.
Keep this file and `lib/metadata.py` in sync.

| Field | Hard limit | Soft guidance |
|---|---|---|
| Title | 100 chars, no `<` `>` | Front-load the payoff in the first ~50-70 chars (truncation in search / suggested / mobile) |
| Description | 5,000 bytes (UTF-8), no `<` `>` | First ~150 chars show in search and above "...more": put the value + main keyword there |
| Tags | 500 chars total (multi-word tags count +2 for quotes, plus commas) | Low ranking weight; use for misspellings and brand/name variants |
| Hashtags | More than 15 in the description → YouTube ignores all of them | 3-5 relevant; the first 3 can show above the title |
| Chapters | First timestamp `00:00`, at least 3, ascending, each ≥ 10 s | Label with the viewer's words, not "Part 2" |
| Thumbnail | ≤ 2 MB, JPG/PNG/GIF (static) | 1280×720 (16:9), legible at 160 px wide, keep bottom-right clear (duration badge) |
| Shorts | Up to 3 min, vertical or square | Hook in the first second, loops well |
| Scheduling | `publishAt` requires `privacyStatus: private`, ISO 8601 with timezone | |
| Made for kids | Must be declared (`madeForKids`) | Legal (COPPA) declaration, never guess: ask |
| Synthetic media | `containsSyntheticMedia` when realistic altered/AI content | Disclose; it is policy |
| Pinned comment / heart | Not available in the Data API | Do it in Studio; the skill hands over the text |
| End screens / cards | Not available in the Data API | Do it in Studio; the skill hands over a checklist |

## Category IDs (most used)

1 Film & Animation · 2 Autos · 10 Music · 15 Pets · 17 Sports · 19 Travel · 20 Gaming ·
22 People & Blogs · 23 Comedy · 24 Entertainment · 25 News & Politics · 26 Howto & Style ·
27 Education · 28 Science & Technology · 29 Nonprofits

## Channel branding specs

| Asset | Spec |
|---|---|
| Profile picture | 800×800, round crop, readable at 48 px |
| Banner | 2560×1440, safe area 1546×423 centred (everything important inside it) |
| Watermark | 150×150, transparent PNG |
| Channel trailer | 30-90 s, for non-subscribers |
