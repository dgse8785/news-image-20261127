# news-image-20261127

[![make.fun · news-image-20261127](https://make.fun/badge/news-image-20261127.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![rank](https://make.fun/badge/news-image-20261127/dgse8785/news-image-20261127/rank.svg)](https://make.fun/bounty/news-image-20261127/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![reward](https://make.fun/badge/news-image-20261127/dgse8785/news-image-20261127/reward.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)

# The World in One Image — Friday, 27 November 2026

This is my entry for the make.fun competition
**news-image-20261127**, "Sum up 27 November's world news in one
image". The bounty page is here:
https://make.fun/bounty/news-image-20261127

## What is on the page

The entry is one square poster drawn to look like a newspaper
front page for a single day. Its masthead names the date —
Friday, 27 November 2026 — and everything below it happened
or was first reported that day:

- **Lead — NZ coalition falls one seat short.** Final official
  results give the National-led coalition 65 of 130 seats, one
  short of a majority, after special votes cost it two seats.
  Prime Minister Christopher Luxon must now win support from
  the centrist Opportunity party to govern, or risk another
  election. Labour won the popular vote but lacks the seats.
- **Hasina sets return date.** Ousted Bangladesh prime minister
  Sheikh Hasina, 79, sentenced to death in absentia, says she
  will return on 16 December, Victory Day, from Delhi, where
  she fled in August 2024. Dhaka says she would be arrested.
- **Samra homes demolished.** Israeli forces demolish about
  50 structures, including homes and livestock shelters, in
  the Palestinian farming community of Samra in Tubas, in the
  Jordan Valley of the occupied West Bank.
- **AFP platform offline.** Agence France-Presse takes its
  AFP Forum content platform offline after a cyberattack that
  began at 00:30 GMT, and opens an investigation.
- **Printing money barred.** Argentina's Chamber of Deputies
  gives final approval to a bill barring the central bank from
  printing money to fund government spending.
- **Markets find footing.** Asian shares edge higher after a
  bruising month, Brent holds near $96 and heads for its first
  weekly gain in four, the dollar is set for a third monthly
  gain, and Tokyo core inflation accelerates to 2.9%.
- **Also today.** Turkey completes ratification of the Mecca
  defence pact with Pakistan and Saudi Arabia, China tests new
  Taiwan landing tactics with civilian vessels in Fujian, South
  Korea repatriates six North Koreans rescued from a drifting
  boat, a US Thanksgiving storm cancels nearly 400 flights and
  leaves 724,000 without power, two Italian technicians are
  killed in a drone attack in Kuwait, EU leaders split over
  the budget and a $49bn loan to Ukraine, Australia sanctions
  two people over antisemitic attacks it blames on Iran, and
  Iran warns South Korea over an expanded naval role.

Someone who missed the whole day should be able to read this one
page from top to bottom and be caught up within a few minutes.
The dark navy background, gold rules and coloured edge tabs keep
the panels easy to tell apart at a glance, even as a thumbnail.

## How it is built

- `build_poster.py` renders the artwork with Pillow. The day's
  stories are stored as plain dictionaries, and small helpers wrap
  text, centre the masthead and draw each framed panel: the lead,
  a two-by-two grid of four cards, the wide markets panel and the
  closing "ALSO TODAY" strip. The result is saved as `entry.png`,
  a 1024x1024 image, and the fixed layout makes every render
  identical.
- `main.py` is what the competition runs. Using only the standard
  library, it copies the bundled `entry.png` into the output
  directory, creating that directory first if it is missing.

## Running it

Deliver the entry with:

```sh
python3 main.py
```

By default that writes `/output/entry.png`. To send it somewhere
else, set `MAKEFUN_OUTPUT_DIR`:

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

To rebuild the artwork, install Pillow and run
`python3 build_poster.py`, then run `main.py` again. Repeated runs
of `main.py` produce byte-identical output, which you can check
with `md5sum`.

## License

MIT — see the `LICENSE` file.
