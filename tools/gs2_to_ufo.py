#!/usr/bin/env python3
"""Convert Fluma's Glyphr Studio JSON source to an editable UFO source."""

import argparse
import json
import math
import unicodedata
from pathlib import Path

from fontTools.agl import UV2AGL
from fontTools.misc.roundTools import otRound
from ufoLib2 import Font
from ufoLib2.objects import Anchor


def glyph_name(codepoint):
    return UV2AGL.get(codepoint, f"uni{codepoint:04X}")


def key_to_name(key):
    if key.startswith("glyph-0x"):
        return glyph_name(int(key.removeprefix("glyph-0x"), 16))
    if key.startswith("comp-"):
        return f"_component{key.removeprefix('comp-')}"
    raise ValueError(f"Unsupported Glyphr reference: {key}")


def point_coord(point, handle="p"):
    value = point[handle]["coord"]
    return float(value["x"]), float(value["y"])


def draw_path(pen, points):
    if len(points) < 2:
        raise ValueError("A path needs at least two on-curve points")
    pen.moveTo(point_coord(points[0]))
    for index, start in enumerate(points):
        end = points[(index + 1) % len(points)]
        p0 = point_coord(start)
        p3 = point_coord(end)
        p1 = point_coord(start, "h2") if start["h2"].get("use", True) else p0
        p2 = point_coord(end, "h1") if end["h1"].get("use", True) else p3
        if p0 == p1 and p2 == p3:
            # Glyphr/Illustrator can leave sub-unit line fragments. Their
            # endpoints become identical in the integer TrueType outline,
            # creating zero-length segments in otherwise valid contours.
            if p0 != p3 and tuple(map(otRound, p0)) != tuple(map(otRound, p3)):
                pen.lineTo(p3)
        else:
            pen.curveTo(p1, p2, p3)
    pen.closePath()


def draw_shapes(glyph, shapes):
    pen = glyph.getPen()
    for shape in shapes:
        if "link" in shape:
            pen.addComponent(
                key_to_name(shape["link"]),
                (1, 0, 0, 1, float(shape.get("translateX", 0)), float(shape.get("translateY", 0))),
            )
        elif "pathPoints" in shape:
            draw_path(pen, shape["pathPoints"])
        else:
            raise ValueError(f"Unsupported shape in {glyph.name}: {shape.keys()}")


def add_notdef(font):
    glyph = font.newGlyph(".notdef")
    glyph.width = 1000
    pen = glyph.getPen()
    pen.moveTo((100, 0))
    pen.lineTo((900, 0))
    pen.lineTo((900, 1500))
    pen.lineTo((100, 1500))
    pen.closePath()
    pen.moveTo((230, 130))
    pen.lineTo((230, 1370))
    pen.lineTo((770, 1370))
    pen.lineTo((770, 130))
    pen.closePath()


def add_dotted_circle(font):
    """Generate a functional support glyph for isolated combining marks."""
    glyph = font.newGlyph(glyph_name(0x25CC))
    glyph.unicodes = [0x25CC]
    glyph.width = 1000
    pen = glyph.getPen()
    radius = 43
    kappa = 0.5522847498
    def point(x, y):
        # Avoid platform-specific last-bit trig differences in the committed UFO.
        return (round(x, 6), round(y, 6))

    for index in range(12):
        angle = 2 * math.pi * index / 12
        cx = 500 + 330 * math.cos(angle)
        cy = 500 + 330 * math.sin(angle)
        pen.moveTo(point(cx + radius, cy))
        pen.curveTo(point(cx + radius, cy + kappa * radius), point(cx + kappa * radius, cy + radius), point(cx, cy + radius))
        pen.curveTo(point(cx - kappa * radius, cy + radius), point(cx - radius, cy + kappa * radius), point(cx - radius, cy))
        pen.curveTo(point(cx - radius, cy - kappa * radius), point(cx - kappa * radius, cy - radius), point(cx, cy - radius))
        pen.curveTo(point(cx + kappa * radius, cy - radius), point(cx + radius, cy - kappa * radius), point(cx + radius, cy))
        pen.closePath()
    glyph.appendAnchor(Anchor(x=500, y=1053, name="top"))
    glyph.appendAnchor(Anchor(x=500, y=-85, name="bottom"))
    return glyph.name


