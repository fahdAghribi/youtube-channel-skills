# Project conventions: youtube-channel-skills

Read before changing this repository.

## Versioning

- Version lives in `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`; keep them equal.
- Default bump: PATCH for every shippable change. MINOR/MAJOR only when the owner asks.
- After bumping: `git tag -a vX.Y.Z -m "..."`, push the tag, `gh release create vX.Y.Z --notes "..."`.

## Before every commit

```bash
python3 scripts/check_skills.py        # frontmatter, references, script paths, skill count
python3 -m unittest discover -s tests  # offline tests, no network, no credentials
```

## Skill bundle invariants

- **10 skills**, all named `youtube-<name>`, folder name == frontmatter `name`.
- The count is announced in `plugin.json` description, root `SKILL.md` and README. Change all three together.
- Frontmatter `description` ≤ 500 chars, no em dashes, includes a "Not for X (use Y)" sentinel when a sibling overlaps.
- Only `youtube-publisher` and `youtube-comment-manager` may document write calls. Every write script must use `lib/approval.py` (dry run by default, `--confirm <fingerprint>` to execute).

## Reference layout

- Shared references: root `references/`. Cite from skills as `../../references/X.md`.
- Skill-local references: `skills/<skill>/references/`. Cite as `references/X.md`.
- Skill "Hard rules" sections start with `Global voice rules: see root SKILL.md §Voice rules.` and only add overrides.
- `references/metadata-limits.md` and `lib/metadata.py` must agree. Change both, add a test.

## Code

- `lib/` is importable without third-party packages; Google libraries are imported lazily inside functions.
- Scripts bootstrap with `import _common` (adds the repo root to `sys.path`).
- Never print secrets. Tokens live in `~/.config/youtube-channel-skills/`, never in the repo.
