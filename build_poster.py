#!/usr/bin/env python3
"""Poster generator for the Friday 27 November 2026 news edition.

The artwork is a single square page that reads like the front of a
broadsheet: a masthead naming the day, one dominant lead story, four
smaller stories arranged as a two-by-two grid, a wide markets panel
underneath, and a closing strip that sweeps up the rest of the day.
All of the wording lives in plain data structures below, and the
drawing helpers only care about boxes, fonts and wrapped lines, so
the editorial content can be swapped without touching the layout
machinery.  Every coordinate and string is fixed, which makes the
rendered PNG fully deterministic.
"""

import os

from PIL import Image, ImageDraw, ImageFont

PAGE = 1024
MARGIN = 36
CONTENT = PAGE - MARGIN * 2
GAP = 12

BACKGROUND = (8, 20, 38)
PANEL = (17, 38, 64)
PANEL_LINE = (55, 82, 114)
INK = (237, 242, 249)
MUTED = (169, 186, 206)
GOLD = (222, 184, 66)
RED = (236, 100, 84)
TEAL = (84, 201, 183)
SKY = (105, 183, 246)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
FONT_BOLD = "DejaVuSans-Bold.ttf"
FONT_PLAIN = "DejaVuSans.ttf"

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_FILE = os.path.join(HERE, "entry.png")

LEAD = {
    "kicker": "LEAD - NEW ZEALAND POLITICS",
    "headline": "NZ COALITION FALLS ONE SEAT SHORT",
    "body": (
        "Final official results give the National-led coalition 65 of "
        "130 seats, one short of a majority, after special votes cost "
        "it two seats. Prime Minister Christopher Luxon must now win "
        "support from the centrist Opportunity party to govern, or "
        "risk another election. Labour won the popular vote but lacks "
        "the seats to form a government."
    ),
    "accent": GOLD,
}

GRID = [
    {
        "kicker": "BANGLADESH - HASINA RETURN",
        "headline": "HASINA SETS RETURN DATE",
        "body": (
            "Ousted prime minister Sheikh Hasina, 79, sentenced to "
            "death in absentia, says she will return on 16 December, "
            "Victory Day, from Delhi, where she fled in August 2024. "
            "Dhaka says she would be arrested at once."
        ),
        "accent": RED,
    },
    {
        "kicker": "WEST BANK - DEMOLITIONS",
        "headline": "SAMRA HOMES DEMOLISHED",
        "body": (
            "Israeli forces demolish about 50 structures, including "
            "homes and livestock shelters, in the Palestinian farming "
            "community of Samra in Tubas, in the Jordan Valley of "
            "the occupied West Bank."
        ),
        "accent": TEAL,
    },
    {
        "kicker": "FRANCE - AFP CYBERATTACK",
        "headline": "AFP PLATFORM OFFLINE",
        "body": (
            "Agence France-Presse takes its AFP Forum content "
            "platform offline after a cyberattack that began at "
            "00:30 GMT, and opens an investigation into who was "
            "behind the intrusion."
        ),
        "accent": SKY,
    },
    {
        "kicker": "ARGENTINA - CENTRAL BANK",
        "headline": "PRINTING MONEY BARRED",
        "body": (
            "Argentina's Chamber of Deputies gives final approval "
            "to a bill barring the central bank from printing money "
            "to fund government spending, defining its main mission "
            "as maintaining the currency's value."
        ),
        "accent": GOLD,
    },
]

WIDE = {
    "kicker": "MARKETS - SHARES STEADIER, OIL UP",
    "headline": "MARKETS FIND FOOTING",
    "body": (
        "Asian shares edge higher after a bruising month of AI jitters, "
        "Brent crude holds near $96 a barrel and heads for its first "
        "weekly gain in four, and the dollar is set for a third monthly "
        "gain. Tokyo core inflation accelerates to 2.9% in November."
    ),
    "accent": TEAL,
}

