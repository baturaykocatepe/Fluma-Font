#!/usr/bin/env python3
"""Read-only audit of the Fluma source, exports, and local Latin Core list."""

import json
import re
from pathlib import Path

from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.ttLib import TTFont


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "sources/Fluma.gs2"
CORE = ROOT / "sources/GF_Latin_Core.nam"
FONT_PATHS = (
    ROOT / "fonts/ttf/Fluma-Regular.ttf",
    ROOT / "fonts/otf/Fluma-Regular.otf",
)
EXPECTED_EMPTY = {0x0020, 0x00A0}


def core_codepoints():
    values = []
    for line in CORE.read_text(encoding="utf-8").splitlines():
        match = re.match(r"\s*0x([0-9A-Fa-f]+)\b", line)
        if match:
            values.append(int(match.group(1), 16))
    return set(values)


def names(font, name_id):
    return sorted({entry.toUnicode().strip() for entry in font["name"].names if entry.nameID == name_id})


def has_outline(font, glyph_name):
    glyph_set = font.getGlyphSet()
    pen = DecomposingRecordingPen(glyph_set)
    glyph_set[glyph_name].draw(pen)
    return any(operation in {"lineTo", "curveTo", "qCurveTo"} for operation, _ in pen.value)


def codepoint_labels(values):
    return [f"U+{value:04X}" for value in sorted(values)]


def main():
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    settings = source["settings"]["font"]
    required = core_codepoints()
    license_header = (ROOT / "OFL.txt").read_text(encoding="utf-8").splitlines()[0]
    print(f"Local GF Latin Core: {len(required)} unique encoded codepoints")
    print(f"OFL header: {license_header}")
    print("Source empty glyphs:", [key for key, glyph in source["glyphs"].items() if not glyph.get("shapes")])
    print("Source metadata:", {key: settings.get(key) for key in ("copyright", "license", "licenseURL", "capHeight", "xHeight")})

    for path in FONT_PATHS:
        font = TTFont(path)
        cmap = font.getBestCmap()
        required_empty = {cp for cp in required & cmap.keys() if cp not in EXPECTED_EMPTY and not has_outline(font, cmap[cp])}
        all_empty = {cp for cp, glyph in cmap.items() if cp not in EXPECTED_EMPTY and not has_outline(font, glyph)}
        print(f"\n{path.relative_to(ROOT)}")
        print("  mapped/glyphs:", len(cmap), len(font.getGlyphOrder()))
        print("  missing core:", codepoint_labels(required - cmap.keys()))
        print("  empty core:", codepoint_labels(required_empty))
        print("  other empty mapped:", codepoint_labels(all_empty - required))
        print("  name 0 copyright:", names(font, 0))
        print("  name 13 license:", names(font, 13))
        print("  name 14 license URL:", names(font, 14))
        print("  copyright matches OFL:", names(font, 0) == [license_header])
        os2 = font["OS/2"]
        print("  source/export cap height:", settings.get("capHeight"), os2.sCapHeight)
        print("  source/export x-height:", settings.get("xHeight"), os2.sxHeight)


if __name__ == "__main__":
    main()
