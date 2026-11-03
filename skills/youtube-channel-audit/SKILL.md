---
name: youtube-channel-audit
description: "Audit a YouTube channel end to end (positioning, audience, pillars, branding, home tab, playlists, packaging consistency, upload history) and write the shared channel profile every other skill reads. Use when starting with a new or existing channel, or when growth stalls. Not for diagnosing one video's numbers (use youtube-analytics-reviewer)."
---

# YouTube Channel Audit

Score the channel against what makes YouTube recommend it, return a prioritised fix
list, and fill `../../references/channel-profile.md` so every later task starts with context.

## When to use

- "Audit my channel", "why is my channel not growing", "set up my channel"
- First run of the bundle (profile says `filled: no`)
- Before a rebrand, niche change, or language switch

## Input

- Channel URL or @handle (or a description if the channel does not exist yet)
- Goal: subscribers, watch time for monetisation (YPP), leads/sales, authority
- Optional: Studio exports (Overview, Content tab CSV), the creator's time budget per week

## Steps

1. **Load the profile.** If `../../references/channel-profile.md` has `filled: yes`, start from it and only ask about gaps.
2. **Collect data** (tier-dependent):
   - Tier 1+: `python3 scripts/research_outliers.py @handle --limit 50 --min 0` gives the last 50 uploads with views, duration and the outlier ratio vs the channel median.
   - Tier 2 (own channel): `python3 scripts/analytics_report.py top --days 90` adds watch time, % viewed and subscribers per video.
   - Tier 0: ask the user to paste the Content tab or a list of the last 20 titles with views.
3. **Interview** the 4 starred profile questions plus: who is the viewer, what do they search, which 3-5 channels do they also watch.
4. **Score the 8 areas** below (0-3 each) using `references/audit-checklist.md`.
5. **Find the pattern in the outliers**: which topics/formats/titles beat the median by 2x+? Which are flops? This is the strongest evidence of what the audience wants from *this* channel.
6. **Prioritise**: return at most 7 fixes, ordered by impact ÷ effort. Each fix has a concrete next action and which skill executes it.
7. **Write the profile.** Show the filled `channel-profile.md` as a diff, ask for approval, then save it with `filled: yes` and today's date in `updated:`.

## The 8 areas

| # | Area | What "3" looks like |
|---|---|---|
| 1 | Positioning | One-line promise a stranger understands in 5 s; videos all serve it |
| 2 | Audience fit | Clear primary viewer; titles use their words |
| 3 | Pillars | 2-4 pillars, each with at least one proven outlier |
| 4 | Packaging | Recognisable thumbnail style, titles complement thumbnails, no repetition |
| 5 | Retention craft | Hooks start in the first line, avg % viewed at or above channel norm |
| 6 | Cadence | Sustainable schedule kept for 8+ weeks |
| 7 | Channel page | Banner within safe area, handle, About with keywords + links, trailer for non-subs, sections by pillar, playlists |
| 8 | Conversion | End screens, pinned comment, playlists chaining videos; links that match the goal |

## Output

1. **Scorecard** table (area, score, evidence, fix).
2. **What the outliers say** (3-5 bullets, each with a video and its ratio).
3. **Top fixes** (≤ 7), each: action, why, effort (S/M/L), skill to run next.
4. **Profile diff** awaiting approval.

## Hard rules

Global voice rules: see root SKILL.md §Voice rules.

- Outlier ratios and numbers come from script output or the user. Never estimate views.
- Never recommend deleting old videos to "reset" the channel: there is no such mechanism.
- Recommend a niche change only with evidence (outliers in the new topic, or the user's explicit goal).

## Files

- `references/audit-checklist.md` — scoring criteria per area
- `../../references/channel-profile.md` — the profile this skill writes
- `../../references/algorithm-heuristics.md` — why each area matters
- `../../references/metadata-limits.md` — banner, avatar and trailer specs

## Related skills

- `youtube-idea-research` — turn the outlier patterns into a backlog
- `youtube-content-planner` — turn pillars + cadence into a calendar
- `youtube-title-thumbnail` — fix packaging issues found here
- `youtube-analytics-reviewer` — deep dive on individual videos
