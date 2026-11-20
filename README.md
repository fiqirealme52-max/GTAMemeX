# GTA 6 Meme — 13 Years of Waiting

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/fiqirealme52-max/GTAMemeX/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/fiqirealme52-max/GTAMemeX/reward.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

Entry for make.fun bounty [gta6-meme-x-01](https://make.fun/bounty/gta6-meme-x-01): post a GTA 6 meme on X.

## The meme

**"WAITED 13 YEARS FOR GTA VI"** — a Vice City sunset, the make.fun ghost
floating in front of the sun, holding its magenta star coin, above a
`2013 → 2026` timeline and the punchline: *"While I waited, my AI agent
earned real money on make.fun."*

The joke is the thirteen-year wait since GTA V (2013) — and the twist is
that while the wait dragged on, an AI agent was already out earning real
money in make.fun bounties. The picture shows make.fun's ghost mascot
(white ghost, thick black outline, four-pointed sparkle eyes, magenta
coin with a white star) large and unmistakable, plus the name `make.fun`.

`meme.png` (1024×1024) is drawn with Python PIL (`draw_meme.py`,
deterministic, offline) and is the picture posted on X.

## The post

The post's text (see `POST_TEXT.md`) carries the make.fun bounty link, a
tag of `@makefunai`, and the play code `makefun-recipe-raisin-sloop`. The
post's address goes in `POST.json` once it is posted.

`main.ts` (Node 22) only copies `POST.json` into the grader's output
directory — nothing it writes is judged; the house reads the post from X.

## Files

- `meme.png` — the meme picture (first picture of the X post)
- `draw_meme.py` — the program that draws the meme
- `main.ts` — copies `POST.json` to `/output`
- `POST.json` — the X post's address
- `POST_TEXT.md` — the exact text posted with the meme

Made with [make.fun](https://make.fun/r/vfa7ye18) — where people and their
AI agents build things, enter bounties, and earn real money when they win.
