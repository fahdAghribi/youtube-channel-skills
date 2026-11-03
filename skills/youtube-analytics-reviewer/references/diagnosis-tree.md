# Diagnosis tree

Compare every number with the channel's own median for videos of the same age and format.

```
1. Impressions low vs norm?
   ├─ yes → was it tested at all? (first 24-48 h impressions)
   │        ├─ low from the start → DISTRIBUTION / TOPIC: topic far from what this audience watches,
   │        │                       or audience not active. Check traffic sources + idea fit.
   │        └─ started OK, then stopped → go to 2 (signals failed the test)
   └─ no → go to 2
2. CTR below norm?
   ├─ yes and % viewed ≥ norm → PACKAGING. Good video, weak click. Repackage (thumbnail first).
   ├─ yes and % viewed < norm → TOPIC or PROMISE: the idea itself is weak for this audience.
   └─ no → go to 3
3. Retention at 0:30 below ~65% (or below norm)?
   ├─ yes → PROMISE: the first seconds don't confirm the click (slow intro, wrong expectation,
   │        title/thumbnail promise not visible). Fix the hook pattern next time.
   └─ no → go to 4
4. Average % viewed below norm with a steady slope or cliffs?
   ├─ cliffs → BODY: find the timestamp; usually a tangent, a sponsor, a slow demo, a resolved loop.
   ├─ steady decline steeper than norm → BODY: pacing; too few re-hooks / visual changes.
   └─ no → go to 5
5. Good CTR + good retention but views flat?
   ├─ traffic mostly search → normal for evergreen; it will grow slowly. Improve search phrasing.
   ├─ traffic mostly external/notifications → not yet picked up by browse; give it time, then repackage.
   └─ → WORKING: make more like it. Send to youtube-idea-research as a seed.
```

## Shorts branch
- Viewed vs swiped away < ~60-70% → first second (hook) problem.
- Good viewed rate, low views → topic/format; test 3 different hooks on the same idea.
- Average percentage viewed > 100% means loops: that's good, replicate the ending style.

## Retention curve vocabulary
- **Initial drop**: % lost in the first 30 s. Promise problem.
- **Cliff**: sudden drop > ~5 points. Specific moment to fix.
- **Bump**: the curve rises. People rewound to rewatch: valuable moment, clip it as a Short.
- **End drop**: early drop before the end screen means the outro is too long or signals "it's over".
- **relativeRetentionPerformance**: compares with videos of similar length on YouTube; > 0.5 is above average.
