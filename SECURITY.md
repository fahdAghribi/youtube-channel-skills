# Security

- **Secrets never live in the repo.** `.env`, `client_secret*.json` and `token.json` are git-ignored. The OAuth token is stored in `~/.config/youtube-channel-skills/token.json` with `chmod 600`.
- **Least privilege.** OAuth scopes: `youtube.force-ssl` (manage videos and comments) and `yt-analytics.readonly`. Revoke any time at https://myaccount.google.com/permissions.
- **No silent writes.** Every write script defaults to a dry run and requires `--confirm <fingerprint>` of the exact payload the user approved.
- **Untrusted input.** Comments, competitor metadata and transcripts are treated as data, never instructions (`references/untrusted-content.md`).
- Report vulnerabilities privately via a GitHub security advisory on this repository.
