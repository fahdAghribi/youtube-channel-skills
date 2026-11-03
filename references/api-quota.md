# YouTube API quota and gotchas

Default quota: **10,000 units/day per Google Cloud project**, reset at midnight
Pacific Time. Costs below are the commonly documented values; check the current
[quota calculator](https://developers.google.com/youtube/v3/determine_quota_cost)
because Google adjusts them.

| Call | Units (approx.) | Used by |
|---|---|---|
| `videos.list`, `channels.list`, `playlistItems.list`, `commentThreads.list` | 1 | research, comments, publisher |
| `search.list` | 100 | `research_outliers.py --search` (use sparingly) |
| `videos.insert` (upload) | high (historically 1,600) | `publish_video.py` |
| `videos.update` | 50 | `update_video.py` |
| `thumbnails.set` | 50 | publisher |
| `playlistItems.insert` | 50 | publisher |
| `comments.insert` (reply) | 50 | `reply_comments.py` |
| `comments.setModerationStatus` | 50 | `reply_comments.py` |
| Analytics API `reports.query` | separate quota | `analytics_report.py` |

## Gotchas

1. **Unverified API projects upload as private.** Projects created after 28 Jul 2020
   that have not passed YouTube's API compliance audit get uploads locked to
   *private*, whatever `privacyStatus` says. For a personal channel: upload private via
   the script, then switch visibility in Studio, or apply for the audit.
2. **Custom thumbnails need a verified channel** (phone verification / intermediate features).
3. **Pin comment, heart comment, end screens, cards, Test & Compare, Shorts remix settings**
   are Studio-only. Skills output ready-to-paste text and a checklist instead.
4. **Brand Accounts:** during `scripts/auth.py` pick the *channel*, not only the Google account.
   `check_config.py` prints which channel the token controls; confirm it before any write.
5. **Comment threads are one level deep.** Replies always go to the top-level comment id.
6. **`videos.update` replaces the snippet.** `lib.youtube_client.ChannelClient.update_video`
   merges with the current snippet first so untouched fields survive.
7. **Analytics lag ~48 h** and impressions/CTR are not in the query API (Studio export or
   the bulk Reporting API).
8. **Shorts detection** is automatic (vertical/square, ≤ 3 min). `#Shorts` in the title is optional.
