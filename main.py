#!/usr/bin/env python3
"""Entry point for the 27 November 2026 news poster.

The competition harness runs this file and expects the finished
poster to appear in its output directory.  The poster itself is
bundled next to this script as entry.png, so the job here is a
faithful copy: locate the bundled file, make sure the destination
directory exists, and copy the bytes across without modification.
Only the Python standard library is used, and because the source
image never changes, every run delivers exactly the same file.
"""

import os
import shutil

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(SCRIPT_DIR, "entry.png")
DEFAULT_DIR = "/output"
ENV_VAR = "MAKEFUN_OUTPUT_DIR"


def output_dir():
    chosen = os.environ.get(ENV_VAR, "").strip()
    return chosen if chosen else DEFAULT_DIR


def main():
    # Resolve the destination first, then create it only if needed.
    # The copy is byte-for-byte, so repeated runs stay identical.
    folder = output_dir()
    os.makedirs(folder, exist_ok=True)
    destination = os.path.join(folder, "entry.png")
    shutil.copyfile(SOURCE, destination)
    print("Entry delivered to", destination)
    return destination


if __name__ == "__main__":
    main()
