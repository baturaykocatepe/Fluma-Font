# FlumaFont technical readiness, 2026-09-30

> **Specimen update through 2026-10-24:** The designer replaced all 22 PNGs in `documentation/article/` with revised 1600 × 900 exports on 23 October, supplied further replacements for pages 19, 20, and 21, and corrected page 20's lower-right caption on 24 October. The font source, binaries, and September QA results did not change. The specimen section below describes the current repository images; the [initial audit](TECHNICAL_AUDIT-2026-09-30.md) retains the earlier export history.

## Verified package

The canonical editable source is `sources/Fluma.gs2`. `sources/build.sh` converts it to `sources/Fluma.ufo` and builds `fonts/ttf/Fluma-Regular.ttf` and `fonts/otf/Fluma-Regular.otf`. Its finalization step adds a static upright STAT axis and Latin `meta` tags. Python dependencies are listed in `requirements.txt`. Two consecutive builds produced byte-identical TTF, OTF, WOFF, and WOFF2 files with the build date pinned to 2026-09-30 UTC. The converter now omits sub-unit line fragments that become zero-length when compiled to integer TrueType coordinates. Relative to the preceding 14-WARN TTF, all on-curve points and the cmap, hmtx, GDEF, GPOS, GSUB, name, STAT, and meta tables remain identical; six off-curve points in five glyphs shift by one unit. The GS2 design source was unchanged by this cleanup.

The source includes the previously missing Ĕ and a nonempty ĕ derived from the existing E/e and breve shapes. It also contains license and copyright metadata that matches `OFL.txt`. The UFO conversion adds OpenType mark attachment and dotless i/j substitution for top combining marks. Empty U+00AD was removed; empty zero-width line and paragraph separators were added. U+25CC dotted circle is generated as a mark support glyph.

