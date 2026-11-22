# The World in One Day — Sunday 22 November 2026

[![make.fun](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122)
[![Rank](https://make.fun/badge/news-image-20261122/adeqaila/makefun-news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122)
[![Reward](https://make.fun/badge/news-image-20261122/adeqaila/makefun-news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122)

Entry for make.fun bounty **news-image-20261122**: "Sum up 22 November's
world news in one image". $100, top 50 paid (1st $20). Deadline Tue 24 Nov
2026 00:00 UTC.

## What it is

A dense newspaper front page (1024×1024 PNG) summing up the day in 36
verified stories across 7 regions: 3 illustrated hero stories (COP31 still
without a deal in Antalya; the Russian cargo ship Sparta II ablaze in the
Baltic after a drone strike; Iran saying it downed two US drones over
Hormuz), 10 more illustrated panels, a world map with numbered story dots,
23 more stories in the ALSO list, a BY THE CLOCK timeline, and a DATE CHECK
box that dates the Saturday items honestly and lists what was left out as
other days' news.

## How it is built

- `compose.py` renders `entry.png` from the story data (stdlib + PIL,
  no network, fully deterministic — two runs produce identical bytes).
  All artwork is drawn with PIL primitives; all text is real text.
- `main.py` (stdlib only) copies `entry.png` to the grader's output
  directory as `entry.png`.
- `AUDIT.md` documents every story, its source, and the items checked
  and rejected as not-22-November news.

## Verify locally

```bash
python3 compose.py            # renders entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
python3 -c "from PIL import Image; im = Image.open('out/entry.png'); print(im.size)"
```

## License

MIT — see LICENSE.
