---
name: youtube-analytics-reviewer
description: "Diagnose YouTube performance with a decision tree: is the problem packaging (CTR), the promise (first 30 s), the body (retention curve), distribution (traffic sources) or the topic? Reads the Analytics API or Studio CSV exports and returns 3 prioritised actions per video or for the channel. Not for full channel positioning (use youtube-channel-audit)."
---

# YouTube Analytics Reviewer

Numbers into decisions. The output is never a dashboard; it is "the problem is X,
here is the evidence, do Y next, check Z in 7-14 days".

## When to use

- "Why did this video flop?", "review my last month", "what should I change?"
- Weekly or monthly review cadence
- Before repackaging an old video (to confirm the problem is packaging)

## Input

- Tier 2: video URL(s) or "last 28 days"
- Tier 0/1: Studio exports (Advanced mode > Export > CSV) or screenshots of Reach, Engagement, Audience tabs
- **CTR and impressions always come from Studio** (not in the Analytics query API): ask for them

## Steps

1. **Load the profile** for the channel's norms if recorded, else compute norms from the last 10-20 videos.
2. **Pull data** (Tier 2):
   - Channel: `python3 scripts/analytics_report.py top --days 28`
   - One video: `python3 scripts/analytics_report.py retention <url> --days 90` and `python3 scripts/analytics_report.py traffic <url> --days 28`
3. **Compare to the channel's own norm** at the same age (first 7 / 28 days), never to other channels.
4. **Walk the decision tree** in `references/diagnosis-tree.md`. Stop at the first branch that explains the gap.
5. **Read the retention curve** (`audienceWatchRatio` vs `elapsedVideoTimeRatio`): initial drop (0-30 s), slope, cliffs (> 5-point drop in a few %), bumps (rewatch = valuable moment), end drop timing.
6. **Write 3 actions max**, ordered by impact, each tied to a skill: repackage → `youtube-title-thumbnail`; hook/structure → `youtube-script-writer`; topic → `youtube-idea-research`; comments/community → `youtube-comment-manager`.
7. **Set a check**: which metric to re-read and when (7-14 days for repackaging).

## Output

```
VIDEO / PERIOD: ...
VERDICT: [Packaging | Promise | Body | Distribution | Topic | Working: scale it]
EVIDENCE: 3 bullets with numbers vs channel norm
RETENTION READ: initial drop, cliffs (timestamps), bumps
ACTIONS (≤ 3): action → skill → expected signal
CHECK ON: date + metric
```

For a channel review: a table of the period's videos (views, % viewed, subs gained, CTR if provided, verdict) then the 3 channel-level patterns.

## Hard rules

Global voice rules: see root SKILL.md §Voice rules.

- Never invent metrics. If CTR is missing, say the verdict on packaging is provisional.
- Small samples (< 1,000 impressions or < 100 views) are noise: say so and do not over-diagnose.
- One change at a time per video, so the effect can be read.
- Do not blame "the algorithm". Translate every statement into viewer behaviour.

## Files

- `references/diagnosis-tree.md`
- `../../references/algorithm-heuristics.md`
- `scripts/analytics_report.py`

## Related skills

- `youtube-title-thumbnail` — repackaging
- `youtube-script-writer` — fix hooks and structure for the next video
- `youtube-channel-audit` — when the problem is the whole channel, not a video