The final TTF, OTF, WOFF, and WOFF2 each map 337 Unicode codepoints. All 319 codepoints in `GF_Latin_Core.nam` are present with outlines except the expected spaces. That local file was byte-identical to the [official glyphsets `GF_Latin_Core.nam`](https://github.com/googlefonts/glyphsets/blob/main/data/results/nam/GF_Latin_Core.nam) fetched on 2026-09-30. The TTF and OTF copyright, license names, cap height and x-height match the source. WOFF and WOFF2 are generated from the TTF and contain the same OpenType features. The current TTF and OTF copies under `markdown/fluma/` have matching SHA-256 hashes. A visual side-by-side proof of selected old and new strings is in `qa/proof-2026-09-30.png`; it does not replace full application and design proofing.

## Automated QA

Fontspector 1.8.0, `googlefonts` profile, current TTF, correctly named `fluma` family directory and working network: **203 checks, 107 PASS, 12 WARN, 0 FAIL, 0 ERROR, 0 FATAL, 81 SKIP, 8 INFO**. [Current full report](qa/fontspector-2026-09-30-current.md) and [review of every remaining warning](qa/WARN_REVIEW-2026-09-30.md). The first reproducible build had 16 WARN; STAT, `meta`, and two zero-length outline warnings were resolved. The first Glyphr export had 71 FAIL in the [initial audit](TECHNICAL_AUDIT-2026-09-30.md). The direct Glyphr export does not include the UFO build's OpenType fixes; future releases must use `sources/build.sh`.

The remaining WARN items require design or distribution judgment rather than a mechanical pass:

| Area | Current interpretation |
|---|---|
| Contours and outlines | The zero-length and overlapping-segment checks now pass. Two jaggy double-acute outlines remain; decomposed alternate carons and unusual contour counts need manual glyph review. Preserve the approved forms until reviewed. |
| Glyph coverage | GF Latin Core passes; auxiliary characters for some other languages and the optional rupee sign are not included. Do not claim broader language coverage from the Latin Core result. |
| Spacing | Several math symbols have different advances. Review as a design choice before changing widths. |
| Metadata and tables | The static STAT and Latin ScriptLangTags `meta` tables are now present. Vendor ID is `NONE` because no registered vendor ID was provided. The local package has no Google Fonts `METADATA.pb`, so the subsetting warning is a staging condition. |
| Unhinted smoothing | The font uses GASP 0x000A as the [Google Fonts static font guide](https://googlefonts.github.io/gf-guide/statics.html) recommends for an unhinted display face. Fontspector 1.8.0 separately warns that 0x000F is expected. This conflict needs Google Fonts review; the explicit unhinted guidance was followed. |

## Specimen images

The first set of 22 user-supplied PNGs was copied from `specimen/` to `documentation/article/` and verified by SHA-256 at that time. On 2026-10-23, the designer supplied revised files directly in `documentation/article/`, including later replacements for pages 19, 20, and 21. On 2026-10-24, page 20 was replaced again. The [current gallery](SPECIMENS.md) and `documentation/article/ARTICLE.en_us.html` reference all 22 current repository images in order. A current file check found all 22 to be 1600 × 900 PNGs, each below 1.75 MB. The user explicitly approved CC BY-SA 4.0 for public repository use, recorded in `documentation/image-license.txt`. Google Fonts recommends 1 to 8 About images but does not state an eight-image maximum; the user requested consideration of all 22.

In the current files, specimen 19's top-right label reads “FLUMA / REGULAR,” and specimen 21 reports “337 encoded characters,” matching the current font's mapped codepoint count. The embedded designer credits previously observed on pages 1, 12, 21, and 22 have been removed in the revised images. Specimen 20's top-left heading reads “CHARACTER,” and its revised lower-right caption reads “COMPARISON”. The page sequence remains 01 through 22. Google's editorial review may request fewer or adjusted About images; no such acceptance can be guaranteed locally. No image pixels were edited as part of this technical report update.

## Publication dependencies

- The public [Fluma-Font GitHub repository](https://github.com/baturaykocatepe/Fluma-Font) exists. A fresh public clone was rebuilt and produced byte-identical TTF, OTF, WOFF, and WOFF2 files; it contained all 22 article images. The unchanged source and binaries also passed the [GitHub Actions build and audit on 2026-10-23](https://github.com/baturaykocatepe/Fluma-Font/actions/runs/40013330623). As checked on 2026-10-23, the [Google Fonts submission issue #11060](https://github.com/google/fonts/issues/11060) is open and links to this repository and all 22 current images. Its two personal declaration boxes are checked, the author is subscribed, and the issue is in the “Submissions to review” milestone. This is review queue status, not acceptance.
- The author signed Google's Individual Contributor License Agreement personally. On 2026-09-30, the Google CLA Manage Agreements page, signed in as the author's account, listed a Google Individual CLA under “Baturay Kocatepe.” The author confirmed that no retail/restricted Fluma version exists and that he alone holds the rights to the typeface and 22 images. Those ownership statements are author attestations. Font design quality, ownership/originality review, and final catalog acceptance belong to Google Fonts; automated QA cannot guarantee them.
- The four direct Glyphr Studio exports of 2026-09-30 are preserved locally in `fonts/exports-glyphr-studio-2026-09-30/` and excluded from Git. They map 336 codepoints and lack the GDEF/GSUB features of the release build. The four files in the main `fonts/` format folders are from `sources/build.sh`.
- During onboarding, inspect the 12 remaining WARN items in the [warning review](qa/WARN_REVIEW-2026-09-30.md) in light of Google's specific feedback and proof the rebuilt font in actual target apps. WARN-level findings need human judgment; there is no known 0-FAIL blocker requiring a speculative contour change before review. Reinstalling the font locally is required for existing applications to use these new binaries.

## Reference template comparison

The former `_reference-template` directory was a clone of `googlefonts/googlefonts-project-template`. It was moved intact to `../googlefonts-project-template-reference/` so example Radio Canada sources and assets cannot be confused with Fluma deliverables. The essential upstream files are present in this Fluma repository: `AUTHORS.txt`, `CONTRIBUTORS.txt`, `OFL.txt`, README with a specimen and build instructions, `documentation/`, `sources/Fluma.gs2`, committed `sources/Fluma.ufo`, `sources/build.sh`, `fonts/ttf/`, `requirements.txt`, and `.gitignore`. A small read-only GitHub Actions build check was added in place of the template's wider workflow.

The template's `Makefile`, `config.yaml`, proof-page scripts, `requirements.in`, Renovate configuration, and templating metadata are optional conveniences, not missing Google Fonts requirements. `build.sh` already fills the required one-command build role of `config.yaml`. Its Radio Canada files must not be copied into Fluma. The current [Article guide](https://googlefonts.github.io/gf-guide/article.html) and [promotion guide](https://googlefonts.github.io/gf-guide/promotion.html) place Article images together under an `article/` directory; Fluma uses `documentation/article/` for this upstream package.

## Submission assertions and CLA

The [current Google Fonts new-font issue template](https://github.com/google/fonts/blob/main/.github/ISSUE_TEMPLATE/1_add-font.md) asks the copyright holder to affirm that the entire family is OFL, no larger retail/Pro version exists, all copyright holders have authorized publication, AI tools used during creation are disclosed, the upstream repo will be maintained, and the full contribution rules are met. The source, license, name, and Latin Core claims are locally supported. The author confirmed sole copyright and no retail/restricted version in this conversation. The [opened issue](https://github.com/google/fonts/issues/11060) discloses GPT Image, Illustrator Image Trace, Adobe Firefly, Claude Code, and Codex roles. Its personal contribution and maintenance declarations are now checked by the copyright holder. The Google Individual CLA is on file in the author's account. The [fontdata name check](https://namecheck.fontdata.com/?q=Fluma) returned no exact match for Fluma on 2026-09-30, though it is not a trademark clearance.

## Official references

- [Google Fonts onboarding](https://googlefonts.github.io/gf-guide/onboarding.html)
- [Google Fonts upstream repository structure](https://googlefonts.github.io/gf-guide/upstream.html)
- [Google Fonts QA and Fontspector](https://googlefonts.github.io/gf-guide/qa.html)
- [Google Fonts promotion and image requirements](https://googlefonts.github.io/gf-guide/promotion.html)
