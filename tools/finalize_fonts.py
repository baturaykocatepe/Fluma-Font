#!/usr/bin/env python3
"""Add reproducible static-font tables after fontmake compilation."""

import argparse
from pathlib import Path

from fontTools.otlLib.builder import buildStatTable
from fontTools.ttLib import TTFont, newTable


def finalize(path: Path) -> None:
    font = TTFont(path)

    # Fluma currently has one upright static style. An elidable value keeps
    # the regular menu name intact while satisfying STAT consumers.
    buildStatTable(
        font,
        [{"tag": "ital", "name": "Italic", "values": [{"value": 0, "name": "Roman", "flags": 0x2}]}],
    )

    meta = newTable("meta")
    meta.data = {"dlng": "Latn", "slng": "Latn"}
    font["meta"] = meta
    font.save(path)
    font.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fonts", nargs="+", type=Path)
    args = parser.parse_args()
    for font_path in args.fonts:
        finalize(font_path)
        print(f"Finalized {font_path}")
