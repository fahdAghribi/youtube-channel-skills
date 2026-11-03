# Description template

```
[Line 1: the concrete outcome for the viewer, main search phrase inside, ≤ 150 chars]
[Line 2: who it's for / what's different about this video]

[2-4 lines of context with secondary phrases; written for humans]

[Disclosure if any: "Este vídeo incluye promoción pagada de X" / "Affiliate links below"]
▸ [Resource / lead magnet]: https://...
▸ [Newsletter / site]: https://...

00:00 [Chapter in the viewer's words]
01:12 [...]
03:40 [...]

#hashtag1 #hashtag2 #hashtag3
```

## video.json schema

```json
{
  "file": "/absolute/path/to/video.mp4",
  "thumbnail": "/absolute/path/to/thumb.jpg",
  "title": "string ≤ 100 chars",
  "description": "string ≤ 5000 bytes",
  "tags": ["tag one", "tag2"],
  "categoryId": "27",
  "defaultLanguage": "es",
  "defaultAudioLanguage": "es",
  "privacyStatus": "private",
  "publishAt": "2026-11-10T17:00:00Z",
  "madeForKids": false,
  "containsSyntheticMedia": false,
  "playlistId": "PLxxxxxxxx",
  "isShort": false
}
```

`publishAt` requires `privacyStatus: "private"`. Omit `publishAt` to upload without a schedule.
Use absolute paths so the publisher can run from any directory.