ALSO = [
    "Turkey completes ratification of the Mecca defence pact with Pakistan and Saudi Arabia",
    "China tests new Taiwan landing tactics, linking civilian vessels into an 800-metre floating bridge in Fujian drills",
    "South Korea repatriates six North Koreans rescued from a drifting fishing boat; a seventh stays",
    "US Thanksgiving storm cancels nearly 400 flights and leaves 724,000 without power",
    "Two Italian technicians killed in a drone attack in Kuwait",
    "EU leaders split over the budget and a $49bn loan to Ukraine",
    "Australia sanctions two people over antisemitic attacks it blames on Iran",
    "Iran warns South Korea over an expanded naval role near the Gulf of Oman",
]


def load_font(size, bold=False):
    name = FONT_BOLD if bold else FONT_PLAIN
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def wrap(draw, text, font, width):
    lines = []
    current = ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=font) <= width or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_text_block(draw, x, y, text, font, colour, width, leading):
    for line in wrap(draw, text, font, width):
        draw.text((x, y), line, font=font, fill=colour)
        y += leading
    return y


def draw_panel(draw, x, y, width, height, story, headline_size, body_size):
    draw.rounded_rectangle(
        [x, y, x + width, y + height], radius=12,
        fill=PANEL, outline=PANEL_LINE, width=2,
    )
    draw.rectangle([x, y + 10, x + 5, y + 52], fill=story["accent"])
    inner = width - 34
    cursor = draw_text_block(
        draw, x + 17, y + 11, story["kicker"],
        load_font(14, bold=True), story["accent"], inner, 18,
    )
    cursor = draw_text_block(
        draw, x + 17, cursor + 2, story["headline"],
        load_font(headline_size, bold=True), INK, inner, headline_size + 4,
    )
    draw_text_block(
        draw, x + 17, cursor + 4, story["body"],
        load_font(body_size), MUTED, inner, body_size + 5,
    )


def centred(draw, text, y, size, colour):
    font = load_font(size, bold=True)
    w = draw.textlength(text, font=font)
    draw.text(((PAGE - w) / 2, y), text, font=font, fill=colour)


def build():
    # One fresh canvas per call: no state is shared between renders,
    # so two consecutive builds cannot drift apart.
    image = Image.new("RGB", (PAGE, PAGE), BACKGROUND)
    draw = ImageDraw.Draw(image)

    centred(draw, "THE WORLD IN ONE IMAGE", 22, 40, INK)
    centred(draw, "FRIDAY - 27 NOVEMBER 2026", 74, 21, GOLD)
    draw.rectangle([MARGIN, 110, PAGE - MARGIN, 114], fill=GOLD)

    y = 126
    draw_panel(draw, MARGIN, y, CONTENT, 182, LEAD, 29, 17)
    y += 182 + GAP

    half = (CONTENT - GAP) // 2
    for row in range(2):
        for col in range(2):
            story = GRID[row * 2 + col]
            draw_panel(
                draw, MARGIN + col * (half + GAP), y, half, 158,
                story, 19, 14,
            )
        y += 158 + GAP

    draw_panel(draw, MARGIN, y, CONTENT, 106, WIDE, 20, 15)
    y += 106 + GAP

    draw.rectangle([MARGIN, y, PAGE - MARGIN, y + 3], fill=GOLD)
    y = draw_text_block(
        draw, MARGIN, y + 11, "ALSO TODAY",
        load_font(16, bold=True), GOLD, CONTENT, 20,
    )
    joined = "  /  ".join(ALSO)
    draw_text_block(draw, MARGIN, y + 4, joined, load_font(14), INK, CONTENT, 19)

    # Footer names the source day so a thumbnail still dates the page.
    centred(draw, "Wire reports of 27 November 2026 - One page, one day", 990, 13, MUTED)
    image.save(OUT_FILE, format="PNG")
    return OUT_FILE


if __name__ == "__main__":
    print("Poster saved to", build())
