---
name: youtube-title-thumbnail
description: "Package a video: 5-10 title candidates across title formulas, 3 thumbnail concepts as designer-ready briefs (composition, text, colours, emotion), and a Test & Compare plan with 3 variants. Also repackages old videos with good retention but low CTR. Not for the description, tags and chapters (use youtube-metadata-optimizer)."
---

# YouTube Title & Thumbnail

Packaging decides whether a good video gets a chance. Title and thumbnail are one
unit: the thumbnail shows, the title tells, they never repeat each other.

## When to use

- New video: "titles for...", "thumbnail idea for..."
- Old video: "this video has good retention but nobody clicks" (repackaging)
- Before filming: validate that an idea can be packaged

## Input

- Idea / script / promise of the video
- Target traffic: browse, search or suggested (default browse)
- Profile §Packaging style (colours, face, text yes/no)
- For repackaging: current title, thumbnail description, CTR and % viewed (Studio)

## Steps

1. **Load the profile** for language, capitalisation and thumbnail style.
2. **Write the promise** in 8 words. If you cannot, ask the user before packaging.
3. **Generate 8-10 titles across at least 3 formulas** from `../../references/title-formulas.md`. Tag each with formula and traffic source.
4. **Filter**: drop anything that over-promises, repeats the thumbnail text, exceeds ~60 chars for browse, or hides the topic for search.
5. **Three thumbnail concepts** using `references/thumbnail-brief.md`. Each concept is a different *idea* (result, contrast, emotion), not three colour variants.
6. **Pair**: recommend 3 title+thumbnail pairs for Test & Compare. Thumbnail tests are the default; title tests only if the channel has title testing.
7. **Self-check** with the checklist below and return.

## Output

### Titles
| # | Title | Chars | Formula | Traffic | Note |
|---|---|---|---|---|---|

### Thumbnail briefs (×3)
Concept name · focal subject · expression/emotion · background · text (≤ 4 words) · colour palette · composition sketch (ASCII 16:9) · what NOT to include

### Test & Compare plan
| Variant | Thumbnail | Title | Hypothesis |
|---|---|---|---|

### Self-check
- [ ] Readable at 160 px wide (mobile suggested size)
- [ ] One focal point, high contrast, ≤ 4 words on the image
- [ ] Bottom-right corner free (duration badge)
- [ ] Title and thumbnail complement, zero repeated words
- [ ] The video's first 30 s pay the promise
- [ ] Consistent with the channel's recognisable style

## Repackaging mode

Only when **% viewed is at or above channel norm and CTR is below it** (a good video
nobody clicks). Change the thumbnail first, wait 7-14 days, then the title if needed.
One variable at a time. Never repackage a video whose problem is retention.

## Hard rules

Global voice rules: see root SKILL.md §Voice rules.

- No fake reactions, fake UI, misleading arrows/circles on things not in the video.
- No text that duplicates the title. No more than 4 words on the thumbnail.
- If thumbnails will be generated with an image model, write the brief as a prompt too, and remind the user that realistic people must be the creator or consented talent.

## Files

- `references/thumbnail-brief.md` — brief template and composition rules
- `../../references/title-formulas.md`
- `../../references/metadata-limits.md`

## Related skills

- `youtube-script-writer` — the hook must continue this promise
- `youtube-metadata-optimizer` — description and chapters
- `youtube-publisher` — upload with the chosen thumbnail
- `youtube-analytics-reviewer` — decide whether repackaging is the fix
