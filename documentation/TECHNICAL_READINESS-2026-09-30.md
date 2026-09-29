# FlumaFont technical readiness, 2026-09-30

## Verified package

The canonical editable source is `sources/Fluma.gs2`. `sources/build.sh` converts it to `sources/Fluma.ufo` and builds `fonts/ttf/Fluma-Regular.ttf` and `fonts/otf/Fluma-Regular.otf`. Python dependencies are listed in `requirements.txt`. Two consecutive builds produced byte-identical TTF and OTF files with the build date pinned to 2026-09-30 UTC.

The source includes the previously missing Ĕ and a nonempty ĕ derived from the existing E/e and breve shapes. It also contains license and copyright metadata that matches `OFL.txt`. The UFO conversion adds OpenType mark attachment and dotless i/j substitution for top combining marks. Empty U+00AD was removed; empty zero-width line and paragraph separators were added. U+25CC dotted circle is generated as a mark support glyph.

The final TTF and OTF each map 337 Unicode codepoints. All 319 codepoints in the local `GF_Latin_Core.nam` are present with outlines except the expected spaces. The TTF and OTF copyright, license names, cap height and x-height match the source. The copies under `markdown/fluma/` have the same SHA-256 hashes as the package binaries. A visual side-by-side proof of selected old and new strings is in `qa/proof-2026-09-30.png`; it does not replace full application and design proofing.

## Automated QA

Fontspector 1.8.0, `googlefonts` profile, final TTF, correctly named `fluma` family directory and working network: **203 checks, 102 PASS, 15 WARN, 0 FAIL, 0 ERROR, 0 FATAL, 84 SKIP, 6 INFO**. [Full final report](qa/fontspector-2026-09-30-rebuilt.md). The first Glyphr export had 71 FAIL in the [initial audit](TECHNICAL_AUDIT-2026-09-30.md). The direct Glyphr export does not include the UFO build's OpenType fixes; future TTF/OTF releases must use `sources/build.sh`.

The remaining WARN items require design or distribution judgment rather than a mechanical pass:

| Area | Current interpretation |
|---|---|
| Contours and outlines | Tiny colinear and overlapping segments, and two jaggy double-acute outlines remain. Decomposed alternate carons and unusual contour counts need manual glyph review. Preserve the approved forms until reviewed. |
| Glyph coverage | GF Latin Core passes; auxiliary characters for some other languages and the optional rupee sign are not included. Do not claim broader language coverage from the Latin Core result. |
| Spacing | Several math symbols have different advances. Review as a design choice before changing widths. |
| Metadata and tables | Static font has no STAT or meta ScriptLangTags table. Vendor ID is `NONE` because no registered vendor ID was provided. The local package has no Google Fonts `METADATA.pb`, so the subsetting warning is a staging condition. |

## Specimen images

All 22 user-supplied PNGs were copied without modification from `specimen/` to `documentation/article/`. A SHA-256 comparison verified every copy. They are indexed in `documentation/SPECIMENS.md` and referenced in order 01 through 22 by `documentation/ARTICLE.en_us.html`. All are 1600 × 900 PNGs and each is below 1.75 MB. The user explicitly approved CC BY-SA 4.0 for public repository use, recorded in `documentation/image-license.txt`. Google Fonts recommends 1 to 8 About images, but its guide does not state an eight-image maximum; the user explicitly requested all 22 despite that recommendation.

Specimen 21 visibly states “334 encoded characters,” which reflects the first export. The rebuilt font has 337 mapped codepoints. The original PNG was preserved, and the gallery caption states the current value. Some images contain embedded designer credits, while Google Fonts requests no embedded credits in About images. The page numbers are part of the 22-page sequence and are not prohibited by the guide. Google's editorial review may request a shorter or adjusted image selection; no such acceptance can be guaranteed locally.

## Publication dependencies

- A local Git repository was initialized for the prepared package. A public, maintained GitHub or comparable VCS repository and a submission issue are still required. The local `gh` credentials currently report an invalid token, so the package has not been pushed or submitted.
- The copyright holder must complete Google's Contributor License Agreement personally. Font design quality, ownership/originality review, and final catalog acceptance belong to Google Fonts; automated QA cannot guarantee them.
- Before publishing, inspect the 15 WARN items in the full report and proof the rebuilt font in actual target apps. Reinstalling the font locally is required for existing applications to use these new binaries.

## Official references

- [Google Fonts onboarding](https://googlefonts.github.io/gf-guide/onboarding.html)
- [Google Fonts upstream repository structure](https://googlefonts.github.io/gf-guide/upstream.html)
- [Google Fonts QA and Fontspector](https://googlefonts.github.io/gf-guide/qa.html)
- [Google Fonts promotion and image requirements](https://googlefonts.github.io/gf-guide/promotion.html)
