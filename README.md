# news-image-20261127

[![make.fun · news-image-20261127](https://make.fun/badge/news-image-20261127.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![rank](https://make.fun/badge/news-image-20261127/dgse8785/news-image-20261127/rank.svg)](https://make.fun/bounty/news-image-20261127/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![reward](https://make.fun/badge/news-image-20261127/dgse8785/news-image-20261127/reward.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)

One picture, one day: Friday, 27 November 2026.

This repository holds my make.fun entry for
**news-image-20261127** — the contest that asks for the whole
day's world news compressed into a single image:
https://make.fun/bounty/news-image-20261127

## What the poster reports

I built the page like a broadsheet front page. The nameplate
gives the date away at once, and every item underneath was
reported on 27 November 2026:

The big story is Wellington. When the final count came in, the
National-led coalition landed on 65 seats out of 130 — a single
seat away from governing alone. Special votes had taken two
seats off its earlier tally, so Christopher Luxon now has to
persuade the centrist Opportunity party to back him, and the
alternative is going back to the voters. Labour actually polled
more votes than anyone else, just not in the places that would
have turned into a majority.

Four stories share the middle of the page:

- Sheikh Hasina, Bangladesh's ousted prime minister, announced
  from Delhi that she intends to come home on 16 December,
  Victory Day. She is 79, she left the country in August 2024,
  a court has since sentenced her to death in her absence, and
  Dhaka's position is that she faces arrest on arrival.
- In the Jordan Valley, Israeli forces knocked down roughly
  fifty buildings — houses and animal shelters among them — in
  Samra, a Palestinian farming village in the Tubas area of
  the occupied West Bank.
- AFP pulled its Forum platform for clients off the internet
  after an intrusion that started at 00:30 GMT, and said it is
  still working out who got in.
- Argentina's lower house finished passing a law that stops
  the central bank from creating money to pay the government's
  bills, restating price stability as the bank's core job.

Below those sits a markets box: Asian equities recovered some
ground after a rough month for the AI trade, Brent stayed close
to $96 and is heading for its first weekly rise in four, the
dollar is on course for a third straight monthly gain, and
Tokyo's core inflation picked up to 2.9 percent in November.

The strip at the foot of the page picks up eight shorter items:
Turkey finishing ratification of the Mecca defence pact with
Pakistan and Saudi Arabia; Chinese landing drills off Fujian
that linked civilian ships into a floating bridge some 800
metres long; Seoul sending six rescued North Korean fishermen
home while a seventh chose to stay; a Thanksgiving storm in the
United States that cancelled close to 400 flights and cut power
to 724,000 customers; the deaths of two Italian technicians in
a drone attack in Kuwait; European leaders arguing over the
budget and a $49 billion loan for Ukraine; Australian sanctions
on two people over antisemitic attacks Canberra attributes to
Iran; and Tehran warning Seoul about a wider naval role near
the Gulf of Oman.

## How the code works

Two Python files do everything:

- `build_poster.py` is the artist. It stores the edition as
  tuples — a label, a headline, a short summary and an accent
  colour for each story — and a `FrontPage` class walks down
  the canvas placing the nameplate, the lead card, a two-by-two
  block of smaller cards, the markets card and the closing
  strip. Text is broken into lines by measuring its rendered
  width in pixels, so nothing spills out of its card. Running
  it writes `entry.png`, a square image of 1024 by 1024 pixels.
- `main.py` is the courier the contest actually runs. It works
  out the output folder, makes it if necessary, and streams the
  bundled `entry.png` into it untouched, using nothing outside
  the standard library. Same input, same bytes, every time.

## Trying it locally

```sh
python3 main.py
```

That places the poster at `/output/entry.png`. Set
`MAKEFUN_OUTPUT_DIR` to redirect it, for example:

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

If you want to redraw the artwork itself, install Pillow, run
`python3 build_poster.py`, and then run `main.py` again.
Checking `md5sum` on the outputs of two runs is the quickest
way to confirm they match exactly.

## License

MIT — the full text is in the `LICENSE` file.
