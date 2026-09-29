#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fluma / Glyphr Studio - composite (accented) glyph auto-builder
=================================================================

What this does
---------------
Glyphr Studio has a native "Component / Component Instance" system
(https://www.glyphrstudio.com/help/pages/components.html) that is
functionally the same idea as FontForge's "Build Accented Glyph":
draw one accent mark ONCE as a "Component", then every accented
letter that uses it is just a Component Instance of the base letter
+ a Component Instance of the mark, positioned with an x/y offset.

This script automates the *placement* half of that workflow for the
entire "GF Latin Core" glyph set (Google Fonts' minimum required set
for onboarding - https://github.com/googlefonts/glyphsets), which is
also the set that gives you Turkish support (Ç ç Ğ ğ İ ı Ö ö Ş ş Ü ü)
plus most other European languages.

For every GF Latin Core character that is a Unicode NFD "base + mark"
composite (~145 of them):
  - if the base letter already exists in your project (it does, for
    all 145 - you already drew Basic Latin), it is referenced directly
  - if the required accent mark does not exist yet, a small PLACEHOLDER
    Component is created for it (you replace its shape once, by hand,
    in Glyphr Studio - every glyph using it updates automatically)
  - if the mark already exists (this script auto-detects that your
    "i" and "j" dots can be reused as the "dot above" / dieresis mark),
    no new drawing is needed at all
  - the new composite glyph is written into the project as two
    Component Instances with computed Δx/Δy, using YOUR project's own
    metrics (upm/ascent/descent/capHeight/xHeight)

Turkish-specific chars (İ, ı) are not part of Unicode's NFD
decomposition, so they're handled with two manual rules (also fully
automatic - see TURKISH_SPECIAL below).

What this does NOT do
----------------------
~79 GF Latin Core characters are NOT accent+base composites (currency
signs, quotation marks, ligatures like æ œ, stroke letters like ø ł đ,
ß, etc.) - those still need to be actually drawn. This script prints
that list at the end so you know exactly what's left.

Usage
-----
    python3 build_composites.py Fluma_-_Glyphr_Studio_Project.gs2 GF_Latin_Core.nam

Writes:
    Fluma_-_Glyphr_Studio_Project_with_composites.gs2

Open the output file in Glyphr Studio (Projects > Open Project) and
you'll see all the new glyphs already assembled and placed. Look for
Components whose name starts with "NEW MARK - " - those are the ones
you still need to draw (open them from the Components page).
"""

import json
import math
import os
import re
import sys
import unicodedata
from copy import deepcopy

# ---------------------------------------------------------------- config --

# Gap between an "above" mark and the letter is now PROPORTIONAL, not a flat
# number: a flat 55 upm gap is ~5.5% of x-height (1000) but only ~3.7% of
# cap-height (1480), so the exact same numeric gap reads as noticeably
# tighter above capitals (this is what made İ's dot look too close to the
# stem - test drive feedback). 0.055 is exactly 55/1000, so lowercase marks
# (measured against x-height) render pixel-identical to before; uppercase
# marks (measured against cap-height) now get a proportionally bigger gap.
MARK_GAP_ABOVE_RATIO = 55 / 1000  # = 0.055
MARK_GAP_BELOW = 15      # upm gap between baseline and top of a "below" mark
PLACEHOLDER_W = 260
PLACEHOLDER_H = 170
# how far apart a mark PAIR (dieresis, double acute) sits, as a fraction of
# one mark's own width. Must be > 1.0 or the two instances' bounding boxes
# overlap (a value of 0.85, like before, puts their centers CLOSER together
# than one mark-width, so they visibly merge - test drive feedback on Ö).
# 1.4 puts their centers 1.4 mark-widths apart, leaving a clear ~0.4-width
# gap between them.
PAIR_SPACING = 1.4

# Fluma's own "roundness signature": measured directly from the hand-drawn
# 'i'/'j' dot blobs already in this project (h1/h2 handle length divided by
# the chord length of the segment it belongs to, averaged over every curved
# segment of both dots -> ~0.447). The general letter outlines (r/f/t) sit
# lower on average (~0.33-0.38, since most of their points are gentle
# corners, not full round caps), but their actual rounded terminal points
# spike into the same 0.4-0.85 range as the dots. 0.45 is the representative
# constant for "this is a soft round blob", used below to build placeholder
# mark shapes with real curves instead of sharp diamond corners.
MARK_ROUNDNESS = 0.45

# Unicode combining-mark name -> (internal mark name, how many instances, attach side)
MARK_INFO = {
    "COMBINING ACUTE ACCENT":        ("acute", 1, "above"),
    "COMBINING GRAVE ACCENT":        ("grave", 1, "above"),
    "COMBINING CIRCUMFLEX ACCENT":   ("circumflex", 1, "above"),
    "COMBINING TILDE":               ("tilde", 1, "above"),
    "COMBINING MACRON":              ("macron", 1, "above"),
    "COMBINING BREVE":               ("breve", 1, "above"),
    "COMBINING DOT ABOVE":           ("dot", 1, "above"),          # reused from i/j
    "COMBINING DIAERESIS":           ("dot", 2, "above"),          # reused, x2
    "COMBINING RING ABOVE":          ("ring", 1, "above"),
    "COMBINING CARON":               ("caron", 1, "above"),
    "COMBINING DOUBLE ACUTE ACCENT": ("acute", 2, "above"),        # reused, x2
    "COMBINING OGONEK":              ("ogonek", 1, "below"),
    "COMBINING CEDILLA":             ("cedilla", 1, "below"),
    "COMBINING COMMA BELOW":         ("commabelow", 1, "below"),
}

# İ (dotted capital I) IS covered by Unicode NFD (-> I + combining dot above)
# so it's already handled by the generic loop below. ı (dotless small i) is
# NOT decomposable in Unicode terms, so it gets one manual rule here.
TURKISH_SPECIAL = [
    (0x0131, None, None),  # ı = dotless i -> handled as a stem copy, see build_dotless_i()
]


# ------------------------------------------------------------- gs2 helpers --

def glyph_key(cp):
    return f"glyph-0x{cp:X}"


def bbox_of_shape(shape):
    xs, ys = [], []
    for pt in shape.get("pathPoints", []):
        c = pt["p"]["coord"]
        xs.append(c["x"])
        ys.append(c["y"])
    return min(xs), max(xs), min(ys), max(ys)


def combined_bbox(shapes):
    """bbox across ALL paths of a multi-path shape list. Several marks
    (circumflex, tilde, ring, cedilla) are now more than one path, so
    anywhere that used to read shapes[0] alone needs this instead."""
    xs, ys = [], []
    for s in shapes:
        for pt in s.get("pathPoints", []):
            c = pt["p"]["coord"]
            xs.append(c["x"])
            ys.append(c["y"])
    return min(xs), max(xs), min(ys), max(ys)


def make_placeholder_shape():
    """A smooth, round blob placeholder centered at x=0, resting on y=0 -
    same silhouette (top/right/bottom/left corners) and same bounding box
    as the old sharp-cornered diamond, so accent-mark offset math in
    compute_offsets() is completely unaffected. But every corner is now a
    real "symmetric" curve point (h1/h2 equal length, exactly opposite
    directions - the standard "convert corner to smooth point" construction)
    using MARK_ROUNDNESS, Fluma's own measured roundness constant - so it
    reads as a soft swelling drop/blob like the rest of the font, not a
    hard-edged diamond. Replace the points of this shape (inside the
    Component, in Glyphr Studio) with your real mark artwork - position is
    already handled."""
    hw, h = PLACEHOLDER_W / 2, PLACEHOLDER_H
    corners = [(0, h), (hw, h * 0.45), (0, 0), (-hw, h * 0.45)]
    n = len(corners)

    def dist(ax, ay, bx, by):
        return math.hypot(bx - ax, by - ay)

    points = []
    for i, (x, y) in enumerate(corners):
        x_prev, y_prev = corners[(i - 1) % n]
        x_next, y_next = corners[(i + 1) % n]
        chord_prev = dist(x_prev, y_prev, x, y)
        chord_next = dist(x, y, x_next, y_next)

        # tangent direction through this point = straight line from the
        # previous corner to the next one (the usual rule for turning a
        # sharp corner into a smooth point)
        tx, ty = x_next - x_prev, y_next - y_prev
        t_len = math.hypot(tx, ty) or 1.0
        tx, ty = tx / t_len, ty / t_len

        # true "symmetric" point: h1 and h2 must be the same length and
        # point in exactly opposite directions
        hlen = MARK_ROUNDNESS * (chord_prev + chord_next) / 2

        points.append({
            "type": "symmetric",
            "p": {"coord": {"x": x, "y": y}},
            "h1": {"coord": {"x": x - tx * hlen, "y": y - ty * hlen}},
            "h2": {"coord": {"x": x + tx * hlen, "y": y + ty * hlen}},
        })

    return {"name": "Path 1", "pathPoints": points}


# ------------------------------------------------------ mark geometry --
# Every one of the 11 auto-generated marks below is built ONLY by rotating,
# mirroring, non-uniformly scaling and duplicating-and-placing copies of the
# exact same base blob from make_placeholder_shape() - no new points are
# drawn anywhere in this section. That keeps them all "family members" of
# the same roundness signature, while giving each a distinct, unmistakable
# silhouette (a leaning stroke, a caret, a flat bar, a hollow ring, ...).

def _apply(shape, fn):
    """Apply a 2D point transform fn(x,y)->(x,y) to every anchor/handle
    coordinate of a (deep-copied) shape."""
    s = deepcopy(shape)
    for pt in s["pathPoints"]:
        for key in ("p", "h1", "h2"):
            c = pt.get(key, {}).get("coord")
            if c is not None:
                c["x"], c["y"] = fn(c["x"], c["y"])
    return s


def mark_rotate(shape, deg, cx=0.0, cy=0.0):
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)

    def fn(x, y):
        x, y = x - cx, y - cy
        return (x * ca - y * sa + cx, x * sa + y * ca + cy)

    return _apply(shape, fn)


def mark_scale(shape, sx, sy, cx=0.0, cy=0.0):
    return _apply(shape, lambda x, y: ((x - cx) * sx + cx, (y - cy) * sy + cy))


def mark_translate(shape, dx, dy):
    return _apply(shape, lambda x, y: (x + dx, y + dy))


def mark_mirror_x(shape, cx=0.0):
    return mark_scale(shape, -1, 1, cx=cx, cy=0)


def mark_mirror_y(shape, cy=0.0):
    return mark_scale(shape, 1, -1, cx=0, cy=cy)


def mark_reverse_winding(shape):
    """Reverse contour direction without changing its geometry (reverses
    point order, swaps h1/h2 so tangents stay correct). Two overlapping
    paths need the SAME winding direction to read as one solid merged
    shape under a font's nonzero-winding fill rule, and OPPOSITE winding
    to read as a shape-with-a-hole (see make_ring below). Plain rotate/
    translate preserve winding automatically; mirror_x/mirror_y flip it,
    so any mirrored piece that overlaps an unmirrored sibling needs this
    to be called on it afterwards to restore a solid (non-holed) merge."""
    s = deepcopy(shape)
    pts = list(reversed(s["pathPoints"]))
    for pt in pts:
        pt["h1"], pt["h2"] = pt["h2"], pt["h1"]
    s["pathPoints"] = pts
    return s


def _label_paths(shapes):
    for i, s in enumerate(shapes):
        s["name"] = f"Path {i + 1}"
    return shapes


def make_mark_acute(stroke_weight):
    """A single lean stroke tilted up-and-right, like '/' - acute leans
    toward the letter it follows. The stroke's thin axis is set to Fluma's
    own measured stem weight (see measure_stroke_weight) so it reads as
    the same "pen" as the letters, not a thin decorative sliver.

    Angle note: a steep rotation (the original -35 deg) makes the
    bounding box's thin-axis dimension mathematically INDEPENDENT of the
    thin-axis scale - for this 4-corner symmetric shape, the two corners
    that end up defining that extent are exactly as far apart after
    rotation regardless of how narrow/wide the shape started, because
    their scale-driven offsets cancel out in the subtraction. Checked
    numerically: at -35 deg, doubling the thickness moved the rendered
    width by exactly 0.00 upm. -15 deg keeps a visible "/" lean while
    giving thickness a real, checked effect (~+17 upm for this project's
    stroke-weight change, instead of +0)."""
    sx = stroke_weight / PLACEHOLDER_W
    s = mark_scale(make_placeholder_shape(), sx, 1.15)
    s = mark_rotate(s, -15)
    return _label_paths([s])


def make_mark_grave(stroke_weight):
    """acute mirrored left-right - same stroke, opposite lean, like '\\'."""
    return _label_paths([mark_mirror_x(make_mark_acute(stroke_weight)[0])])


def make_mark_circumflex(stroke_weight):
    """Two narrow arms meeting at a shared top point - a '^' caret. Both
    arms are rotated (not mirrored) around their own tip so the tip stays
    fixed and only the foot swings out; the right arm is then mirrored for
    its outward lean and re-would (mark_reverse_winding) so the two arms,
    which overlap slightly right at the apex, merge solid instead of
    notching a hole into the peak. Arm thickness = measured stroke weight
    (angle reduced from the original -50 to -28 for the same reason as
    acute above - checked numerically that -50 made the arm's rendered
    width totally insensitive to its thickness parameter; -28 keeps a
    clear caret peak while responding ~+22 upm to this project's actual
    thickness change)."""
    sx = stroke_weight / PLACEHOLDER_W
    arm = mark_scale(make_placeholder_shape(), sx, 0.95)
    _, _, _, top_y = bbox_of_shape(arm)
    left = mark_rotate(arm, -28, cx=0, cy=top_y)
    right = mark_reverse_winding(mark_mirror_x(left))
    return _label_paths([left, right])


def make_mark_tilde(stroke_weight):
    """Two narrow blobs, rotated opposite directions and overlapped, so
    together they read as one stretched S-shaped wave. Wave thickness =
    measured stroke weight."""
    sx = stroke_weight / PLACEHOLDER_W
    wave = mark_scale(make_placeholder_shape(), sx, 0.62)
    left = mark_rotate(wave, 38)
    right = mark_rotate(wave, -38)
    left = mark_translate(left, -12, 0)
    right = mark_translate(right, 12, 22)
    return _label_paths([left, right])


def make_mark_macron(stroke_weight):
    """The base blob squashed flat and stretched wide - a horizontal bar
    whose height is the measured stroke weight."""
    sy = stroke_weight / PLACEHOLDER_H
    return _label_paths([mark_scale(make_placeholder_shape(), 1.35, sy)])


def make_mark_ring(stroke_weight):
    """A smaller copy nested inside a bigger copy, with the inner one's
    winding reversed so it punches a hole instead of adding solid area -
    reads as a hollow ring. The ring wall's thickness is the measured
    stroke weight, same as every other mark."""
    outer = mark_scale(make_placeholder_shape(), 0.66, 0.98)
    ox0, ox1, oy0, oy1 = bbox_of_shape(outer)
    outer_w, outer_h = ox1 - ox0, oy1 - oy0
    inner = mark_scale(make_placeholder_shape(),
                        (outer_w - 2 * stroke_weight) / PLACEHOLDER_W,
                        (outer_h - 2 * stroke_weight) / PLACEHOLDER_H)
    _, _, iy0, iy1 = bbox_of_shape(inner)
    inner = mark_translate(inner, 0, (oy0 + oy1) / 2 - (iy0 + iy1) / 2)
    inner = mark_reverse_winding(inner)
    return _label_paths([outer, inner])


def make_mark_breve(stroke_weight):
    """A wide, plump, slightly tilted dome - deliberately rounder/taller
    than macron's flat bar so the two are never confused. Height = the
    measured stroke weight (this is the one Test Drive flagged as too
    thin - it now matches the letters' own stem weight).

    Angle note: the original 24 deg tilt made the rendered bounding box
    EXACTLY independent of this height parameter - proven algebraically
    and confirmed numerically (doubling the height moved the rendered
    box by 0.00 upm), the same effect as acute above but for the "wide
    flat shape" case instead of the "tall thin shape" case. 10 deg keeps
    a visible lean while actually responding to the measured thickness.
    Width also narrowed (1.05 -> 0.85): at the old width, the height
    increase alone was real but visually subtle (a still-quite-elongated
    ellipse just slightly less flat); narrowing it lets the added
    thickness read as genuinely plumper/rounder instead."""
    sy = stroke_weight / PLACEHOLDER_H
    s = mark_scale(make_placeholder_shape(), 0.85, sy)
    return _label_paths([mark_rotate(s, 10)])


def make_mark_caron(stroke_weight):
    """breve, flipped top-to-bottom - by construction, always exactly
    breve's opposite."""
    b = make_mark_breve(stroke_weight)[0]
    _, _, cy0, cy1 = bbox_of_shape(b)
    return _label_paths([mark_mirror_y(b, cy=(cy0 + cy1) / 2)])


def make_mark_cedilla(stroke_weight):
    """Two small overlapping blobs forming a short curling tail below the
    baseline - both built from pure rotation (no mirror) of the same
    piece, so they already share winding and merge solid. Piece height =
    measured stroke weight."""
    sy = stroke_weight / PLACEHOLDER_H
    hook = mark_scale(make_placeholder_shape(), 0.34, sy)
    top = mark_rotate(hook, 30)
    bottom = mark_rotate(hook, -75)
    top = mark_translate(top, -2, -2)
    bottom = mark_translate(bottom, 14, -58)
    return _label_paths([top, bottom])


def make_mark_commabelow(stroke_weight):
    """A small lean stroke below the baseline - the same idea as acute,
    at a smaller scale so it reads as a subtler mark. Thickness = measured
    stroke weight."""
    sx = stroke_weight / PLACEHOLDER_W
    s = mark_scale(make_placeholder_shape(), sx, 0.68)
    return _label_paths([mark_rotate(s, -32)])


def make_mark_ogonek(stroke_weight):
    """commabelow mirrored left-right - opposite lean, like acute/grave."""
    return _label_paths([mark_mirror_x(make_mark_commabelow(stroke_weight)[0])])


MARK_SHAPE_BUILDERS = {
    "acute": make_mark_acute,
    "grave": make_mark_grave,
    "circumflex": make_mark_circumflex,
    "tilde": make_mark_tilde,
    "macron": make_mark_macron,
    "ring": make_mark_ring,
    "breve": make_mark_breve,
    "caron": make_mark_caron,
    "cedilla": make_mark_cedilla,
    "commabelow": make_mark_commabelow,
    "ogonek": make_mark_ogonek,
}


def build_mark_shapes(mark_name, stroke_weight):
    """The distinct geometric shape for a given internal mark name, or a
    plain round blob as a safe fallback for any future mark this script
    doesn't have a specific recipe for yet."""
    builder = MARK_SHAPE_BUILDERS.get(mark_name)
    if builder:
        return builder(stroke_weight)
    return [make_placeholder_shape()]


# internal mark names that get an auto-generated placeholder Component (all
# of MARK_INFO's targets except "dot", which reuses your real hand-drawn
# i/j dot artwork instead - see find_existing_dot_component())
PLACEHOLDER_MARK_NAMES = sorted({name for name, _count, _side in MARK_INFO.values()} - {"dot"})


# Frozen snapshot of the PREVIOUS run's mark shapes (hardcoded thickness
# ratios, before they were tied to the measured stroke weight / before the
# dieresis spacing and gap-above fixes). Kept only so refresh detection
# below can recognize "still exactly what the last version of this script
# generated" as safe to upgrade, the same way it already recognizes the
# sharp-diamond and generic-round-blob generations before that.
def _legacy_make_mark_acute():
    s = mark_scale(make_placeholder_shape(), 0.30, 1.15)
    s = mark_rotate(s, -35)
    return _label_paths([s])


def _legacy_make_mark_grave():
    return _label_paths([mark_mirror_x(_legacy_make_mark_acute()[0])])


def _legacy_make_mark_circumflex():
    arm = mark_scale(make_placeholder_shape(), 0.22, 0.95)
    _, _, _, top_y = bbox_of_shape(arm)
    left = mark_rotate(arm, -50, cx=0, cy=top_y)
    right = mark_reverse_winding(mark_mirror_x(left))
    return _label_paths([left, right])


def _legacy_make_mark_tilde():
    wave = mark_scale(make_placeholder_shape(), 0.34, 0.62)
    left = mark_rotate(wave, 38)
    right = mark_rotate(wave, -38)
    left = mark_translate(left, -12, 0)
    right = mark_translate(right, 12, 22)
    return _label_paths([left, right])


def _legacy_make_mark_macron():
    return _label_paths([mark_scale(make_placeholder_shape(), 1.35, 0.18)])


def _legacy_make_mark_ring():
    outer = mark_scale(make_placeholder_shape(), 0.66, 0.98)
    inner = mark_scale(make_placeholder_shape(), 0.30, 0.44)
    _, _, oy0, oy1 = bbox_of_shape(outer)
    _, _, iy0, iy1 = bbox_of_shape(inner)
    inner = mark_translate(inner, 0, (oy0 + oy1) / 2 - (iy0 + iy1) / 2)
    inner = mark_reverse_winding(inner)
    return _label_paths([outer, inner])


def _legacy_make_mark_breve():
    s = mark_scale(make_placeholder_shape(), 1.05, 0.50)
    return _label_paths([mark_rotate(s, 24)])


def _legacy_make_mark_caron():
    b = _legacy_make_mark_breve()[0]
    _, _, cy0, cy1 = bbox_of_shape(b)
    return _label_paths([mark_mirror_y(b, cy=(cy0 + cy1) / 2)])


def _legacy_make_mark_cedilla():
    hook = mark_scale(make_placeholder_shape(), 0.34, 0.5)
    top = mark_rotate(hook, 30)
    bottom = mark_rotate(hook, -75)
    top = mark_translate(top, -2, -2)
    bottom = mark_translate(bottom, 14, -58)
    return _label_paths([top, bottom])


def _legacy_make_mark_commabelow():
    s = mark_scale(make_placeholder_shape(), 0.26, 0.68)
    return _label_paths([mark_rotate(s, -32)])


def _legacy_make_mark_ogonek():
    return _label_paths([mark_mirror_x(_legacy_make_mark_commabelow()[0])])


LEGACY_MARK_SHAPE_BUILDERS = {
    "acute": _legacy_make_mark_acute,
    "grave": _legacy_make_mark_grave,
    "circumflex": _legacy_make_mark_circumflex,
    "tilde": _legacy_make_mark_tilde,
    "macron": _legacy_make_mark_macron,
    "ring": _legacy_make_mark_ring,
    "breve": _legacy_make_mark_breve,
    "caron": _legacy_make_mark_caron,
    "cedilla": _legacy_make_mark_cedilla,
    "commabelow": _legacy_make_mark_commabelow,
    "ogonek": _legacy_make_mark_ogonek,
}


def refresh_existing_placeholder_marks(project, stroke_weight):
    """Re-run safety net: if this script already ran before and the project
    already has '_mark_<name>' Components, ensure_mark_component() will just
    reuse them as-is and never touch their shape again. This function is
    what actually upgrades a mark's artwork on a later run (sharp diamond ->
    round generic blob -> distinct per-mark shape -> weight/spacing-tuned
    shape) - but ONLY for components that are still exactly some previous
    auto-generated version of themselves. If you've already hand-drawn real
    artwork into one of these components, its shape won't match any known
    auto-generated version, so it is left completely alone."""

    def is_old_diamond(shape, eps=0.01):
        pts = shape.get("pathPoints", [])
        if len(pts) != 4:
            return False
        for pt in pts:
            p = pt["p"]["coord"]
            h1 = pt.get("h1", {}).get("coord", p)
            h2 = pt.get("h2", {}).get("coord", p)
            if math.hypot(h1["x"] - p["x"], h1["y"] - p["y"]) > eps:
                return False
            if math.hypot(h2["x"] - p["x"], h2["y"] - p["y"]) > eps:
                return False
        return True

    def is_still_auto_generated(shapes, mark_name):
        if len(shapes) == 1 and is_old_diamond(shapes[0]):
            return True  # 1st generation: sharp diamond
        if json.dumps(shapes) == json.dumps([make_placeholder_shape()]):
            return True  # 2nd generation: generic round blob (same for all marks)
        legacy_builder = LEGACY_MARK_SHAPE_BUILDERS.get(mark_name)
        if legacy_builder and json.dumps(shapes) == json.dumps(legacy_builder()):
            return True  # 3rd generation: distinct-per-mark, hardcoded thickness
        if json.dumps(shapes) == json.dumps(build_mark_shapes(mark_name, stroke_weight)):
            return True  # current generation, already up to date - re-running is a no-op
        return False

    refreshed = []
    for mark_name in PLACEHOLDER_MARK_NAMES:
        lookup_key = f"_mark_{mark_name}"
        for comp in project["components"].values():
            if comp.get("name") != lookup_key:
                continue
            shapes = comp.get("shapes") or []
            if is_still_auto_generated(shapes, mark_name):
                new_shapes = build_mark_shapes(mark_name, stroke_weight)
                if json.dumps(shapes) != json.dumps(new_shapes):
                    comp["shapes"] = new_shapes
                    refreshed.append(mark_name)
            break
    return refreshed


def new_component_id(project):
    i = 0
    while f"comp-{i}" in project["components"]:
        i += 1
    return f"comp-{i}"


def ensure_mark_component(project, mark_name, made_placeholder, stroke_weight):
    """Return a component id for the given internal mark name, creating a
    placeholder Component the first time a mark is needed."""
    lookup_key = f"_mark_{mark_name}"
    for cid, comp in project["components"].items():
        if comp.get("name") == lookup_key:
            return cid, False

    cid = new_component_id(project)
    project["components"][cid] = {
        "id": cid,
        "name": f"NEW MARK - {mark_name}",
        "advanceWidth": 0,
        "shapes": build_mark_shapes(mark_name, stroke_weight),
    }
    made_placeholder.add(mark_name)
    # tag it with a stable internal name too, so re-runs find it again
    project["components"][cid]["name"] = lookup_key
    return cid, True


def find_existing_dot_component(project):
    """Your lowercase 'i' already has its dot drawn as a separate Path.
    Reuse that exact artwork as the shared 'dot' Component instead of a
    placeholder, so İ / Ö / Ü etc. use your real dot from day one."""
    for cid, comp in project["components"].items():
        if comp.get("name") == "_mark_dot":
            return cid  # already created on a previous run - reuse it, don't duplicate

    i_glyph = project["glyphs"].get(glyph_key(ord("i")))
    if not i_glyph:
        return None
    x_height = project["settings"]["font"]["xHeight"]
    dot_shape = None
    for shape in i_glyph["shapes"]:
        if "pathPoints" not in shape:
            continue
        _, _, ymin, _ = bbox_of_shape(shape)
        if ymin > x_height * 0.7:  # sits clearly above the stem -> it's the dot
            dot_shape = shape
            break
    if dot_shape is None:
        return None

    cid = new_component_id(project)
    project["components"][cid] = {
        "id": cid,
        "name": "_mark_dot",
        "advanceWidth": 0,
        "shapes": [deepcopy(dot_shape)],
    }
    return cid


def make_instance(link, dx=0, dy=0):
    inst = {"link": link}
    if dx:
        inst["translateX"] = round(dx, 2)
    if dy:
        inst["translateY"] = round(dy, 2)
    return inst


def compute_offsets(mark_bbox, base_width, is_upper, font, side):
    xmin, xmax, ymin, ymax = mark_bbox
    mark_w = xmax - xmin
    mark_cx = (xmin + xmax) / 2
    dx = (base_width / 2) - mark_cx

    cap_h, x_h = font["capHeight"], font["xHeight"]
    if side == "above":
        reference_h = cap_h if is_upper else x_h
        target_bottom = reference_h + reference_h * MARK_GAP_ABOVE_RATIO
        dy = target_bottom - ymin
    else:  # below baseline (cedilla, ogonek, comma below)
        target_top = -MARK_GAP_BELOW
        dy = target_top - ymax
    return dx, dy, mark_w


def build_composite_glyph(project, base_cp, mark_name, count, side, made_placeholder,
                           dot_component_id, stroke_weight):
    base_key = glyph_key(base_cp)
    base_glyph = project["glyphs"].get(base_key)
    if base_glyph is None:
        return None  # base letter not drawn yet - skip

    if mark_name == "dot" and dot_component_id:
        mark_id = dot_component_id
        is_new = False
    else:
        mark_id, is_new = ensure_mark_component(project, mark_name, made_placeholder, stroke_weight)

    mark_comp = project["components"][mark_id]
    mark_bbox = combined_bbox(mark_comp["shapes"])
    is_upper = chr(base_cp).isupper()
    base_width = base_glyph["advanceWidth"]
    dx, dy, mark_w = compute_offsets(mark_bbox, base_width, is_upper, project["settings"]["font"], side)

    shapes = [make_instance(base_key)]
    if count == 1:
        shapes.append(make_instance(mark_id, dx, dy))
    else:  # pair (dieresis, double acute) - spread symmetrically
        spread = mark_w * PAIR_SPACING / 2
        shapes.append(make_instance(mark_id, dx - spread, dy))
        shapes.append(make_instance(mark_id, dx + spread, dy))

    return {"advanceWidth": base_width, "shapes": shapes}


def build_dotless_i(project):
    """ı (U+0131) = the stem-only part of your existing lowercase 'i',
    with no dot. Copied directly as a plain path - no component needed."""
    i_glyph = project["glyphs"].get(glyph_key(ord("i")))
    if not i_glyph:
        return None
    x_height = project["settings"]["font"]["xHeight"]
    stem_shapes = [
        deepcopy(s) for s in i_glyph["shapes"]
        if "pathPoints" in s and bbox_of_shape(s)[2] <= x_height * 0.7
    ]
    if not stem_shapes:
        return None
    return {"advanceWidth": i_glyph["advanceWidth"], "shapes": stem_shapes}


def rebuild_stale_composite_positions(project, dot_component_id, stroke_weight):
    """Every existing composite glyph's mark position (dx/dy) was computed
    ONCE, at build time, from whatever compute_offsets()/PAIR_SPACING were
    in effect that moment - those numbers are baked into each composite's
    stored translateX/translateY, not re-derived from the mark's current
    shape. So when a mark's geometry or these constants change later
    (thickness, dieresis spacing, gap-above ratio...), already-built
    composites go stale even if the mark COMPONENT itself didn't change at
    all (PAIR_SPACING, for instance, changes dieresis placement without
    touching the dot's own shape). This recomputes every composite that is
    STILL exactly an untouched base+mark instance construction (i.e. never
    hand-edited in Glyphr Studio - see the structural check below) and
    overwrites it only where the recomputed result actually differs."""
    rebuild_plan = {}
    for cp in range(0x80, 0x500):  # Latin-1 Supplement + Latin Extended-A/B
        ch = chr(cp)
        decomp = unicodedata.normalize("NFD", ch)
        if len(decomp) != 2:
            continue
        base_ch, mark_ch = decomp
        mark_uname = unicodedata.name(mark_ch, "")
        if mark_uname in MARK_INFO:
            mark_name, count, side = MARK_INFO[mark_uname]
            rebuild_plan[cp] = (ord(base_ch), mark_name, count, side)
    for target_cp, base_cp, mark in TURKISH_SPECIAL:
        if mark is None:
            continue
        mark_name, count, side = mark
        rebuild_plan[target_cp] = (base_cp, mark_name, count, side)

    rebuilt = []
    for cp, (base_cp, mark_name, count, side) in rebuild_plan.items():
        key = glyph_key(cp)
        glyph = project["glyphs"].get(key)
        if glyph is None:
            continue

        expected_mark_id = dot_component_id if (mark_name == "dot" and dot_component_id) else None
        if expected_mark_id is None:
            comp = find_mark_component(project, mark_name)
            expected_mark_id = comp["id"] if comp else None
        if expected_mark_id is None:
            continue

        shapes = glyph.get("shapes", [])
        # safety check: only touch it if it's STILL a plain, untouched
        # base-instance + mark-instance(s) construction - anything with a
        # raw drawn path, or a link that doesn't match what this script
        # would have produced, means a human has been in here - leave it
        if not shapes or any("pathPoints" in s for s in shapes):
            continue
        if shapes[0].get("link") != glyph_key(base_cp):
            continue
        if not all(s.get("link") == expected_mark_id for s in shapes[1:]):
            continue

        new_g = build_composite_glyph(project, base_cp, mark_name, count, side,
                                       set(), dot_component_id, stroke_weight)
        if new_g and json.dumps(new_g["shapes"]) != json.dumps(shapes):
            project["glyphs"][key] = new_g
            rebuilt.append(cp)
    return rebuilt


# ============================================================== TASK 2 ===
# "Bonus" glyphs: legacy spacing accents + combining accents (26 chars).
# ZERO new drawing - each is just one of the 11 marks (or the real dot)
# placed alone in its own glyph slot instead of next to a base letter.

LEGACY_SPACING_MARKS = {
    # codepoint: (internal mark name, how many instances) - these get a
    # REAL non-zero advance width, per GOOGLE_FONTS_SUBMISSION_GUIDE.md #5
    0x00A8: ("dot", 2),          # DIAERESIS
    0x00AF: ("macron", 1),       # MACRON
    0x00B4: ("acute", 1),        # ACUTE ACCENT
    0x00B8: ("cedilla", 1),      # CEDILLA
    0x02C6: ("circumflex", 1),   # MODIFIER LETTER CIRCUMFLEX ACCENT
    0x02C7: ("caron", 1),        # CARON
    0x02D8: ("breve", 1),        # BREVE
    0x02D9: ("dot", 1),          # DOT ABOVE
    0x02DA: ("ring", 1),         # RING ABOVE
    0x02DB: ("ogonek", 1),       # OGONEK
    0x02DC: ("tilde", 1),        # SMALL TILDE
    0x02DD: ("acute", 2),        # DOUBLE ACUTE ACCENT
}

BELOW_MARK_NAMES = {"cedilla", "ogonek", "commabelow"}
STANDALONE_SIDE_BEARING = 100  # upm - either side of a standalone mark/symbol glyph


def find_mark_component(project, mark_name):
    lookup_key = f"_mark_{mark_name}"
    for comp in project["components"].values():
        if comp.get("name") == lookup_key:
            return comp
    return None


def combining_marks_table():
    """codepoint -> (mark name, count), derived straight from MARK_INFO's
    Unicode combining-mark names so it can never drift out of sync with
    the composite-building table above."""
    table = {}
    for uname, (mark_name, count, _side) in MARK_INFO.items():
        ch = unicodedata.lookup(uname)
        table[ord(ch)] = (mark_name, count)
    return table


def build_standalone_mark_glyph(project, mark_name, count, advance_width):
    """Place 1-2 instances of an EXISTING '_mark_<name>' Component alone in
    its own glyph, centered, with no base letter - exactly the placement
    math build_composite_glyph() uses, just without a base-letter shape."""
    comp = find_mark_component(project, mark_name)
    if comp is None:
        return None

    mark_bbox = combined_bbox(comp["shapes"])
    side = "below" if mark_name in BELOW_MARK_NAMES else "above"
    # standalone marks aren't cased - treat like a lowercase attachment
    dx, dy, mark_w = compute_offsets(mark_bbox, advance_width, False,
                                      project["settings"]["font"], side)

    shapes = []
    if count == 1:
        shapes.append(make_instance(comp["id"], dx, dy))
    else:
        spread = mark_w * PAIR_SPACING / 2
        shapes.append(make_instance(comp["id"], dx - spread, dy))
        shapes.append(make_instance(comp["id"], dx + spread, dy))
    return {"advanceWidth": advance_width, "shapes": shapes}


def build_bonus_mark_glyphs(project):
    """Task 2 driver: legacy spacing (non-zero width) + combining (zero
    width) accent glyphs."""
    built = []

    for cp, (mark_name, count) in LEGACY_SPACING_MARKS.items():
        key = glyph_key(cp)
        if key in project["glyphs"]:
            continue
        comp = find_mark_component(project, mark_name)
        if comp is None:
            continue
        mw = combined_bbox(comp["shapes"])
        advance = (mw[1] - mw[0]) + 2 * STANDALONE_SIDE_BEARING
        g = build_standalone_mark_glyph(project, mark_name, count, advance)
        if g:
            project["glyphs"][key] = g
            built.append(cp)

    for cp, (mark_name, count) in combining_marks_table().items():
        key = glyph_key(cp)
        if key in project["glyphs"]:
            continue
        g = build_standalone_mark_glyph(project, mark_name, count, 0)
        if g:
            project["glyphs"][key] = g
            built.append(cp)

    return built


# ============================================================== TASK 3 ===
# Æ æ Œ œ Ø ø Đ đ (8 chars) - built mechanically from letters you already
# drew: æ/œ are two existing letters overlapped like a real ligature;
# ø/Ø and đ/Đ are an existing letter (O/o, D/d) plus a short straight
# stroke - and even that stroke is built the same way as the accent marks
# above (scale + rotate the same base blob into a flat bar - no hand
# drawing anywhere in this section either).

LIGATURE_LETTERS = {
    0x00C6: ("A", "E"),  # Æ
    0x00E6: ("a", "e"),  # æ
    0x0152: ("O", "E"),  # Œ
    0x0153: ("o", "e"),  # œ
    0x0132: ("I", "J"),  # Ĳ - was present only as an empty stub (see
    0x0133: ("i", "j"),  # ĳ   is_empty_glyph_stub below), not real artwork
}
LIGATURE_OVERLAP = 0.30  # fraction of the 2nd letter's width tucked under the 1st


def is_empty_glyph_stub(glyph):
    """True for a glyph entry that exists only as a bare {'id': ...} with
    no real shapes or advance width - Glyphr Studio can create these when
    a character range is added but the character is never actually drawn
    (found for IJ/U+0132 among a few others outside GF Latin Core)."""
    return not glyph.get("shapes") and not glyph.get("advanceWidth")


def shoelace_area(shape):
    pts = [p["p"]["coord"] for p in shape["pathPoints"]]
    n = len(pts)
    s = 0
    for i in range(n):
        s += pts[i]["x"] * pts[(i + 1) % n]["y"] - pts[(i + 1) % n]["x"] * pts[i]["y"]
    return s / 2


def dominant_winding_sign(shapes):
    """+1/-1 winding sign of a shape list's OUTER contour (the one with the
    biggest |area| - inner counters/holes are deliberately the opposite
    sign of their own outer, so only the outer contour's sign matters for
    checking compatibility with another, separate letter)."""
    if not shapes:
        return None
    outer = max(shapes, key=lambda s: abs(shoelace_area(s)))
    return -1 if shoelace_area(outer) < 0 else 1


def build_ligature_glyph(project, left_ch, right_ch):
    """Two letters overlapped like a ligature. Different letters can have
    been hand-drawn with opposite outer-contour winding (Fluma's own 'A' is
    CCW-outer while 'E' is CW-outer, for instance) - if left uncorrected,
    their overlap would cancel to a hole under a real font's nonzero-
    winding fill rule, the same class of bug found in make_mark_circumflex.
    So the right-hand letter is copied (not just instanced) and its whole
    shape list is winding-reversed as a unit when its outer sign doesn't
    match the left letter's - reversing every contour of a letter together
    preserves its own outer/inner (solid/hole) relationship, it just flips
    which absolute sign that relationship is expressed with, so it's always
    safe for the letter in isolation and now safe to overlap too."""
    left_key, right_key = glyph_key(ord(left_ch)), glyph_key(ord(right_ch))
    left_g, right_g = project["glyphs"].get(left_key), project["glyphs"].get(right_key)
    if left_g is None or right_g is None:
        return None
    overlap = right_g["advanceWidth"] * LIGATURE_OVERLAP
    dx = left_g["advanceWidth"] - overlap
    advance = dx + right_g["advanceWidth"]

    left_shapes = [s for s in left_g["shapes"] if "pathPoints" in s]
    right_shapes = [deepcopy(s) for s in right_g["shapes"] if "pathPoints" in s]
    if dominant_winding_sign(left_shapes) != dominant_winding_sign(right_shapes):
        right_shapes = [mark_reverse_winding(s) for s in right_shapes]
    right_shapes = translate_shapes(right_shapes, dx, 0)

    shapes = [make_instance(left_key)] + _label_paths(right_shapes)
    return {"advanceWidth": advance, "shapes": shapes}


def bezier_flatten(shape, steps=40):
    """Sample a path's curves into a polyline - needed to find where a
    glyph's outline actually is at a given height (anchor points alone
    can land anywhere along a curve, not just at height bands we care
    about)."""
    pts = shape["pathPoints"]
    n = len(pts)
    poly = []
    for i in range(n):
        p0 = pts[i]["p"]["coord"]
        c1 = pts[i]["h2"]["coord"]
        c2 = pts[(i + 1) % n]["h1"]["coord"]
        p1 = pts[(i + 1) % n]["p"]["coord"]
        for s in range(steps + 1):
            t = s / steps
            mt = 1 - t
            x = mt**3*p0["x"] + 3*mt**2*t*c1["x"] + 3*mt*t**2*c2["x"] + t**3*p1["x"]
            y = mt**3*p0["y"] + 3*mt**2*t*c1["y"] + 3*mt*t**2*c2["y"] + t**3*p1["y"]
            poly.append((x, y))
    return poly


def find_stem_x_range(shapes, y_lo, y_hi, x_max=None):
    """The outline's x-range within a horizontal height band - used to
    locate a letter's stem/ascender without guessing its coordinates by
    eye. x_max optionally restricts the search to the left half of the
    glyph (D's left stem, vs. the open bowl on its right)."""
    xs = []
    for s in shapes:
        for x, y in bezier_flatten(s):
            if y_lo <= y <= y_hi and (x_max is None or x < x_max):
                xs.append(x)
    return (min(xs), max(xs)) if xs else None


def make_stroke_bar(length, thickness, angle_deg, cx, cy):
    """A straight flat bar - the SAME technique as make_mark_macron(),
    just parameterized and placed wherever it's needed (through O, or
    across D's stem)."""
    s = mark_scale(make_placeholder_shape(), length / PLACEHOLDER_W, thickness / PLACEHOLDER_H)
    s = mark_translate(s, 0, -thickness / 2)
    s = mark_rotate(s, angle_deg)
    s = mark_translate(s, cx, cy)
    return _label_paths([s])


def ensure_stroke_component(project, comp_name, build_fn):
    for comp in project["components"].values():
        if comp.get("name") == comp_name:
            return comp["id"]
    shapes = build_fn()
    if shapes is None:
        return None
    cid = new_component_id(project)
    project["components"][cid] = {"id": cid, "name": comp_name, "advanceWidth": 0, "shapes": shapes}
    return cid


def build_oslash_stroke(project, base_cp):
    base_glyph = project["glyphs"].get(glyph_key(base_cp))
    if base_glyph is None:
        return None
    shapes = [s for s in base_glyph["shapes"] if "pathPoints" in s]
    x0, x1, y0, y1 = combined_bbox(shapes)
    w, h = x1 - x0, y1 - y0
    length = math.hypot(w, h) * 0.98
    thickness = h * 0.085
    return make_stroke_bar(length, thickness, 22, (x0 + x1) / 2, (y0 + y1) / 2)


def build_dstroke(project, base_cp, ascender_side, angle=0):
    base_glyph = project["glyphs"].get(glyph_key(base_cp))
    if base_glyph is None:
        return None
    shapes = [s for s in base_glyph["shapes"] if "pathPoints" in s]
    x0, x1, y0, y1 = combined_bbox(shapes)
    height = y1 - y0

    if ascender_side == "top":  # lowercase d - ascender sticks up above the bowl
        band = find_stem_x_range(shapes, y1 - height * 0.12, y1 - height * 0.02)
        cy = y1 - height * 0.25
    else:  # capital D - a left-side stem at mid cap-height
        xmid = (x0 + x1) / 2
        mid = (y0 + y1) / 2
        band = find_stem_x_range(shapes, mid - height * 0.08, mid + height * 0.08, x_max=xmid)
        cy = mid
    if band is None:
        return None
    bx0, bx1 = band
    length = (bx1 - bx0) * 1.9
    thickness = height * 0.065
    return make_stroke_bar(length, thickness, angle, (bx0 + bx1) / 2, cy)


def build_stroke_letter_glyph(project, base_cp, stroke_component_id):
    base_key = glyph_key(base_cp)
    base_glyph = project["glyphs"].get(base_key)
    if base_glyph is None or stroke_component_id is None:
        return None
    shapes = [make_instance(base_key), make_instance(stroke_component_id)]
    return {"advanceWidth": base_glyph["advanceWidth"], "shapes": shapes}


def build_ligature_and_stroke_letters(project):
    """Task 3 driver."""
    built = []
    for cp, (left_ch, right_ch) in LIGATURE_LETTERS.items():
        key = glyph_key(cp)
        existing = project["glyphs"].get(key)
        if existing is not None and not is_empty_glyph_stub(existing):
            continue
        g = build_ligature_glyph(project, left_ch, right_ch)
        if g:
            project["glyphs"][key] = g
            built.append(cp)

    for cp, base_ch in ((0x00D8, "O"), (0x00F8, "o")):
        key = glyph_key(cp)
        if key in project["glyphs"]:
            continue
        stroke_id = ensure_stroke_component(
            project, f"_stroke_oslash_{base_ch}", lambda bc=base_ch: build_oslash_stroke(project, ord(bc)))
        g = build_stroke_letter_glyph(project, ord(base_ch), stroke_id)
        if g:
            project["glyphs"][key] = g
            built.append(cp)

    for cp, base_ch, side in ((0x0110, "D", "mid"), (0x0111, "d", "top")):
        key = glyph_key(cp)
        if key in project["glyphs"]:
            continue
        stroke_id = ensure_stroke_component(
            project, f"_stroke_dstroke_{base_ch}",
            lambda bc=base_ch, sd=side: build_dstroke(project, ord(bc), sd))
        g = build_stroke_letter_glyph(project, ord(base_ch), stroke_id)
        if g:
            project["glyphs"][key] = g
            built.append(cp)

    return built


# ============================================================== TASK 4 ===
# Punctuation / math symbols with ZERO new drawing - only copying,
# mirroring, scaling or duplicating shapes already drawn as plain ASCII
# glyphs (period, comma, apostrophe, quotation mark, hyphen, exclamation/
# question, angle brackets, x) or reusing the ring/dot mark Components.

def copy_glyph_shapes(project, cp):
    g = project["glyphs"].get(glyph_key(cp))
    if g is None:
        return None
    return [deepcopy(s) for s in g.get("shapes", []) if "pathPoints" in s]


def rotate_shapes(shapes, deg, cx, cy):
    return [mark_rotate(s, deg, cx=cx, cy=cy) for s in shapes]


def mirror_shapes_x(shapes, cx):
    return [mark_mirror_x(s, cx=cx) for s in shapes]


def scale_shapes(shapes, sx, sy, cx=0.0, cy=0.0):
    return [mark_scale(s, sx, sy, cx=cx, cy=cy) for s in shapes]


def translate_shapes(shapes, dx, dy):
    return [mark_translate(s, dx, dy) for s in shapes]


def build_reuse_space(project):
    """NBSP = SPACE's advance width copied over, no visible shape."""
    sp = project["glyphs"].get(glyph_key(0x20))
    if sp is None:
        return None
    return {"advanceWidth": sp["advanceWidth"], "shapes": []}


def build_reuse_rotate180(project, source_cp):
    """¡ / ¿ = ! / ? rotated 180 degrees around their own center."""
    shapes = copy_glyph_shapes(project, source_cp)
    src = project["glyphs"].get(glyph_key(source_cp))
    if not shapes or src is None:
        return None
    x0, x1, y0, y1 = combined_bbox(shapes)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    return {"advanceWidth": src["advanceWidth"], "shapes": rotate_shapes(shapes, 180, cx, cy)}


def build_reuse_double(project, source_cp, gap):
    """« » = two <, > side by side. „ = two commas side by side."""
    shapes = copy_glyph_shapes(project, source_cp)
    src = project["glyphs"].get(glyph_key(source_cp))
    if not shapes or src is None:
        return None
    w = src["advanceWidth"]
    right = translate_shapes(deepcopy(shapes), w + gap, 0)
    return {"advanceWidth": w * 2 + gap, "shapes": shapes + right}


def build_reuse_copy(project, source_cp):
    shapes = copy_glyph_shapes(project, source_cp)
    src = project["glyphs"].get(glyph_key(source_cp))
    if not shapes or src is None:
        return None
    return {"advanceWidth": src["advanceWidth"], "shapes": shapes}


def build_reuse_mirror(project, source_cp):
    shapes = copy_glyph_shapes(project, source_cp)
    src = project["glyphs"].get(glyph_key(source_cp))
    if not shapes or src is None:
        return None
    x0, x1, _, _ = combined_bbox(shapes)
    return {"advanceWidth": src["advanceWidth"], "shapes": mirror_shapes_x(shapes, cx=(x0 + x1) / 2)}


def build_reuse_reposition_dot(project, target_y_center):
    """Middle dot = period, shifted up to x-height/2."""
    shapes = copy_glyph_shapes(project, ord("."))
    src = project["glyphs"].get(glyph_key(ord(".")))
    if not shapes or src is None:
        return None
    _, _, y0, y1 = combined_bbox(shapes)
    cy = (y0 + y1) / 2
    return {"advanceWidth": src["advanceWidth"], "shapes": translate_shapes(shapes, 0, target_y_center - cy)}


def build_reuse_ellipsis(project):
    """Three periods, evenly spaced."""
    shapes = copy_glyph_shapes(project, ord("."))
    src = project["glyphs"].get(glyph_key(ord(".")))
    if not shapes or src is None:
        return None
    w = src["advanceWidth"]
    out = list(shapes)
    out += translate_shapes(deepcopy(shapes), w, 0)
    out += translate_shapes(deepcopy(shapes), w * 2, 0)
    return {"advanceWidth": w * 3, "shapes": out}


def build_reuse_dash(project, target_width):
    """en/em dash = hyphen, scaled horizontally to the target width."""
    shapes = copy_glyph_shapes(project, ord("-"))
    src = project["glyphs"].get(glyph_key(ord("-")))
    if not shapes or src is None:
        return None
    x0, x1, _, _ = combined_bbox(shapes)
    w = x1 - x0
    scaled = scale_shapes(shapes, target_width / w, 1.0, cx=x0, cy=0)
    advance = src["advanceWidth"] * (target_width / w)
    return {"advanceWidth": advance, "shapes": scaled}


def build_reuse_minus(project):
    """minus sign = hyphen, vertically realigned to the '+' sign's crossbar
    height, sharing '+'s advance width for consistent math-symbol spacing."""
    hyphen_shapes = copy_glyph_shapes(project, ord("-"))
    plus_shapes = copy_glyph_shapes(project, ord("+"))
    plus_glyph = project["glyphs"].get(glyph_key(ord("+")))
    if not hyphen_shapes or not plus_shapes or plus_glyph is None:
        return None
    _, _, py0, py1 = combined_bbox(plus_shapes)
    plus_cy = (py0 + py1) / 2
    _, _, hy0, hy1 = combined_bbox(hyphen_shapes)
    shapes = translate_shapes(hyphen_shapes, 0, plus_cy - (hy0 + hy1) / 2)
    x0, x1, _, _ = combined_bbox(shapes)
    dx = (plus_glyph["advanceWidth"] / 2) - (x0 + x1) / 2
    shapes = translate_shapes(shapes, dx, 0)
    return {"advanceWidth": plus_glyph["advanceWidth"], "shapes": shapes}


def build_reuse_multiply(project):
    """multiplication sign = lowercase x, scaled/repositioned to the '+'/
    minus sign's size and math-axis height."""
    x_shapes = copy_glyph_shapes(project, ord("x"))
    plus_shapes = copy_glyph_shapes(project, ord("+"))
    plus_glyph = project["glyphs"].get(glyph_key(ord("+")))
    if not x_shapes or not plus_shapes or plus_glyph is None:
        return None
    x0, x1, y0, y1 = combined_bbox(x_shapes)
    xh = y1 - y0
    _, _, py0, py1 = combined_bbox(plus_shapes)
    plus_h = py1 - py0
    plus_cy = (py0 + py1) / 2
    scale = (plus_h * 1.15) / xh  # a touch bigger than the plus sign's own height
    shapes = scale_shapes(x_shapes, scale, scale, cx=x0, cy=y0)
    nx0, nx1, ny0, ny1 = combined_bbox(shapes)
    shapes = translate_shapes(shapes, 0, plus_cy - (ny0 + ny1) / 2)
    dx = (plus_glyph["advanceWidth"] / 2) - (nx0 + nx1) / 2
    shapes = translate_shapes(shapes, dx, 0)
    return {"advanceWidth": plus_glyph["advanceWidth"], "shapes": shapes}


def build_reuse_degree(project):
    """degree sign = the 'ring' mark Component, placed up near cap-height."""
    comp = find_mark_component(project, "ring")
    if comp is None:
        return None
    ring_bbox = combined_bbox(comp["shapes"])
    font = project["settings"]["font"]
    advance = (ring_bbox[1] - ring_bbox[0]) + 2 * STANDALONE_SIDE_BEARING
    dx, dy, _ = compute_offsets(ring_bbox, advance, True, font, "above")
    return {"advanceWidth": advance, "shapes": [make_instance(comp["id"], dx, dy)]}


def build_reuse_bullet(project):
    """bullet = the real 'i'/'j' dot artwork, enlarged, centered at
    x-height/2."""
    comp = find_mark_component(project, "dot")
    if comp is None:
        return None
    dot_bbox = combined_bbox(comp["shapes"])
    shapes = scale_shapes([deepcopy(s) for s in comp["shapes"]], 1.6, 1.6,
                           cx=(dot_bbox[0] + dot_bbox[1]) / 2, cy=(dot_bbox[2] + dot_bbox[3]) / 2)
    x0, x1, y0, y1 = combined_bbox(shapes)
    font = project["settings"]["font"]
    shapes = translate_shapes(shapes, 0, font["xHeight"] / 2 - (y0 + y1) / 2)
    advance = (x1 - x0) + 2 * STANDALONE_SIDE_BEARING
    x0b, x1b, _, _ = combined_bbox(shapes)
    shapes = translate_shapes(shapes, advance / 2 - (x0b + x1b) / 2, 0)
    return {"advanceWidth": advance, "shapes": shapes}


def build_reuse_division(project):
    """division sign = hyphen bar + two dots (the 'dot' mark), one above,
    one below."""
    hyphen_shapes = copy_glyph_shapes(project, ord("-"))
    hyphen_glyph = project["glyphs"].get(glyph_key(ord("-")))
    comp = find_mark_component(project, "dot")
    if not hyphen_shapes or hyphen_glyph is None or comp is None:
        return None
    x0, x1, y0, y1 = combined_bbox(hyphen_shapes)
    bar_cy = (y0 + y1) / 2
    dot_bbox = combined_bbox(comp["shapes"])
    dot_cx = (dot_bbox[0] + dot_bbox[1]) / 2
    gap = (dot_bbox[3] - dot_bbox[2]) * 0.9
    dx = (x0 + x1) / 2 - dot_cx
    dy_top = (bar_cy + gap) - dot_bbox[2]
    dy_bot = (bar_cy - gap) - dot_bbox[3]
    shapes = list(hyphen_shapes)
    shapes.append(make_instance(comp["id"], dx, dy_top))
    shapes.append(make_instance(comp["id"], dx, dy_bot))
    return {"advanceWidth": hyphen_glyph["advanceWidth"], "shapes": shapes}


def build_mechanical_punctuation(project):
    """Task 4 driver."""
    font = project["settings"]["font"]
    upm = font["upm"]
    built = []

    def add(cp, glyph):
        key = glyph_key(cp)
        if glyph and key not in project["glyphs"]:
            project["glyphs"][key] = glyph
            built.append(cp)

    add(0x00A0, build_reuse_space(project))                          # NBSP
    add(0x00A1, build_reuse_rotate180(project, ord("!")))            # ¡
    add(0x00BF, build_reuse_rotate180(project, ord("?")))            # ¿
    add(0x00AB, build_reuse_double(project, ord("<"), 40))           # «
    add(0x00BB, build_reuse_double(project, ord(">"), 40))           # »
    add(0x2039, build_reuse_copy(project, ord("<")))                 # ‹
    add(0x203A, build_reuse_copy(project, ord(">")))                 # ›
    add(0x00B7, build_reuse_reposition_dot(project, font["xHeight"] / 2))  # ·
    add(0x2013, build_reuse_dash(project, upm * 0.5))                # – en dash
    add(0x2014, build_reuse_dash(project, upm * 1.0))                # — em dash
    add(0x2018, build_reuse_mirror(project, ord("'")))               # '
    add(0x2019, build_reuse_copy(project, ord("'")))                 # '
    add(0x201A, build_reuse_copy(project, ord(",")))                 # ‚
    add(0x201C, build_reuse_mirror(project, ord('"')))               # "
    add(0x201D, build_reuse_copy(project, ord('"')))                 # "
    add(0x201E, build_reuse_double(project, ord(","), 30))           # „
    add(0x2022, build_reuse_bullet(project))                         # •
    add(0x2026, build_reuse_ellipsis(project))                       # …
    add(0x2212, build_reuse_minus(project))                          # −
    add(0x00F7, build_reuse_division(project))                       # ÷
    add(0x00D7, build_reuse_multiply(project))                       # ×
    add(0x00B0, build_reuse_degree(project))                         # °

    return built


# ============================================================== TASK 6 ===
# 15 more characters, same mechanical philosophy as Tasks 2-4: measure the
# real letter, add a stroke/ring/scaled-copy built from the same base-blob
# technique - still zero hand-drawn artwork. Every construction here that
# overlaps two independently-drawn shapes checks their winding direction
# first (see dominant_winding_sign / mark_reverse_winding above) - the
# same class of bug make_mark_circumflex had is possible any time two
# separately-drawn contours overlap in area.

# --- Ð ð (Eth) - same construction as Đ/đ, just a different component so
# it can be edited independently; ð gets a distinct stroke angle so it
# doesn't render pixel-identical to đ.

def build_eth_letters(project):
    built = []
    for cp, base_ch, side, angle in ((0x00D0, "D", "mid", 0), (0x00F0, "d", "top", -14)):
        key = glyph_key(cp)
        if key in project["glyphs"]:
            continue
        comp_name = f"_stroke_eth_{base_ch}"
        stroke_id = ensure_stroke_component(
            project, comp_name,
            lambda bc=base_ch, sd=side, an=angle: build_dstroke(project, ord(bc), sd, angle=an))
        g = build_stroke_letter_glyph(project, ord(base_ch), stroke_id)
        if g:
            project["glyphs"][key] = g
            built.append(cp)
    return built


# --- Ħ ħ - H/h + a horizontal stroke (full width on capital H, over the
# ascender only on lowercase h, same "top band" trick as đ's ascender).

def build_h_stroke(project, base_cp, ascender_side):
    base_glyph = project["glyphs"].get(glyph_key(base_cp))
    if base_glyph is None:
        return None
    shapes = [s for s in base_glyph["shapes"] if "pathPoints" in s]
    x0, x1, y0, y1 = combined_bbox(shapes)
    height = y1 - y0

    if ascender_side == "top":  # lowercase h - stroke over the left ascender
        band = find_stem_x_range(shapes, y1 - height * 0.12, y1 - height * 0.02)
        if band is None:
            return None
        bx0, bx1 = band
        cx, cy = (bx0 + bx1) / 2, y1 - height * 0.25
        length = (bx1 - bx0) * 1.9
        thickness = height * 0.065
    else:  # capital H - a full-width stroke, a bit above natural center
        cx, cy = (x0 + x1) / 2, y0 + height * 0.63
        length = (x1 - x0) * 1.12
        thickness = height * 0.07
    return make_stroke_bar(length, thickness, 0, cx, cy)


def build_hstroke_letters(project):
    built = []
    for cp, base_ch, side in ((0x0126, "H", "mid"), (0x0127, "h", "top")):
        key = glyph_key(cp)
        if key in project["glyphs"]:
            continue
        comp_name = f"_stroke_hstroke_{base_ch}"
        stroke_id = ensure_stroke_component(
            project, comp_name, lambda bc=base_ch, sd=side: build_h_stroke(project, ord(bc), sd))
        g = build_stroke_letter_glyph(project, ord(base_ch), stroke_id)
        if g:
            project["glyphs"][key] = g
            built.append(cp)
    return built


# --- Ł ł - L/l + a diagonal stroke through the stem, positioned near
# x-height (matching where a real Ł/ł crosses, not the vertical middle of
# the whole ascender/cap stem).

def build_l_stroke(project, base_cp, y_center_abs):
    base_glyph = project["glyphs"].get(glyph_key(base_cp))
    if base_glyph is None:
        return None
    shapes = [s for s in base_glyph["shapes"] if "pathPoints" in s]
    x0, x1, y0, y1 = combined_bbox(shapes)
    height = y1 - y0
    band = find_stem_x_range(shapes, y_center_abs - height * 0.08, y_center_abs + height * 0.08)
    if band is None:
        band = (x0, x1)
    bx0, bx1 = band
    length = (bx1 - bx0) * 2.6
    thickness = height * 0.06
    return make_stroke_bar(length, thickness, 25, (bx0 + bx1) / 2, y_center_abs)


def build_lstroke_letters(project):
    built = []
    font = project["settings"]["font"]
    y_center = font["xHeight"] * 0.45
    for cp, base_ch in ((0x0141, "L"), (0x0142, "l")):
        key = glyph_key(cp)
        if key in project["glyphs"]:
            continue
        comp_name = f"_stroke_lstroke_{base_ch}"
        stroke_id = ensure_stroke_component(
            project, comp_name, lambda bc=base_ch: build_l_stroke(project, ord(bc), y_center))
        g = build_stroke_letter_glyph(project, ord(base_ch), stroke_id)
        if g:
            project["glyphs"][key] = g
            built.append(cp)
    return built


# --- ª º - a/o shrunk to superscript size with a short underline, the
# standard construction for feminine/masculine ordinal indicators.

SUPERSCRIPT_SCALE = 0.50
SUPERSCRIPT_UNDERLINE_GAP = 30


def build_superscript_ordinal(project, base_cp):
    base_glyph = project["glyphs"].get(glyph_key(base_cp))
    if base_glyph is None:
        return None
    shapes = [deepcopy(s) for s in base_glyph["shapes"] if "pathPoints" in s]
    font = project["settings"]["font"]
    baseline = font["capHeight"] * 0.50

    scaled = scale_shapes(shapes, SUPERSCRIPT_SCALE, SUPERSCRIPT_SCALE, cx=0, cy=0)
    x0, x1, y0, y1 = combined_bbox(scaled)
    scaled = translate_shapes(scaled, 0, baseline - y0)
    x0, x1, y0, y1 = combined_bbox(scaled)
    letter_w = x1 - x0

    thickness = (font["xHeight"] * SUPERSCRIPT_SCALE) * 0.09
    bar_cy = y0 - SUPERSCRIPT_UNDERLINE_GAP - thickness / 2
    bar = make_stroke_bar(letter_w * 1.05, thickness, 0, (x0 + x1) / 2, bar_cy)

    shapes_all = _label_paths(scaled) + bar
    ax0, ax1, _, _ = combined_bbox(shapes_all)
    advance = (ax1 - ax0) + 2 * STANDALONE_SIDE_BEARING
    shapes_all = translate_shapes(shapes_all, advance / 2 - (ax0 + ax1) / 2, 0)
    return {"advanceWidth": advance, "shapes": shapes_all}


def build_ordinal_indicators(project):
    built = []
    for cp, base_ch in ((0x00AA, "a"), (0x00BA, "o")):
        key = glyph_key(cp)
        if key in project["glyphs"]:
            continue
        g = build_superscript_ordinal(project, ord(base_ch))
        if g:
            project["glyphs"][key] = g
            built.append(cp)
    return built


# --- ȷ (dotless j) - same technique as dotless ı: copy the non-dot path(s)
# of 'j' (its hook/descender), same dot-detection heuristic as build_dotless_i.

def build_dotless_j(project):
    j_glyph = project["glyphs"].get(glyph_key(ord("j")))
    if not j_glyph:
        return None
    x_height = project["settings"]["font"]["xHeight"]
    stem_shapes = [
        deepcopy(s) for s in j_glyph["shapes"]
        if "pathPoints" in s and bbox_of_shape(s)[2] <= x_height * 0.7
    ]
    if not stem_shapes:
        return None
    return {"advanceWidth": j_glyph["advanceWidth"], "shapes": stem_shapes}


def build_dotless_j_glyph(project):
    key = glyph_key(0x0237)
    if key in project["glyphs"]:
        return []
    g = build_dotless_j(project)
    if g:
        project["glyphs"][key] = g
        return [0x0237]
    return []


# --- © ® - a bigger, rounder ring (same outer+winding-reversed-inner
# donut technique as make_mark_ring, just sized to comfortably frame a
# letter) + a scaled copy of C / R centered inside it.

def make_ring_shape(outer_w, outer_h, thickness):
    outer = mark_scale(make_placeholder_shape(), outer_w / PLACEHOLDER_W, outer_h / PLACEHOLDER_H)
    inner = mark_scale(make_placeholder_shape(),
                        (outer_w - 2 * thickness) / PLACEHOLDER_W,
                        (outer_h - 2 * thickness) / PLACEHOLDER_H)
    _, _, oy0, oy1 = bbox_of_shape(outer)
    _, _, iy0, iy1 = bbox_of_shape(inner)
    inner = mark_translate(inner, 0, (oy0 + oy1) / 2 - (iy0 + iy1) / 2)
    inner = mark_reverse_winding(inner)
    return _label_paths([outer, inner])


def build_circled_letter(project, base_cp, comp_name, ring_size, ring_thickness, letter_scale_frac):
    stroke_id = ensure_stroke_component(
        project, comp_name, lambda: make_ring_shape(ring_size, ring_size, ring_thickness))
    if stroke_id is None:
        return None
    base_glyph = project["glyphs"].get(glyph_key(base_cp))
    if base_glyph is None:
        return None

    font = project["settings"]["font"]
    ring_local_cy = ring_size / 2  # ring rests on y=0, spans up to outer_h locally
    target_cy = font["capHeight"] * 0.52
    dy = target_cy - ring_local_cy
    advance = ring_size + 2 * STANDALONE_SIDE_BEARING
    dx_ring = advance / 2  # the ring is already x-centered at 0 locally

    letter_shapes = [deepcopy(s) for s in base_glyph["shapes"] if "pathPoints" in s]
    lx0, lx1, ly0, ly1 = combined_bbox(letter_shapes)
    letter_h = ly1 - ly0
    inner_d = ring_size - 2 * ring_thickness
    scale = (inner_d * letter_scale_frac) / letter_h

    # nonzero-winding check: the ring's own outer/inner already oppose each
    # other by design (like make_mark_ring) - the LETTER dropped inside its
    # hollow center is a separate, independent contour, so it only needs
    # its OWN internal solid/hole relationship intact (untouched here), not
    # matched to the ring - a letter's own winding never gets cancelled by
    # a DIFFERENT shape's winding, only by an oppositely-wound copy of the
    # very same overlapping area (see build_ligature_glyph for that case).
    scaled = scale_shapes(letter_shapes, scale, scale, cx=lx0, cy=ly0)
    sx0, sx1, sy0, sy1 = combined_bbox(scaled)
    scaled = translate_shapes(scaled, -(sx0 + sx1) / 2, ring_local_cy - (sy0 + sy1) / 2)
    scaled = translate_shapes(scaled, dx_ring, dy)

    shapes = [make_instance(stroke_id, 0, dy)] + _label_paths(scaled)
    shapes[0]["translateX"] = round(dx_ring, 2)
    return {"advanceWidth": advance, "shapes": shapes}


def build_copyright_registered(project):
    built = []
    for cp, base_ch in ((0x00A9, "C"), (0x00AE, "R")):
        key = glyph_key(cp)
        if key in project["glyphs"]:
            continue
        g = build_circled_letter(project, ord(base_ch), f"_symbol_ring_{base_ch}", 1150, 130, 0.60)
        if g:
            project["glyphs"][key] = g
            built.append(cp)
    return built


# --- ™ - T + M shrunk to superscript size, side by side, no ring.

def build_trademark(project):
    key = glyph_key(0x2122)
    if key in project["glyphs"]:
        return []
    t_glyph = project["glyphs"].get(glyph_key(ord("T")))
    m_glyph = project["glyphs"].get(glyph_key(ord("M")))
    if t_glyph is None or m_glyph is None:
        return []
    font = project["settings"]["font"]
    scale = 0.46
    baseline = font["capHeight"] * 0.50

    def prep(glyph):
        shapes = [deepcopy(s) for s in glyph["shapes"] if "pathPoints" in s]
        shapes = scale_shapes(shapes, scale, scale, cx=0, cy=0)
        x0, x1, y0, y1 = combined_bbox(shapes)
        shapes = translate_shapes(shapes, -x0, baseline - y0)
        _, x1b, _, _ = combined_bbox(shapes)
        return shapes, x1b

    t_shapes, t_w = prep(t_glyph)
    m_shapes, m_w = prep(m_glyph)
    gap = t_w * 0.18
    m_shapes = translate_shapes(m_shapes, t_w + gap, 0)
    advance = t_w + gap + m_w + 2 * STANDALONE_SIDE_BEARING
    all_shapes = translate_shapes(_label_paths(t_shapes + m_shapes), STANDALONE_SIDE_BEARING, 0)
    project["glyphs"][key] = {"advanceWidth": advance, "shapes": all_shapes}
    return [0x2122]


# --- € ¥ ¢ - existing letter + bar(s)/stem reused from elsewhere.

def build_euro(project):
    key = glyph_key(0x20AC)
    if key in project["glyphs"]:
        return []
    c_glyph = project["glyphs"].get(glyph_key(ord("C")))
    if c_glyph is None:
        return []
    shapes = [s for s in c_glyph["shapes"] if "pathPoints" in s]
    x0, x1, y0, y1 = combined_bbox(shapes)
    height = y1 - y0
    bar_x0 = x0 - height * 0.05
    bar_x1 = (x0 + x1) / 2 + height * 0.08
    length = bar_x1 - bar_x0
    thickness = height * 0.07
    bar_cx = (bar_x0 + bar_x1) / 2
    bar1 = make_stroke_bar(length, thickness, 0, bar_cx, y0 + height * 0.40)
    bar2 = make_stroke_bar(length, thickness, 0, bar_cx, y0 + height * 0.60)
    shapes_all = [make_instance(glyph_key(ord("C")))] + bar1 + bar2
    project["glyphs"][key] = {"advanceWidth": c_glyph["advanceWidth"], "shapes": shapes_all}
    return [0x20AC]


def build_yen(project):
    key = glyph_key(0x00A5)
    if key in project["glyphs"]:
        return []
    y_glyph = project["glyphs"].get(glyph_key(ord("Y")))
    if y_glyph is None:
        return []
    shapes = [s for s in y_glyph["shapes"] if "pathPoints" in s]
    x0, x1, y0, y1 = combined_bbox(shapes)
    height = y1 - y0
    band = find_stem_x_range(shapes, y0, y0 + height * 0.32)
    if band is None:
        band = (x0, x1)
    bx0, bx1 = band
    length = (bx1 - bx0) * 1.7
    thickness = height * 0.055
    cx = (bx0 + bx1) / 2
    bar1 = make_stroke_bar(length, thickness, 0, cx, y0 + height * 0.16)
    bar2 = make_stroke_bar(length, thickness, 0, cx, y0 + height * 0.30)
    shapes_all = [make_instance(glyph_key(ord("Y")))] + bar1 + bar2
    project["glyphs"][key] = {"advanceWidth": y_glyph["advanceWidth"], "shapes": shapes_all}
    return [0x00A5]


def build_cent(project):
    key = glyph_key(0x00A2)
    if key in project["glyphs"]:
        return []
    c_glyph = project["glyphs"].get(glyph_key(ord("c")))
    stem_glyph = project["glyphs"].get(glyph_key(ord("I")))
    if c_glyph is None or stem_glyph is None:
        return []
    c_shapes = [s for s in c_glyph["shapes"] if "pathPoints" in s]
    cx0, cx1, cy0, cy1 = combined_bbox(c_shapes)
    c_h = cy1 - cy0
    c_cx, c_cy = (cx0 + cx1) / 2, (cy0 + cy1) / 2

    stem_shapes = [deepcopy(s) for s in stem_glyph["shapes"] if "pathPoints" in s]
    sx0, sx1, sy0, sy1 = combined_bbox(stem_shapes)
    scale = (c_h * 1.5) / (sy1 - sy0)
    stem_shapes = scale_shapes(stem_shapes, scale, scale, cx=(sx0 + sx1) / 2, cy=sy0)
    nx0, nx1, ny0, ny1 = combined_bbox(stem_shapes)
    stem_shapes = translate_shapes(stem_shapes, c_cx - (nx0 + nx1) / 2, c_cy - (ny0 + ny1) / 2)

    shapes_all = [make_instance(glyph_key(ord("c")))] + _label_paths(stem_shapes)
    project["glyphs"][key] = {"advanceWidth": c_glyph["advanceWidth"], "shapes": shapes_all}
    return [0x00A2]


def build_task6_mechanical(project):
    """Driver for all of Task 6."""
    built = []
    built += build_eth_letters(project)
    built += build_hstroke_letters(project)
    built += build_lstroke_letters(project)
    built += build_ordinal_indicators(project)
    built += build_dotless_j_glyph(project)
    built += build_copyright_registered(project)
    built += build_trademark(project)
    built += build_euro(project)
    built += build_yen(project)
    built += build_cent(project)
    return built


# ============================================================== TASK 7 ===
# QA pass fix: Þ/þ (Thorn) were drawn (via Firefly) at the wrong scale
# relative to the rest of the font - found by measuring their bbox against
# sibling letters (B/D/H for the cap, b/d/h/k/l for the ascender) rather
# than eyeballing it. Rescales the real path data + advance width
# proportionally, pivoting from the baseline and left edge so position and
# left sidebearing don't move - only the glyph's own size corrects.

def rescale_glyph_shapes(project, cp, scale, pivot_x, pivot_y=0.0):
    gl = project["glyphs"][glyph_key(cp)]
    for s in gl["shapes"]:
        if "pathPoints" not in s:
            continue
        for pt in s["pathPoints"]:
            for k in ("p", "h1", "h2"):
                c = pt.get(k, {}).get("coord")
                if c:
                    c["x"] = pivot_x + (c["x"] - pivot_x) * scale
                    c["y"] = pivot_y + (c["y"] - pivot_y) * scale
    gl["advanceWidth"] = gl["advanceWidth"] * scale


def fix_thorn_scale(project):
    fixed = []

    def measured_top(ref_chars):
        tops = []
        for ch in ref_chars:
            gl = project["glyphs"].get(glyph_key(ord(ch)))
            if not gl:
                continue
            shapes = [s for s in gl["shapes"] if "pathPoints" in s]
            if shapes:
                tops.append(combined_bbox(shapes)[3])
        return sum(tops) / len(tops) if tops else None

    # 0x00DF (ss) confirmed by user request: also rescale to ascender
    # height, same technique as Thorn (QA pass found it at ~1146 vs the
    # b/d/h/k/l group's ~1530-1550 - same class of undersized artwork).
    for cp, ref_chars in ((0x00DE, "BDH"), (0x00FE, "bdhkl"), (0x00DF, "bdhkl")):
        key = glyph_key(cp)
        gl = project["glyphs"].get(key)
        if gl is None:
            continue
        shapes = [s for s in gl["shapes"] if "pathPoints" in s]
        if not shapes:
            continue
        target = measured_top(ref_chars)
        if target is None:
            continue
        x0, x1, y0, y1 = combined_bbox(shapes)
        if y1 <= 0:
            continue
        scale = target / y1
        if abs(scale - 1.0) > 0.02:  # idempotent guard - already-fixed run is a no-op
            rescale_glyph_shapes(project, cp, scale, x0, 0.0)
            fixed.append(cp)
    return fixed


def fix_pilcrow_descender(project):
    """Pilcrow's two stems didn't descend below the baseline (found during
    this QA pass - confirmed by user request to fix, since most typefaces
    have the vertical stroke hang down past baseline). Extends the two
    stems' already-rounded bottom caps (matching this font's own blob-
    terminal style - the curve data already dips slightly past y=0 right
    at these points) straight down by a fixed amount, leaving the bowl
    and everything else untouched. Hardcoded to this glyph's specific,
    already-inspected point layout - if the shape is ever hand-redrawn
    the structural guard below makes this a safe no-op instead of
    corrupting new artwork."""
    key = glyph_key(0x00B6)
    gl = project["glyphs"].get(key)
    if gl is None:
        return []
    shapes = [s for s in gl["shapes"] if "pathPoints" in s]
    if len(shapes) != 1 or len(shapes[0]["pathPoints"]) != 20:
        return []  # structure changed since this was written - leave alone
    pts = shapes[0]["pathPoints"]
    stem_bottom_indices = [2, 3, 14, 15]
    offset = 200
    if min(pts[i]["p"]["coord"]["y"] for i in stem_bottom_indices) < -50:
        return []  # already extended - idempotent no-op
    for i in stem_bottom_indices:
        pt = pts[i]
        for k in ("p", "h1", "h2"):
            c = pt.get(k, {}).get("coord")
            if c:
                c["y"] -= offset
    return [0x00B6]


# ============================================================== TASK 8 ===
# ẞ (U+1E9E, capital sharp S) - the one genuinely hand-drawn artwork this
# whole audit could not build mechanically. Imported from an external SVG
# (drawn outside Glyphr Studio) and positioned using the SAME "measure the
# real reference capitals" technique as the Thorn/ss fix above: cap-height
# from B/D/H, left/right sidebearing from the same three, so it drops in
# matching its siblings instead of at whatever scale/position the SVG
# happened to use.

def svg_path_to_glyphr_points(path):
    """Convert an svgpathtools Path (cubic beziers + lines, one closed
    contour) into Glyphr Studio's pathPoints list. Each point's anchor is
    a segment boundary; h2 = that segment's own first control point (or
    the anchor itself for a straight Line - a zero-length handle renders
    as a straight edge, same convention as make_placeholder_shape's
    corners); h1 = the PREVIOUS segment's second control point. SVG's
    y-axis points down; this flips it to match the font's y-up, baseline-
    relative space (still unscaled/unpositioned - the caller places it)."""
    import svgpathtools

    def to_xy(c):
        return (c.real, -c.imag)

    n = len(path)
    anchors = [to_xy(seg.start) for seg in path]
    h2s, h1s = [], []
    for seg in path:
        if isinstance(seg, svgpathtools.CubicBezier):
            h2s.append(to_xy(seg.control1))
            h1s.append(to_xy(seg.control2))
        else:  # Line or anything else without real control points
            h2s.append(to_xy(seg.start))
            h1s.append(to_xy(seg.end))

    points = []
    for i in range(n):
        h1 = h1s[i - 1]
        points.append({
            "type": "corner",
            "p": {"coord": {"x": anchors[i][0], "y": anchors[i][1]}},
            "h1": {"coord": {"x": h1[0], "y": h1[1]}},
            "h2": {"coord": {"x": h2s[i][0], "y": h2s[i][1]}},
        })
    return points


def import_capital_eszett(project, svg_path):
    key = glyph_key(0x1E9E)
    if key in project["glyphs"]:
        return None
    if not os.path.exists(svg_path):
        return None
    try:
        import svgpathtools
    except ImportError:
        print(f"  (skipping SS import - 'pip3 install svgpathtools' first)")
        return None

    paths, _ = svgpathtools.svg2paths(svg_path)
    if not paths:
        return None
    points = svg_path_to_glyphr_points(paths[0])

    xs = [pt["p"]["coord"]["x"] for pt in points]
    ys = [pt["p"]["coord"]["y"] for pt in points]
    raw_x0, raw_x1 = min(xs), max(xs)
    raw_y0, raw_y1 = min(ys), max(ys)
    raw_h = raw_y1 - raw_y0
    if raw_h <= 0:
        return None

    tops, lefts, rights = [], [], []
    for ch in "BDH":
        gl = project["glyphs"].get(glyph_key(ord(ch)))
        if not gl:
            continue
        shapes = [s for s in gl["shapes"] if "pathPoints" in s]
        if not shapes:
            continue
        x0, x1, y0, y1 = combined_bbox(shapes)
        tops.append(y1)
        lefts.append(x0)
        rights.append(gl["advanceWidth"] - x1)
    if not tops:
        return None
    target_top = sum(tops) / len(tops)
    target_left = sum(lefts) / len(lefts)
    target_right = sum(rights) / len(rights)

    scale = target_top / raw_h
    for pt in points:
        for k in ("p", "h1", "h2"):
            c = pt[k]["coord"]
            c["x"] = (c["x"] - raw_x0) * scale + target_left
            c["y"] = (c["y"] - raw_y0) * scale

    scaled_width = (raw_x1 - raw_x0) * scale
    advance_width = target_left + scaled_width + target_right

    project["glyphs"][key] = {
        "advanceWidth": advance_width,
        "shapes": [{"name": "Path 1", "pathPoints": points}],
    }
    return 0x1E9E


# ------------------------------------------------------------------- main --

def load_core_codepoints(nam_path):
    cps = []
    with open(nam_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            m = re.match(r"0x([0-9A-Fa-f]+)", line)
            if m and not line.startswith("#"):
                cps.append(int(m.group(1), 16))
    return cps


def measure_stroke_weight(project):
    """Fluma's own stem/stroke weight (upm units), measured from 'l' and
    'I' - both are plain straight stems with no arch or bowl to confuse
    the measurement, just the organic "swells at both ends" terminals this
    font draws on every stem. Scanning several horizontal bands down each
    letter and taking the NARROWEST width found gives the true stem weight
    (the widest points are the decorative terminal blobs flaring out at
    top/bottom, not the weight); 'l' and 'I' agree to within ~1 upm on this
    project, which is good evidence the measurement is picking up something
    real rather than an artifact of either letter's specific shape."""
    weights = []
    for ch in ("l", "I"):
        glyph = project["glyphs"].get(glyph_key(ord(ch)))
        if glyph is None:
            continue
        shapes = [s for s in glyph["shapes"] if "pathPoints" in s]
        if not shapes:
            continue
        _, _, y0, y1 = combined_bbox(shapes)
        h = y1 - y0
        if h <= 0:
            continue
        widths = []
        for pct in range(30, 71, 5):  # 30%-70% of the stem's height - well
            frac = pct / 100          # clear of the terminal blobs at both ends
            yc = y0 + h * frac
            band = find_stem_x_range(shapes, yc - h * 0.01, yc + h * 0.01)
            if band:
                widths.append(band[1] - band[0])
        if widths:
            weights.append(min(widths))
    if weights:
        return sum(weights) / len(weights)
    return PLACEHOLDER_H * 0.5  # sane fallback if 'l'/'I' are ever missing


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 build_composites.py <project.gs2> <GF_Latin_Core.nam>")
        sys.exit(1)

    src_path, nam_path = sys.argv[1], sys.argv[2]
    with open(src_path, encoding="utf-8") as f:
        project = json.load(f)

    current_cps = {int(k.split("-")[1], 16) for k in project["glyphs"]}
    core_cps = load_core_codepoints(nam_path)
    missing = [cp for cp in core_cps if cp not in current_cps]

    stroke_weight = measure_stroke_weight(project)
    dot_component_id = find_existing_dot_component(project)

    made_placeholder = set()
    built, skipped_atomic, skipped_no_base = [], [], []

    for cp in missing:
        ch = chr(cp)
        decomp = unicodedata.normalize("NFD", ch)
        if len(decomp) == 2:
            base_ch, mark_ch = decomp
            mark_uname = unicodedata.name(mark_ch, "")
            if mark_uname in MARK_INFO:
                mark_name, count, side = MARK_INFO[mark_uname]
                g = build_composite_glyph(project, ord(base_ch), mark_name, count, side,
                                           made_placeholder, dot_component_id, stroke_weight)
                if g:
                    project["glyphs"][glyph_key(cp)] = g
                    built.append(cp)
                    continue
                else:
                    skipped_no_base.append(cp)
                    continue
        skipped_atomic.append(cp)

    # Turkish specials
    for target_cp, base_cp, mark in TURKISH_SPECIAL:
        if target_cp in current_cps:
            continue
        if target_cp == 0x0131:
            g = build_dotless_i(project)
        else:
            mark_name, count, side = mark
            g = build_composite_glyph(project, base_cp, mark_name, count, side,
                                       made_placeholder, dot_component_id, stroke_weight)
        if g:
            project["glyphs"][glyph_key(target_cp)] = g
            built.append(target_cp)
            if target_cp in skipped_atomic:
                skipped_atomic.remove(target_cp)

    # Re-run safety net: replace the OLD sharp-diamond placeholder shape on
    # any mark Component that hasn't been hand-drawn yet, with the new round
    # blob shape (does not touch composite glyphs - only the Component's own
    # path, which every glyph instancing it then picks up automatically).
    refreshed = refresh_existing_placeholder_marks(project, stroke_weight)

    # Marks' own shapes just changed (thickness/spacing/gap) - every
    # already-built composite letter's stored mark position was computed
    # against the OLD geometry, so it's now stale even where the mark
    # ITSELF didn't change shape (PAIR_SPACING affects placement, not the
    # dot's shape). Recompute every untouched one.
    repositioned = rebuild_stale_composite_positions(project, dot_component_id, stroke_weight)

    # Task 2/3/4: everything buildable with ZERO new drawing - run these
    # AFTER the refresh above, so they read the marks' final shapes.
    bonus_built = build_bonus_mark_glyphs(project)
    ligature_built = build_ligature_and_stroke_letters(project)
    punctuation_built = build_mechanical_punctuation(project)
    task6_built = build_task6_mechanical(project)
    for cp in bonus_built + ligature_built + punctuation_built + task6_built:
        if cp in skipped_atomic:
            skipped_atomic.remove(cp)

    thorn_fixed = fix_thorn_scale(project)
    pilcrow_fixed = fix_pilcrow_descender(project)

    svg_dir = os.path.dirname(os.path.abspath(src_path))
    eszett_built = import_capital_eszett(project, os.path.join(svg_dir, "capital-eszett.svg"))
    if eszett_built and eszett_built in skipped_atomic:
        skipped_atomic.remove(eszett_built)

    # Google Fonts requires TTF binaries; Glyphr Studio's OTF export flattens
    # Component/composite structure to plain paths, so TTF is also the
    # format that keeps your composites "live". See markdown/GOOGLE_FONTS_SUBMISSION_GUIDE.md.
    project["settings"]["project"]["exportFormat"] = "ttf"

    # Settings > Font > Designer - a plain string field in project.settings.font,
    # safe to set directly (no geometry/rendering risk, unlike glyph shapes).
    project["settings"]["font"]["designer"] = "Baturay Kocatepe"

    # in-place update if this file is already a "_with_composites" output
    # from a previous run (avoids "..._with_composites_with_composites.gs2")
    if src_path.endswith("_with_composites.gs2"):
        out_path = src_path
    else:
        out_path = src_path.rsplit(".", 1)[0] + "_with_composites.gs2"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(project, f, ensure_ascii=False)

    # ---- report ----
    print(f"Wrote {out_path}")
    print("Project export format set to: ttf")
    print(f"Measured stroke weight (from 'l'/'I'): {stroke_weight:.1f} upm")
    print(f"\nComposite glyphs added automatically: {len(built)}")
    print("  " + " ".join(chr(cp) for cp in built))

    if made_placeholder:
        print(f"\nNEW marks that need real artwork ({len(made_placeholder)} shapes to draw once):")
        print("  " + ", ".join(sorted(made_placeholder)))
        print("  (open Components page in Glyphr Studio, find '_mark_<name>',")
        print("   redraw its single placeholder path - every letter using it updates)")

    if refreshed:
        print(f"\nRefreshed {len(refreshed)} existing placeholder mark(s) with the new round blob shape:")
        print("  " + ", ".join(refreshed))
        print("  (still placeholders, just round instead of sharp-diamond now - redraw them for real)")

    if repositioned:
        print(f"\nRepositioned {len(repositioned)} already-built composite letter(s) (stale mark placement):")
        print("  " + " ".join(chr(cp) for cp in repositioned))

    if dot_component_id:
        print("\nReused your existing 'i' dot for: dot-above + dieresis marks (no new drawing).")

    if bonus_built:
        print(f"\nTask 2 - legacy spacing + combining accents added ({len(bonus_built)}, zero new drawing):")
        print("  " + " ".join(chr(cp) for cp in bonus_built))

    if ligature_built:
        print(f"\nTask 3 - ligatures/stroke letters added ({len(ligature_built)}, mechanical from existing letters):")
        print("  " + " ".join(chr(cp) for cp in ligature_built))

    if punctuation_built:
        print(f"\nTask 4 - punctuation/math symbols added ({len(punctuation_built)}, reused from existing shapes):")
        print("  " + " ".join(chr(cp) for cp in punctuation_built))

    if task6_built:
        print(f"\nTask 6 - Eth/Hstroke/Lstroke/ordinals/dotless-j/(c)(R)(tm)/EUR-YEN-cent added ({len(task6_built)}, mechanical):")
        print("  " + " ".join(chr(cp) for cp in task6_built))

    if thorn_fixed:
        print(f"\nTask 7 - rescaled to match sibling letters (was drawn at the wrong size):")
        print("  " + " ".join(chr(cp) for cp in thorn_fixed))

    if pilcrow_fixed:
        print(f"\nTask 7 - extended pilcrow's stems below baseline (per user request):")
        print("  " + " ".join(chr(cp) for cp in pilcrow_fixed))

    if eszett_built:
        print(f"\nTask 8 - imported and positioned {chr(eszett_built)} (capital ss) from capital-eszett.svg")

    if skipped_atomic:
        print(f"\nFinal TODO - genuinely need new, unique hand-drawn artwork ({len(skipped_atomic)}):")
        names = [unicodedata.name(chr(cp), hex(cp)) for cp in skipped_atomic]
        for cp, name in zip(skipped_atomic, names):
            print(f"  U+{cp:04X} {chr(cp)!r:>4}  {name}")

    if skipped_no_base:
        print(f"\nSkipped (base letter not found in project): {skipped_no_base}")


if __name__ == "__main__":
    main()
