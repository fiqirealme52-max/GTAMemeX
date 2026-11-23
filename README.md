# GTA 6 Meme — 13 Years of Waiting

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/fiqirealme52-max/GTAMemeX/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/fiqirealme52-max/GTAMemeX/reward.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

Entry for make.fun bounty [gta6-meme-x-01](https://make.fun/bounty/gta6-meme-x-01): post a GTA 6 meme on X.

## The meme

**"WANTED — GRAND THEFT AUTO VI"** — a "WANTED" poster from the
Leonida County Sheriff's Office for GRAND THEFT AUTO VI as the most
wanted fugitive, still at large since 2013: "DEAD OR ALIVE — PREFERABLY
OUT NOW", five gold stars for the wanted level, and a statement of fines
listing 7 priced charges with dotted leaders — 13 years on the run
($4,811.00), perjury over the "Fall 2025" oath ($2,025.00), evading a
214 GB download ($214.00), trespassing in Vice City since 2013
($2,013.00), 87 trailer rewatches ($87.00), impersonating a launch date
($13.13), and a mugshot with none on file ($0.00) — adding up to a
TOTAL DUE of **$9,163.13**. A red PAID stamp reading "PAID BY MY AI
AGENT" is stamped across the total, and a magenta footer band carries
the make.fun ghost and "PAID BY MY AI AGENT — with real money it won
in make.fun bounties" plus the make.fun pill.

The joke is the thirteen-year wait since GTA V (2013) — GTA VI is a
fugitive that has been on the run for 13 years and still hasn't shown
up — and the twist is that while the wait dragged on, an AI agent was
already out earning real money in make.fun bounties and paid the
$9,163.13 fine. The picture shows make.fun's ghost mascot (white
ghost, thick black outline, four-pointed sparkle eyes, magenta coin
with a white star) large and unmistakable in the footer band, plus the
name `make.fun`.

`meme-v5.png` (1024×1024) is composed deterministically with Python
PIL (`compose_meme_v5.py`, offline) — the poster, header, stars,
charges, total, stamp and footer band are all drawn in PIL so the
words come out exactly right.

## The post

The post's text (see `POST_TEXT.md`) carries the make.fun bounty link, a
tag of `@makefunai`, and the play code `makefun-recipe-raisin-sloop`. The
post's address goes in `POST.json` once it is posted.

`main.ts` (Node 22) only copies `POST.json` into the grader's output
directory — nothing it writes is judged; the house reads the post from X.

## Files

- `meme-v5.png` — the meme picture (first picture of the X post)
- `compose_meme_v5.py` — the program that composes the meme
- `main.ts` — copies `POST.json` to `/output`
- `POST.json` — the X post's address
- `POST_TEXT.md` — the exact text posted with the meme

Made with [make.fun](https://make.fun/r/vfa7ye18) — where people and their
AI agents build things, enter bounties, and earn real money when they win.
