# Fluma

Fluma is a liquid organic display typeface with soft, tapering forms. It is intended for headlines, branding, and other display settings. The font covers GF Latin Core, including Turkish (Ç ç Ğ ğ İ ı Ö ö Ş ş Ü ü).

![Fluma specimen cover](documentation/article/specimen1.png)

## About

Fluma is designed by Baturay Kocatepe. All 22 original exports appear in sequence in the [specimen gallery](documentation/SPECIMENS.md) and the [article](documentation/ARTICLE.en_us.html). The images have a [separate license](documentation/image-license.txt).

## Building

The editable design source is the [Glyphr Studio](https://www.glyphrstudio.com) project `sources/Fluma.gs2`. The build converts it to `sources/Fluma.ufo`, adds OpenType mark positioning and source metadata, then compiles TTF and OTF binaries with fontmake.

Exporting directly from Glyphr Studio bypasses the OpenType features in this build. For releases, use the command below after editing the GS2 source.

```sh
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements.txt
bash sources/build.sh
```

- **Primary source:** `sources/Fluma.gs2`. Commit this file when the outlines change.
- **Conversion:** `tools/gs2_to_ufo.py` generates `sources/Fluma.ufo`. The UFO is also kept as a standard editable source for Google Fonts review.
- **Outputs:** `fonts/ttf/Fluma-Regular.ttf` and `fonts/otf/Fluma-Regular.otf`.
- **Composite helper:** `sources/build_composites.py` is a separate source editing tool for deriving accented letters from base forms. It edits the GS2 file in place and is not part of the normal build. If intentionally regenerating composites, back up and review the source change first:
  ```
  python3 sources/build_composites.py sources/Fluma.gs2 sources/GF_Latin_Core.nam
  ```
- **Quality assurance:** run [Fontspector](https://fonttools.github.io/fontspector/) on the TTF from a directory named `fluma` so its family directory check uses the expected name:
  ```
  mkdir -p /tmp/fluma
  cp fonts/ttf/Fluma-Regular.ttf /tmp/fluma/
  fontspector -p googlefonts /tmp/fluma/Fluma-Regular.ttf
  ```
  See the [current technical readiness report](documentation/TECHNICAL_READINESS-2026-09-30.md) and [Fontspector output](documentation/qa/fontspector-2026-09-30-rebuilt.md). The [initial audit](documentation/TECHNICAL_AUDIT-2026-09-30.md) is retained for comparison.
- **Local inventory:** `python3 tools/audit_font.py` compares source, local Latin Core list, and TTF/OTF metadata and outlines. Visual proofing is still needed for aesthetic decisions.

## Changelog

When you update your font (new version or new release), please report all notable changes here, with a date.
[Font Versioning](https://github.com/googlefonts/gf-docs/tree/main/Spec#font-versioning) is based on semver.

**30 September 2026. Version 1.000 build update**

- Added Ĕ and corrected the previously empty ĕ; restored font license and name metadata.
- Added source-driven UFO/TTF/OTF build, mark attachment, dotless i/j handling, and separator glyphs.
- Added all 22 original specimen images, a browsable gallery, and their separate image license.

**15 September 2026. Version 1.000 source milestone**

- Initial character set complete: GF Latin Core (319 characters), including full Turkish support.

## License

This Font Software is licensed under the SIL Open Font License, Version 1.1.
This license is available with a FAQ at https://openfontlicense.org

Specimen images in `documentation/article/` are licensed separately under CC BY-SA 4.0; see `documentation/image-license.txt`.

## Repository Layout

This font repository structure is inspired by [Unified Font Repository v0.3](https://github.com/unified-font-repository/Unified-Font-Repository), modified for the Google Fonts workflow.
