# FlumaFont initial technical audit, 2026-09-30

> **Historical baseline, not the current submission status.** This audit examined the original direct Glyphr Studio exports on 30 September 2026. The 334 mapped codepoints and 71 Fontspector FAIL results below describe those earlier files. The current reproducible build maps 337 codepoints and has 0 FAIL and 12 WARN; see the [current technical readiness report](TECHNICAL_READINESS-2026-09-30.md) and [current Fontspector output](qa/fontspector-2026-09-30-current.md). The original findings are retained for comparison.

## Scope and method

This record is a read-only audit of `sources/Fluma.gs2`, the local `GF_Latin_Core.nam`, the then-current TTF/OTF exports, and package metadata. `tools/audit_font.py` was run with fontTools 4.60.2. The TTF was also tested with the `googlefonts` profile of Fontspector 1.8.0. To let Fontspector read the family directory name correctly, the test used an exact copy of the TTF at the temporary path `/private/tmp/fluma-font-qa/fluma/`. Raw results: [initial Fontspector report](qa/fontspector-2026-09-30.md).

The TTF/OTF files and `.gs2` source were not changed during this audit. The specimen images and Figma file were not opened or edited. This audit did not establish visual glyph quality or Google Fonts acceptance.

## Findings verified at the time

| Check | Result |
|---|---|
| Local GF Latin Core `.nam` | 319 unique encoded codepoints |
| TTF and OTF `cmap` | 334 mapped codepoints in each; all 319 entries from the local list were present |
| Core glyph outlines | No empty outlines except space and non-breaking space |
| Extra mapped glyphs | U+0115 `ĕ` was empty with zero advance width in both the source and exports; U+00AD soft hyphen was also empty |
| TTF/OTF `name` table | Copyright (ID 0), license description (ID 13), and license URL (ID 14) consisted only of whitespace; they did not match the `OFL.txt` header |
| Source metadata | The `copyright`, `license`, and `licenseURL` fields were empty |
| Vertical metrics | Source cap height 1480 and x-height 1000; exported OS/2 cap height 1602 and x-height 1002. The reason for the difference was not verified at the time |
| Local copies | The TTF and OTF under `markdown/fluma/` matched the corresponding font package files by SHA-256 |

Coverage in `cmap` does not establish that glyphs have the right shapes or that every language sequence is shaped correctly.

## Initial Fontspector results, TTF

203 checks: **83 PASS, 23 WARN, 71 FAIL, 90 SKIP, 6 INFO, 0 ERROR/FATAL**. The 71 FAIL results were individual outputs grouped into approximately 10 check families. A copy of the test file was placed in a temporary `fluma/` directory to remove an artificial `dirname_matches_nameid_1` failure. The submission profile did not pass on those initial exports.

| Priority | FAIL family | Initial finding and work needed at the time |
|---|---|---|
| P0 | `opentype/name/empty_records`, `name/trailing_spaces`, `googlefonts/font_copyright` | Remove empty name records or fill them with real values. Copyright ID 0 must exactly match the first line of `OFL.txt`. Source metadata and both exports need to be addressed together. |
| P0 | `base_has_width`, `case_mapping`, `contour_count` | U+0115 `ĕ` was empty with zero width, and U+0114 `Ĕ` was missing. Draw and test a real glyph pair, or correct the accidentally mapped empty U+0115 in the source. This requires a character design decision and new exports. |
| P0 | `googlefonts/glyphsets/shape_languages` | In the Dutch `ÍJ́` and `íj́` sequences, the combining acute did not attach to J/j. GPOS mark attachment or an equivalently verified shaping solution was needed. |
| P0 | `googlefonts/font_names`, `googlefonts/name/version_format` | The check expected the Full Name `Fluma Regular` instead of `Fluma`, and the version name record in the form `Version 1.000` instead of `1.000`. |
| P0 | `googlefonts/vertical_metrics` | `OS/2.sTypoLineGap` and `hhea.lineGap` were 58; the profile expected 0. Because changing vertical metrics affects line spacing in real applications, controlled exports and proofing were needed. |

WARN results also called for a review of contour direction, collinear or overlapping segments, soft-dotted mark behavior, unreachable glyphs, separator glyphs, and `xAvgCharWidth`. The `metadata/unreachable_subsetting` warning needed interpretation because the local test did not include a complete Google Fonts `METADATA.pb` package. The raw report contains the complete list.

## Package and publication status at the time

- The local `googlefont/FlumaFont` directory was not yet a Git repository; a public upstream repository or release had not been verified.
- The README did not yet show an image of the font. Existing specimen images were not used in this audit.
- There was no verified one-command pipeline to convert the `.gs2` source to UFO and rebuild the fonts. The existing `build_composites.py` derived source glyphs; it was not a TTF/OTF build script.
- `requirements.txt` included fontmake, but the README then explicitly said that there was no automated fontmake build. A declared dependency and an implemented pipeline were separate matters.

## Technical sequence proposed at the time

1. Decide the design of U+0115, correct the source, export new TTF/OTF files, and review their outlines and proofs.
2. Align source metadata, name records, copyright, version, and Full Name. Verify the new exports; do not conceal a source inconsistency by patching only the binaries.
3. Develop a source-based solution for vertical metrics and Dutch mark attachment; compare rendering in applications.
4. Establish a source-to-UFO conversion and one-command build, then rerun Fontspector on fresh exports.
5. After resolving technical FAIL results, evaluate outline WARN results with visual proofs. Address the README image and public repository once the specimen package is ready.

These steps record the initial work plan. For completed work and remaining WARN results, use the [current readiness report](TECHNICAL_READINESS-2026-09-30.md).

## Official references consulted for the initial audit

- [Google Fonts Quality Assurance](https://googlefonts.github.io/gf-guide/qa.html)
- [Google Fonts onboarding requirements](https://googlefonts.github.io/gf-guide/onboarding.html)
- [Google Fonts upstream repository structure](https://googlefonts.github.io/gf-guide/upstream.html)
- [Google Fonts license file requirements](https://googlefonts.github.io/gf-guide/license-file.html)
- [Google Fonts GF Latin Core definition](https://github.com/googlefonts/glyphsets/blob/main/GLYPHSETS.md#gf-latin-core)

At the time of the audit, the onboarding page still named FontBakery while the QA page described Fontspector as the current tool. This audit used the Fontspector command from the QA page.
