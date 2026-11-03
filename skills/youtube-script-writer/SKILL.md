---
name: youtube-script-writer
description: "Write a retention-first YouTube script for long-form or Shorts: hook for the first 30 seconds, open loops, value beats with pattern interrupts, mid-roll CTA placement and an ending that feeds the next video. Outputs a two-column script (spoken / on screen) with timing. Not for titles and thumbnails (use youtube-title-thumbnail) or repurposing an existing video (use youtube-shorts-repurposer)."
---

# YouTube Script Writer

Scripts written for the ear and for the retention curve. Packaging comes first: if the
video has no title + thumbnail concept yet, write 3 title candidates before the script
(or call `youtube-title-thumbnail`), because the hook has to continue that promise.

## When to use

- "Write the script for...", "give me an outline", "improve my intro"
- Rewriting a script whose retention data shows an early drop

## Input

- Idea + chosen title/thumbnail (or ask for them)
- Format: talking head, tutorial, test, story, list, comparison, Short
- Target length (long-form default 8-12 min ≈ 1,200-1,800 spoken words at ~150 wpm; Short ≤ 60 s default, ≤ 180 s max)
- Receipts: numbers, stories, demos the creator has (profile §Assets or the user)

## Steps

1. **Load the profile** (voice, language, persona, recurring segments).
2. **Lock the promise**: one sentence, "By the end, the viewer will ___". Everything not serving it is cut.
3. **Pick a hook pattern** from `../../references/hook-patterns.md` that pairs with the title formula.
4. **Outline with the structure** in `references/script-structures.md` for the chosen format. Place the main open loop by 0:30 and close it in the last third.
5. **Write the script** in two columns: *Spoken* and *On screen* (b-roll, text, zoom, demo). Add a visual change every 5-8 s in the first minute and every 15-30 s after.
6. **Place CTAs**: subscribe ask only *after* the first payoff (never in the hook); product/newsletter CTA once, where it solves the problem just discussed; end screen CTA pointing to one specific next video.
7. **Retention pass**: run the checklist below. Mark each risky moment with `⚠ drop risk` and a fix.
8. **Return** the script plus a 1-line summary, word count and estimated duration.

## Output

```
TITLE: ...            THUMBNAIL: ...           PROMISE: ...
EST. DURATION: 10:40  WORDS: 1,610             HOOK: H4

| Time | Spoken | On screen |
|------|--------|-----------|
| 0:00 | ...    | ...       |
```

Then: **Retention checklist** (passed / fixed), **CTA map**, **End screen target**.

## Retention checklist

- [ ] First line continues the title; no greeting, no channel intro
- [ ] Promise restated or shown by 0:10, open loop planted by 0:30
- [ ] No "before we start" detours; sponsor (if any) after the first payoff
- [ ] Every section starts with why the viewer should care (stakes) before how
- [ ] At least one re-hook every ~2 minutes ("but this is where it went wrong")
- [ ] No section > 90 s without a visual change or a new micro-question
- [ ] The ending does not say "that's it for today": it hands off to the next video
- [ ] Receipts are real (profile or user). Unknown numbers marked `[NUMBER?]`

## Hard rules

Global voice rules: see root SKILL.md §Voice rules.

- Spoken language: short sentences, contractions, second person. Read-aloud test.
- Shorts: hook in the first second (visual + words), one idea, payoff by the end, loop the last line into the first when possible.
- Never fabricate experiences, results, testimonials or sources. If the user wants a claim, they supply it.

## Files

- `references/script-structures.md` — structures per format
- `../../references/hook-patterns.md`
- `../../references/voice-rules.md`

## Related skills

- `youtube-title-thumbnail` — packaging the script must continue
- `youtube-metadata-optimizer` — chapters from the script's section times
- `youtube-shorts-repurposer` — cut Shorts from the finished video
