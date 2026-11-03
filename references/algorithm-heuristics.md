# How YouTube distributes videos (working heuristics)

These are working heuristics built from YouTube's own public statements (Creator
Insider, YouTube Liaison, Creator Academy) and widely reproduced creator data.
They are not an official formula. Never present them to the user as guaranteed.

## 1. The system follows the viewer, not the video

Recommendations try to predict what *this viewer* will watch and be satisfied with.
There is no "push to all subscribers". A video is tested on small, similar audiences
and expands while the signals hold.

**Signals that matter together:**

| Signal | What it answers | Where to read it |
|---|---|---|
| Impressions CTR | Did the packaging earn the click from people who saw it? | Studio > Reach (export; not in the Analytics query API) |
| Average view duration / % viewed | Did the video keep the promise? | Analytics API `averageViewDuration`, `averageViewPercentage` |
| Retention curve shape | Where exactly do people leave? | Analytics API `audienceWatchRatio` by `elapsedVideoTimeRatio` |
| Satisfaction | Likes, "not interested", surveys, return visits | Partly visible: likes, comments, returning viewers |
| Session | Did they keep watching YouTube afterwards? | Indirect: end screen CTR, playlist starts |

**CTR alone lies.** High CTR + low retention = bait (reach dies). Low CTR + high
retention = packaging problem on a good video (fix title/thumbnail, it can revive).
CTR naturally drops as impressions widen to colder audiences: compare against the
channel's own videos at the same age, not against a universal number.

## 2. Traffic sources behave differently

- **Browse (home)**: driven by packaging + past viewer satisfaction. Biggest lever for growing channels.
- **Suggested**: next to related videos. Topic adjacency to what your viewers already watch matters.
- **Search**: evergreen, intent-driven. Title and first description lines should match the phrasing people type.
- **Shorts feed**: separate surface, measured on swipe-away vs viewed and loops. Shorts views rarely convert to long-form at the same rate; treat them as their own audience unless the topic bridge is tight.
- **External / Notifications / Playlists**: small but they seed the initial test audience.

## 3. Practical rules the skills apply

1. **Packaging first.** Write the title and thumbnail concept *before* the script. If the idea cannot be packaged, it is not ready.
2. **First 30 seconds** confirm the click: restate the promise, show you will deliver, remove the reason to leave. Target ≥ 70% still watching at 0:30 for long-form.
3. **Pay off slowly, pay off fully.** Open loops early, close them late, never close the main loop before the end.
4. **One video, one viewer, one promise.** Mixed audiences send mixed signals.
5. **Consistency over frequency.** A cadence you can keep for 6 months beats a sprint. Quality drop > upload gap.
6. **Outliers teach.** Ideas that beat a channel's own median by 3x+ reveal demand; remix the *idea*, never copy the video.
7. **Old videos are not dead.** Repackaging (new thumbnail/title) on a video with good retention but low CTR is legitimate and often works. Change one variable at a time and wait ~7-14 days.
8. **Test & Compare** (Studio): when available on the channel, test up to 3 thumbnail (and title) variants; YouTube picks by watch-time share. Use it instead of guessing.
9. **Comments early.** Replying in the first hours builds community; it is not a ranking hack, do not fake it.

## 4. Typical ranges (sanity checks, not targets)

| Metric | Typical | Note |
|---|---|---|
| Impressions CTR | 2-10% | YouTube's own guidance; niche and traffic mix move it a lot |
| Avg % viewed, 8-15 min video | 35-55% | Tutorials can be lower (people skip to the answer) |
| Retention at 0:30, long-form | 65-80% | Below 60% = hook/promise mismatch |
| Shorts viewed vs swiped | aim > 70% viewed | Studio > Shorts "Viewed vs swiped away" |
