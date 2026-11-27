#!/usr/bin/env python3
"""Draw the 27 November 2026 front page from scratch.

I keep the whole edition in this one module: the stories sit in
plain tuples near the top, and a small canvas class underneath
turns them into a 1024-pixel square.  Nothing is read from disk
besides the DejaVu fonts, and nothing about the drawing depends
on the clock or on randomness, so re-running the script always
produces the same PNG bytes.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SIDE = 1024
EDGE = 36
COLUMN_WIDTH = SIDE - EDGE * 2
ROW_GAP = 12

COLOURS = {
    "page": (8, 20, 38),
    "card": (17, 38, 64),
    "frame": (55, 82, 114),
    "text": (237, 242, 249),
    "soft": (169, 186, 206),
    "gold": (222, 184, 66),
    "coral": (236, 100, 84),
    "mint": (84, 201, 183),
    "sky": (105, 183, 246),
}

FONT_FILES = {
    True: "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    False: "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
}

# Each story is (section label, headline, summary, accent colour).
TOP_STORY = (
    "LEAD - NEW ZEALAND POLITICS",
    "NZ COALITION FALLS ONE SEAT SHORT",
    "Final official results give the National-led coalition 65 of "
    "130 seats, one short of a majority, after special votes cost "
    "it two seats. Prime Minister Christopher Luxon must now win "
    "support from the centrist Opportunity party to govern, or "
    "risk another election. Labour won the popular vote but lacks "
    "the seats to form a government.",
    "gold",
)

MIDDLE_STORIES = [
    (
        "BANGLADESH - HASINA RETURN",
        "HASINA SETS RETURN DATE",
        "Ousted prime minister Sheikh Hasina, 79, sentenced to "
        "death in absentia, says she will return on 16 December, "
        "Victory Day, from Delhi, where she fled in August 2024. "
        "Dhaka says she would be arrested at once.",
        "coral",
    ),
    (
        "WEST BANK - DEMOLITIONS",
        "SAMRA HOMES DEMOLISHED",
        "Israeli forces demolish about 50 structures, including "
        "homes and livestock shelters, in the Palestinian farming "
        "community of Samra in Tubas, in the Jordan Valley of "
        "the occupied West Bank.",
        "mint",
    ),
    (
        "FRANCE - AFP CYBERATTACK",
        "AFP PLATFORM OFFLINE",
        "Agence France-Presse takes its AFP Forum content "
        "platform offline after a cyberattack that began at "
        "00:30 GMT, and opens an investigation into who was "
        "behind the intrusion.",
        "sky",
    ),
    (
        "ARGENTINA - CENTRAL BANK",
        "PRINTING MONEY BARRED",
        "Argentina's Chamber of Deputies gives final approval "
        "to a bill barring the central bank from printing money "
        "to fund government spending, defining its main mission "
        "as maintaining the currency's value.",
        "gold",
    ),
]

MARKET_STORY = (
    "MARKETS - SHARES STEADIER, OIL UP",
    "MARKETS FIND FOOTING",
    "Asian shares edge higher after a bruising month of AI jitters, "
    "Brent crude holds near $96 a barrel and heads for its first "
    "weekly gain in four, and the dollar is set for a third monthly "
    "gain. Tokyo core inflation accelerates to 2.9% in November.",
    "mint",
)

SHORT_ITEMS = [
    "Turkey completes ratification of the Mecca defence pact with Pakistan and Saudi Arabia",
    "China tests new Taiwan landing tactics, linking civilian vessels into an 800-metre floating bridge in Fujian drills",
    "South Korea repatriates six North Koreans rescued from a drifting fishing boat; a seventh stays",
    "US Thanksgiving storm cancels nearly 400 flights and leaves 724,000 without power",
    "Two Italian technicians killed in a drone attack in Kuwait",
    "EU leaders split over the budget and a $49bn loan to Ukraine",
    "Australia sanctions two people over antisemitic attacks it blames on Iran",
    "Iran warns South Korea over an expanded naval role near the Gulf of Oman",
]

TARGET = Path(__file__).resolve().parent / "entry.png"


class FrontPage:
    """Accumulates one edition onto a Pillow canvas, top to bottom."""

    def __init__(self):
        self.picture = Image.new("RGB", (SIDE, SIDE), COLOURS["page"])
        self.pen = ImageDraw.Draw(self.picture)
        self.cursor = 0

    @staticmethod
    def typeface(points, bold=False):
        return ImageFont.truetype(FONT_FILES[bold], points)

    def measure(self, wording, face):
        return self.pen.textlength(wording, font=face)

    def split_lines(self, wording, face, limit):
        # Greedy line breaking measured in pixels, word by word.
        queue = wording.split()
        finished = []
        while queue:
            line = queue.pop(0)
            while queue and self.measure(line + " " + queue[0], face) <= limit:
                line = line + " " + queue.pop(0)
            finished.append(line)
        return finished

    def put_lines(self, left, top, wording, face, colour, limit, step):
        height = top
        for row in self.split_lines(wording, face, limit):
            self.pen.text((left, height), row, font=face, fill=colour)
            height += step
        return height

    def centred_line(self, wording, top, points, colour_key):
        face = self.typeface(points, bold=True)
        start = (SIDE - self.measure(wording, face)) / 2
        self.pen.text((start, top), wording, font=face, fill=COLOURS[colour_key])

    def header(self):
        self.centred_line("THE WORLD IN ONE IMAGE", 22, 40, "text")
        self.centred_line("FRIDAY - 27 NOVEMBER 2026", 74, 21, "gold")
        self.pen.rectangle(
            [EDGE, 110, SIDE - EDGE, 114], fill=COLOURS["gold"]
        )
        self.cursor = 126

    def card(self, left, top, width, height, story, title_points, body_points):
        label, headline, summary, accent_key = story
        accent = COLOURS[accent_key]
        box = [left, top, left + width, top + height]
        self.pen.rounded_rectangle(
            box, radius=12, fill=COLOURS["card"],
            outline=COLOURS["frame"], width=2,
        )
        self.pen.rectangle([left, top + 10, left + 5, top + 52], fill=accent)
        room = width - 34
        y = self.put_lines(
            left + 17, top + 11, label,
            self.typeface(14, bold=True), accent, room, 18,
        )
        y = self.put_lines(
            left + 17, y + 2, headline,
            self.typeface(title_points, bold=True),
            COLOURS["text"], room, title_points + 4,
        )
        self.put_lines(
            left + 17, y + 4, summary,
            self.typeface(body_points), COLOURS["soft"],
            room, body_points + 5,
        )

    def assemble(self):
        # Placement is strictly sequential: header, lead, the four
        # middle cards in reading order, markets, then the strip.
        self.header()
        self.card(EDGE, self.cursor, COLUMN_WIDTH, 182, TOP_STORY, 29, 17)
        self.cursor += 182 + ROW_GAP

        pair_width = (COLUMN_WIDTH - ROW_GAP) // 2
        for index, story in enumerate(MIDDLE_STORIES):
            column = index % 2
            if index == 2:
                self.cursor += 158 + ROW_GAP
            left = EDGE + column * (pair_width + ROW_GAP)
            self.card(left, self.cursor, pair_width, 158, story, 19, 14)
        self.cursor += 158 + ROW_GAP

        self.card(EDGE, self.cursor, COLUMN_WIDTH, 106, MARKET_STORY, 20, 15)
        self.cursor += 106 + ROW_GAP

        self.pen.rectangle(
            [EDGE, self.cursor, SIDE - EDGE, self.cursor + 3],
            fill=COLOURS["gold"],
        )
        y = self.put_lines(
            EDGE, self.cursor + 11, "ALSO TODAY",
            self.typeface(16, bold=True), COLOURS["gold"], COLUMN_WIDTH, 20,
        )
        self.put_lines(
            EDGE, y + 4, "  /  ".join(SHORT_ITEMS),
            self.typeface(14), COLOURS["text"], COLUMN_WIDTH, 19,
        )
        self.centred_line(
            "Wire reports of 27 November 2026 - One page, one day",
            990, 13, "soft",
        )
        return self.picture


def render():
    edition = FrontPage()
    edition.assemble().save(TARGET, format="PNG")
    return TARGET


if __name__ == "__main__":
    print("Wrote", render())