def add_mark_anchors_and_ccmp(font, source):
    marks = [cp for cp in (int(key.removeprefix("glyph-0x"), 16) for key in source["glyphs"])
             if unicodedata.category(chr(cp)) == "Mn"]
    top_marks = []
    for cp in marks:
        glyph = font[glyph_name(cp)]
        bounds = glyph.getBounds(font.layers.defaultLayer)
        if bounds is None:
            raise ValueError(f"Combining mark U+{cp:04X} has no outline")
        x_min, y_min, x_max, y_max = bounds
        below = cp in (0x0326, 0x0327, 0x0328)
        glyph.appendAnchor(Anchor(x=round((x_min + x_max) / 2), y=round(y_max if below else y_min),
                                  name="_bottom" if below else "_top"))
        if not below:
            top_marks.append(glyph.name)

    bare_bases = list(range(ord("A"), ord("Z") + 1)) + list(range(ord("a"), ord("z") + 1))
    bare_bases += [0x0131, 0x0237]
    for cp in bare_bases:
        glyph = font[glyph_name(cp)]
        tall = chr(cp).isupper() or cp in (ord("b"), ord("d"), ord("f"), ord("h"), ord("k"), ord("l"), ord("t"))
        glyph.appendAnchor(Anchor(x=round(glyph.width / 2), y=1559 if tall else 1053, name="top"))
        bounds = glyph.getBounds(font.layers.defaultLayer)
        bottom = min(-85, round(bounds[1]) - 85) if bounds else -85
        glyph.appendAnchor(Anchor(x=round(glyph.width / 2), y=bottom, name="bottom"))

    # U+012F has the dot of i plus an ogonek. A combining top mark needs the
    # same ogonek with the dotless i outline underneath.
    iogonek = source["glyphs"]["glyph-0x12F"]
    alt = font.newGlyph("iogonek.dotless")
    alt.width = iogonek["advanceWidth"]
    shapes = [dict(shape) for shape in iogonek["shapes"]]
    assert shapes[0]["link"] == "glyph-0x69"
    shapes[0]["link"] = "glyph-0x131"
    draw_shapes(alt, shapes)
    alt.appendAnchor(Anchor(x=round(alt.width / 2), y=1053, name="top"))
    class_text = " ".join(top_marks)
    font.features.text = (
        "languagesystem DFLT dflt;\n"
        "languagesystem latn dflt;\n"
        f"@TopMarks = [{class_text}];\n"
        "feature ccmp {\n"
        f"  sub {glyph_name(0x0069)}' @TopMarks by {glyph_name(0x0131)};\n"
        f"  sub {glyph_name(0x006A)}' @TopMarks by {glyph_name(0x0237)};\n"
        f"  sub {glyph_name(0x012F)}' @TopMarks by iogonek.dotless;\n"
        "} ccmp;\n"
    )
    font.lib["public.openTypeCategories"] = {
        glyph_name(cp): "mark" if cp in marks else "base"
        for cp in (int(key.removeprefix("glyph-0x"), 16) for key in source["glyphs"])
    }
    font.lib["public.openTypeCategories"]["iogonek.dotless"] = "base"
    font.lib["public.openTypeCategories"][glyph_name(0x25CC)] = "base"


def convert(source_path, output_path):
    source = json.loads(source_path.read_text(encoding="utf-8"))
    settings = source["settings"]["font"]
    font = Font()
    info = font.info
    info.familyName = settings["family"]
    info.styleName = settings["style"]
    info.unitsPerEm = settings["upm"]
    info.ascender = settings["ascent"]
    info.descender = settings["descent"]
    info.capHeight = settings["capHeight"]
    info.xHeight = settings["xHeight"]
    info.copyright = settings["copyright"]
    info.openTypeNameLicense = settings["license"]
    info.openTypeNameLicenseURL = settings["licenseURL"]
    info.openTypeNameDesigner = settings["designer"]
    info.openTypeNameDesignerURL = settings["designerURL"]
    info.openTypeNameManufacturer = settings["manufacturer"]
    info.openTypeNameManufacturerURL = settings["manufacturerURL"]
    info.openTypeNameDescription = settings["description"]
    info.openTypeNameVersion = f"Version {settings['version']}"
    info.openTypeNameUniqueID = f"{settings['version']};BaturayKocatepe;Fluma-Regular"
    info.postscriptFontName = "Fluma-Regular"
    info.postscriptFullName = "Fluma Regular"
    info.openTypeNameCompatibleFullName = "Fluma Regular"
    info.versionMajor, info.versionMinor = (int(part) for part in settings["version"].split("."))
    info.openTypeOS2WeightClass = settings["weight"]
    info.openTypeOS2WidthClass = 5
    info.openTypeOS2TypoAscender = settings["ascent"]
    info.openTypeOS2TypoDescender = settings["descent"]
    info.openTypeOS2TypoLineGap = settings["lineGap"]
    info.openTypeHheaAscender = settings["ascent"]
    info.openTypeHheaDescender = settings["descent"]
    info.openTypeHheaLineGap = settings["lineGap"]
    info.openTypeOS2WinAscent = 1928
    info.openTypeOS2WinDescent = 840
    info.openTypeOS2Type = []
    info.openTypeOS2Selection = [7, 8]
    # Google Fonts recommends grayscale/symmetric smoothing for unhinted statics.
    info.openTypeGaspRangeRecords = [{"rangeMaxPPEM": 65535, "rangeGaspBehavior": [1, 3]}]
    info.postscriptUnderlinePosition = settings["underlinePosition"]
    info.postscriptUnderlineThickness = settings["underlineThickness"]

    add_notdef(font)
    order = [".notdef"]
    for key, entry in source["glyphs"].items():
        cp = int(key.removeprefix("glyph-0x"), 16)
        name = glyph_name(cp)
        glyph = font.newGlyph(name)
        glyph.unicodes = [cp]
        glyph.width = entry.get("advanceWidth", 0)
        draw_shapes(glyph, entry.get("shapes", []))
        order.append(name)
    referenced_components = {
        shape["link"] for entry in source["glyphs"].values()
        for shape in entry.get("shapes", []) if shape.get("link", "").startswith("comp-")
    }
    for key, entry in source["components"].items():
        if key not in referenced_components:
            continue
        name = key_to_name(key)
        glyph = font.newGlyph(name)
        glyph.width = entry.get("advanceWidth", 0)
        draw_shapes(glyph, entry.get("shapes", []))
        order.append(name)
    order.append(add_dotted_circle(font))

    for entry in source["kerning"].values():
        for left in entry["leftGroup"]:
            for right in entry["rightGroup"]:
                pair = (glyph_name(int(left, 16)), glyph_name(int(right, 16)))
                font.kerning[pair] = entry["value"]
    add_mark_anchors_and_ccmp(font, source)
    order.append("iogonek.dotless")
    font.lib["public.glyphOrder"] = order
    font.lib["public.skipExportGlyphs"] = [name for name in order if name.startswith("_component")]
    font.save(output_path, overwrite=True)
    print(f"Wrote {output_path}: {len(source['glyphs'])} encoded glyphs, {len(referenced_components)} used components")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    convert(args.source, args.output)
