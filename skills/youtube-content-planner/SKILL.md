---
name: youtube-content-planner
description: "Build a 4-week YouTube publishing calendar: long-form videos, Shorts and Community posts per pillar, with publish dates, packaging seeds, production deadlines and a balance check. Exports markdown plus JSON. Use for 'plan my month' or a launch series. Not for finding ideas from scratch (use youtube-idea-research) or writing one script (use youtube-script-writer)."
---

# YouTube Content Planner

A calendar the creator can actually keep, with every slot tied to a pillar, a goal and
a production deadline. Default horizon: 4 weeks.

## When to use

- "Plan my month / my next 4 weeks"
- Preparing a series or launch (product, course, event)
- After an audit or research run, to turn findings into a schedule

## Input

- Pillars and cadence (from `../../references/channel-profile.md`, else ask)
- Idea backlog (from `youtube-idea-research` or the user)
- Weekly production time budget (hours) and team (solo, editor, etc.)
- Fixed dates: launches, holidays, events, sponsor deadlines

## Steps

1. **Load the profile.** Respect cadence, publishing day/hour and language.
2. **Sanity-check capacity.** Estimate hours per format (`references/production-estimates.md`). If the budget does not fit the cadence, propose the lower cadence first; a kept schedule beats an ambitious one.
3. **Assign slots**: long-form first (they anchor the week), then Shorts that *bridge* to them, then Community posts (polls/teasers before a long-form, results after).
4. **For each long-form**: idea, pillar, goal (search / browse / community / conversion), title seed, thumbnail concept, hook pattern (H1-H10), and backward deadlines: script, film, edit, packaging, upload (schedule ≥ 24 h before publish).
5. **Run the balance check** below and fix anything that fails.
6. **Output** markdown + JSON. Offer: draft the first script (`youtube-script-writer`), package the first video (`youtube-title-thumbnail`).

## Output

### Calendar

| Week | Publish (date, time, TZ) | Type | Pillar | Idea | Goal | Title seed | Thumbnail concept | Hook | Script due | Edit due |
|---|---|---|---|---|---|---|---|---|---|---|

### Shorts & Community

| Date | Type | Bridges to | Angle | Source (clip from / original) |
|---|---|---|---|---|

### Balance check

- [ ] No pillar > 50% of long-form slots (unless the user chose a single-pillar channel)
- [ ] At least 1 search-intent (evergreen) video per month
- [ ] At least 1 browse-intent video with a proven outlier behind it
- [ ] No two videos in a row with the same format
- [ ] Every long-form has a Short or Community post pointing to it
- [ ] Production deadlines fit the weekly hour budget
- [ ] Upload at least 24 h before publish (processing, HD, checks)

### JSON

```json
{"timezone": "Europe/Madrid", "items": [{"date": "2026-11-10", "time": "18:00", "type": "long", "pillar": "...", "idea": "...", "goal": "browse", "title_seed": "...", "thumbnail": "...", "hook": "H1", "deadlines": {"script": "...", "film": "...", "edit": "...", "upload": "..."}}]}
```

## Hard rules

Global voice rules: see root SKILL.md §Voice rules.

- Never schedule more than the stated time budget allows.
- Shorts cadence suggestion: 2-5/week if the user has the capacity; 0 is fine for long-form-first channels.
- Publishing hour: when the audience is online (Studio > Audience > "When your viewers are on YouTube"), publish 1-2 h before the peak. Without data, say it is a default.
- Dates are absolute (2026-11-10), never "next Tuesday".

## Files

- `references/production-estimates.md` — hours per format
- `../../references/channel-profile.md`
- `../../references/hook-patterns.md`
- `../../references/title-formulas.md`

## Related skills

- `youtube-idea-research` — fill the backlog
- `youtube-script-writer` — script each slot
- `youtube-shorts-repurposer` — generate the bridge Shorts
- `youtube-publisher` — schedule uploads
