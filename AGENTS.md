# Agent instructions

Same conventions as `CLAUDE.md` (single source of truth). Summary for other agents (Codex, Cursor, etc.):

- The bundle router is `SKILL.md`; each skill lives in `skills/<name>/SKILL.md`.
- Read `references/channel-profile.md` before producing content.
- Write actions are two-pass: dry run → user approves the card → `--confirm <fingerprint>`. Never skip or fake the fingerprint.
- Validate before committing: `python3 scripts/check_skills.py && python3 -m unittest discover -s tests`.
