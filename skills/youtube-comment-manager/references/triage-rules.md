# Comment triage rules

| Class | Signals | Action |
|---|---|---|
| Question | "?", how/why/what/cómo/por qué/qué, asks for a resource | Reply with the answer or the timestamp; idea if recurring |
| Praise (specific) | mentions a moment, result, detail | Short personal reply; heart |
| Praise (generic) | "great video", emoji only | Heart in Studio, no reply needed |
| Feedback | suggests an improvement (audio, pacing, length) | Thank + say what you'll try; log it |
| Idea / request | "can you make a video about..." | Reply, add to backlog |
| Criticism | disagrees, points out an error | Acknowledge; correct with source or concede; never defensive |
| Troll | insult with no content | No reply; `heldForReview` only if abusive |
| Spam / scam | links, WhatsApp/Telegram/crypto, "contact me", look-alike of the creator's name/avatar | `rejected`; propose `ban_author` for impersonation |

## Impersonation pattern (very common)

A commenter whose name or avatar copies the creator's, replying "Congratulations, you've
been selected, message me on Telegram". Always `rejected` + `ban_author: true` (after user OK),
and suggest the user enables "Hold potentially inappropriate comments" and adds blocked words
(telegram, whatsapp, crypto, the creator's name variants) in Studio > Settings > Community.
