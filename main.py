#!/usr/bin/env python3
"""Deliver the finished poster for the 27 November 2026 edition.

The judges run this file on its own, in a bare Python container.
The artwork already sits next to it as entry.png, so delivering
the entry is just a careful file copy: figure out where the
output folder is, create it when it is not there yet, and stream
the PNG across unchanged.  Only the standard library is touched,
which keeps the two grading runs byte-for-byte identical.
"""

import shutil
from os import environ
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUNDLED_POSTER = HERE / "entry.png"
FALLBACK_FOLDER = Path("/output")
ENV_KEY = "MAKEFUN_OUTPUT_DIR"


def chosen_folder():
    # An empty or blank override counts as "not set".
    raw = environ.get(ENV_KEY, "").strip()
    return Path(raw) if raw else FALLBACK_FOLDER


def deliver():
    folder = chosen_folder()
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / "entry.png"
    with BUNDLED_POSTER.open("rb") as reading, target.open("wb") as writing:
        shutil.copyfileobj(reading, writing, length=64 * 1024)
    print("Poster delivered to", target)
    return target


if __name__ == "__main__":
    deliver()
