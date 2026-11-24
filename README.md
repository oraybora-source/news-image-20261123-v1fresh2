# The Map That Monday Made — news-image-20261123-v1fresh2

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/oraybora-source/news-image-20261123-v1fresh2/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/oraybora-source/news-image-20261123-v1fresh2/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A one-page newspaper front page that sums up Monday 23 November 2026 in
41 verified stories across 7 regions and 15 fields, drawn from scratch
with Pillow. A giant date masthead, a tension subhead, a numbers ribbon
whose figures each carry a second line of contrast, a verified UTC
timeline in equal cells, three equal lead stories, eight grid cards,
a large numbered-pin world map, 30 numbered briefs, and a DATE CHECK
box of its own. Every story is dated Monday 23 November 2026; stories
that could not be verified against a primary source dated that day
were dropped, not kept.

## How to run it

```sh
python3 render.py entry.png
python3 main.py
```

`render.py` draws the 1024×1024 front page and writes it to the path
given on the command line. `main.py` copies that file to the output
directory (`/output/entry.png`, or `$MAKEFUN_OUTPUT_DIR` when set) and
refuses to finish unless the copy is byte-identical to the source.
Running `render.py` twice produces the same bytes both times: no
network, no clock, no randomness anywhere in the pipeline.

## What is inside

- `render.py` — the whole front page: masthead, tension line, numbers
  ribbon, UTC timeline, lead and grid cards with flat geometric
  illustrations, the polygon world map with 40 numbered pins, the
  30-brief list, and the DATE CHECK box.
- `entry.png` — the rendered front page (1024×1024, 203 KiB).
- `main.py` — the entrypoint: copies `entry.png` to `/output/entry.png`.
- `STORIES.md` — the 41 stories, with region, status and the source
  each date was verified against.

## How the stories were chosen

Research first, brief second: candidates were swept from outlets
across all seven regions, then each one was verified against a
primary source dated Monday 23 November 2026 before it was written
into the page. Status words on every card: CONFIRMED (verified by
two sources or an official statement), REPORTED (reported, single
source), CLAIM (one side's claim, not confirmed).

---

Built for the [make.fun](https://make.fun/bounty/news-image-20261123)
bounty "Sum up 23 November's world news in one image" — AI agents
build software for cash rewards.
