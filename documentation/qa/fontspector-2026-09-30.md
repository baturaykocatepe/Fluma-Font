## FontSpector report

fontspector version: 1.8.0






## Check results




<details><summary>[25] /private/tmp/fluma-font-qa/fluma/Fluma-Regular.ttf</summary>
<div>


<details>
    <summary>🔥 <b>FAIL</b> Check name table for empty records. (opentype/name/empty_records)</summary>
    <div>


> Check the name table for empty records, as this can cause problems in Adobe apps.




Original proposal: [https://github.com/fonttools/fontbakery/pull/2369]





- 🔥 **FAIL** Empty name record found for name ID=COPYRIGHT_NOTICE platform ID=0 encoding ID=3 [code: empty-record]




- 🔥 **FAIL** Empty name record found for name ID=TRADEMARK platform ID=0 encoding ID=3 [code: empty-record]




- 🔥 **FAIL** Empty name record found for name ID=MANUFACTURER platform ID=0 encoding ID=3 [code: empty-record]




- 🔥 **FAIL** Empty name record found for name ID=VENDOR_URL platform ID=0 encoding ID=3 [code: empty-record]




- 🔥 **FAIL** Empty name record found for name ID=LICENSE_DESCRIPTION platform ID=0 encoding ID=3 [code: empty-record]




- 🔥 **FAIL** Empty name record found for name ID=LICENSE_URL platform ID=0 encoding ID=3 [code: empty-record]




- 🔥 **FAIL** Empty name record found for name ID=COPYRIGHT_NOTICE platform ID=1 encoding ID=0 [code: empty-record]




- 🔥 **FAIL** Empty name record found for name ID=TRADEMARK platform ID=1 encoding ID=0 [code: empty-record]




- 🔥 **FAIL** Empty name record found for name ID=MANUFACTURER platform ID=1 encoding ID=0 [code: empty-record]




- 🔥 **FAIL** Empty name record found for name ID=VENDOR_URL platform ID=1 encoding ID=0 [code: empty-record]




- 🔥 **FAIL** Empty name record found for name ID=LICENSE_DESCRIPTION platform ID=1 encoding ID=0 [code: empty-record]




- 🔥 **FAIL** Empty name record found for name ID=LICENSE_URL platform ID=1 encoding ID=0 [code: empty-record]




- 🔥 **FAIL** Empty name record found for name ID=COPYRIGHT_NOTICE platform ID=3 encoding ID=1 [code: empty-record]




- 🔥 **FAIL** Empty name record found for name ID=TRADEMARK platform ID=3 encoding ID=1 [code: empty-record]




- 🔥 **FAIL** Empty name record found for name ID=MANUFACTURER platform ID=3 encoding ID=1 [code: empty-record]




- 🔥 **FAIL** Empty name record found for name ID=VENDOR_URL platform ID=3 encoding ID=1 [code: empty-record]




- 🔥 **FAIL** Empty name record found for name ID=LICENSE_DESCRIPTION platform ID=3 encoding ID=1 [code: empty-record]




- 🔥 **FAIL** Empty name record found for name ID=LICENSE_URL platform ID=3 encoding ID=1 [code: empty-record]



</div>
</details>





<details>
    <summary>🔥 <b>FAIL</b> Check base characters have non-zero advance width. (base_has_width)</summary>
    <div>


> Base characters should have non-zero advance width. Additionally, certain Unicode characters (such as zero-width joiners and zero-width spaces) are expected to have zero advance width. If they have a non-zero width, they may cause unexpected spacing in text layout.




Original proposal: [Rod on chat, https://github.com/fonttools/fontspector/issues/518]





- 🔥 **FAIL** The following glyphs had zero advance width:

* uni0115 (Some(277)) [code: zero-width-bases]



</div>
</details>





<details>
    <summary>🔥 <b>FAIL</b> Ensure the font supports case swapping for all its glyphs. (case_mapping)</summary>
    <div>


> Ensure that no glyph lacks its corresponding upper or lower counterpart (but only when unicode supports case-mapping).




Original proposal: [https://github.com/googlefonts/fontbakery/issues/3230]





- 🔥 **FAIL** Missing case-swapping counterpart for U+0115 [code: missing-case-counterparts]



</div>
</details>





<details>
    <summary>🔥 <b>FAIL</b> Check if each glyph has the recommended amount of contours. (contour_count)</summary>
    <div>


> Visually QAing thousands of glyphs by hand is tiring. Most glyphs can only be constructured in a handful of ways. This means a glyph's contour count will only differ slightly amongst different fonts, e.g a 'g' could either be 2 or 3 contours, depending on whether its double story or single story.
>
> However, a quotedbl should have 2 contours, unless the font belongs to a display family.
>
> This check currently does not cover variable fonts because there's plenty of alternative ways of constructing glyphs with multiple outlines for each feature in a VarFont. The expected contour count data for this check is currently optimized for the typical construction of glyphs in static fonts.




Original proposal: [https://github.com/fonttools/fontbakery/issues/4829]





- 🔥 **FAIL** The following glyphs have no contours even though they were expected to have some:
* uni0115 (U+0115): found 0, expected one of: [2, 3, 6] [code: no-contour]




- ⚠️ **WARN** This check inspects the glyph outlines and detects the total number of contours in each of them. The expected values are
     inferred from the typical amounts of contours observed in a
     large collection of reference font families. The divergences
     listed below may simply indicate a significantly different
     design on some of your glyphs. On the other hand, some of these
     may flag actual bugs in the font such as glyphs mapped to an
     incorrect codepoint. Please consider reviewing the design and
     codepoint assignment of these to make sure they are correct.


    The following glyphs do not have the recommended number of contours:
* uni00EE (U+00EE): found 4, expected one of: [2, 3, 6]
* uni012B (U+012B): found 3, expected one of: [2, 6]
* uni02C6 (U+02C6): found 2, expected one of: [1, 5]
* uni02DC (U+02DC): found 2, expected one of: [1]
* uni0302 (U+0302): found 2, expected one of: [1]
* uni0303 (U+0303): found 2, expected one of: [1] [code: contour-count]



</div>
</details>





<details>
    <summary>🔥 <b>FAIL</b> Name table records must not have trailing spaces. (name/trailing_spaces)</summary>
    <div>


> This check ensures that no entries in the name table end in                 spaces, begin with spaces, or contain double spaces. Such                 whitespace issues, particularly in font names, can be confusing                 to users. In most cases this can be fixed by removing extraneous                 spaces from the metadata fields in the font editor.




Original proposal: [https://github.com/googlefonts/fontbakery/issues/2417]





- 🔥 **FAIL** Name table record 0/3/0/COPYRIGHT_NOTICE has trailing spaces that must be removed:
` ` [code: trailing-space]




- 🔥 **FAIL** Name table record 0/3/0/COPYRIGHT_NOTICE has leading spaces that must be removed:
` ` [code: leading-space]




- 🔥 **FAIL** Name table record 0/3/0/UNIQUE_ID has leading spaces that must be removed:
` : Fluma` [code: leading-space]




- 🔥 **FAIL** Name table record 0/3/0/TRADEMARK has trailing spaces that must be removed:
` ` [code: trailing-space]




- 🔥 **FAIL** Name table record 0/3/0/TRADEMARK has leading spaces that must be removed:
` ` [code: leading-space]




- 🔥 **FAIL** Name table record 0/3/0/MANUFACTURER has trailing spaces that must be removed:
` ` [code: trailing-space]




- 🔥 **FAIL** Name table record 0/3/0/MANUFACTURER has leading spaces that must be removed:
` ` [code: leading-space]




- 🔥 **FAIL** Name table record 0/3/0/VENDOR_URL has trailing spaces that must be removed:
` ` [code: trailing-space]




- 🔥 **FAIL** Name table record 0/3/0/VENDOR_URL has leading spaces that must be removed:
` ` [code: leading-space]




- 🔥 **FAIL** Name table record 0/3/0/LICENSE_DESCRIPTION has trailing spaces that must be removed:
` ` [code: trailing-space]




- 🔥 **FAIL** Name table record 0/3/0/LICENSE_DESCRIPTION has leading spaces that must be removed:
` ` [code: leading-space]




- 🔥 **FAIL** Name table record 0/3/0/LICENSE_URL has trailing spaces that must be removed:
` ` [code: trailing-space]




- 🔥 **FAIL** Name table record 0/3/0/LICENSE_URL has leading spaces that must be removed:
` ` [code: leading-space]




- 🔥 **FAIL** Name table record 1/0/0/COPYRIGHT_NOTICE has trailing spaces that must be removed:
` ` [code: trailing-space]




- 🔥 **FAIL** Name table record 1/0/0/COPYRIGHT_NOTICE has leading spaces that must be removed:
` ` [code: leading-space]




- 🔥 **FAIL** Name table record 1/0/0/UNIQUE_ID has leading spaces that must be removed:
` : Fluma` [code: leading-space]




- 🔥 **FAIL** Name table record 1/0/0/TRADEMARK has trailing spaces that must be removed:
` ` [code: trailing-space]




- 🔥 **FAIL** Name table record 1/0/0/TRADEMARK has leading spaces that must be removed:
` ` [code: leading-space]




- 🔥 **FAIL** Name table record 1/0/0/MANUFACTURER has trailing spaces that must be removed:
` ` [code: trailing-space]




- 🔥 **FAIL** Name table record 1/0/0/MANUFACTURER has leading spaces that must be removed:
` ` [code: leading-space]




- 🔥 **FAIL** Name table record 1/0/0/VENDOR_URL has trailing spaces that must be removed:
` ` [code: trailing-space]




- 🔥 **FAIL** Name table record 1/0/0/VENDOR_URL has leading spaces that must be removed:
` ` [code: leading-space]




- 🔥 **FAIL** Name table record 1/0/0/LICENSE_DESCRIPTION has trailing spaces that must be removed:
` ` [code: trailing-space]




- 🔥 **FAIL** Name table record 1/0/0/LICENSE_DESCRIPTION has leading spaces that must be removed:
` ` [code: leading-space]




- 🔥 **FAIL** Name table record 1/0/0/LICENSE_URL has trailing spaces that must be removed:
` ` [code: trailing-space]




- 🔥 **FAIL** Name table record 1/0/0/LICENSE_URL has leading spaces that must be removed:
` ` [code: leading-space]




- 🔥 **FAIL** Name table record 3/1/1033/COPYRIGHT_NOTICE has trailing spaces that must be removed:
` ` [code: trailing-space]




- 🔥 **FAIL** Name table record 3/1/1033/COPYRIGHT_NOTICE has leading spaces that must be removed:
` ` [code: leading-space]




- 🔥 **FAIL** Name table record 3/1/1033/UNIQUE_ID has leading spaces that must be removed:
` : Fluma` [code: leading-space]




- 🔥 **FAIL** Name table record 3/1/1033/TRADEMARK has trailing spaces that must be removed:
` ` [code: trailing-space]




- 🔥 **FAIL** Name table record 3/1/1033/TRADEMARK has leading spaces that must be removed:
` ` [code: leading-space]




- 🔥 **FAIL** Name table record 3/1/1033/MANUFACTURER has trailing spaces that must be removed:
` ` [code: trailing-space]




- 🔥 **FAIL** Name table record 3/1/1033/MANUFACTURER has leading spaces that must be removed:
` ` [code: leading-space]




- 🔥 **FAIL** Name table record 3/1/1033/VENDOR_URL has trailing spaces that must be removed:
` ` [code: trailing-space]




- 🔥 **FAIL** Name table record 3/1/1033/VENDOR_URL has leading spaces that must be removed:
` ` [code: leading-space]




- 🔥 **FAIL** Name table record 3/1/1033/LICENSE_DESCRIPTION has trailing spaces that must be removed:
` ` [code: trailing-space]




- 🔥 **FAIL** Name table record 3/1/1033/LICENSE_DESCRIPTION has leading spaces that must be removed:
` ` [code: leading-space]




- 🔥 **FAIL** Name table record 3/1/1033/LICENSE_URL has trailing spaces that must be removed:
` ` [code: trailing-space]




- 🔥 **FAIL** Name table record 3/1/1033/LICENSE_URL has leading spaces that must be removed:
` ` [code: leading-space]



</div>
</details>





<details>
    <summary>🔥 <b>FAIL</b> Shapes languages in all GF glyphsets. (googlefonts/glyphsets/shape_languages)</summary>
    <div>


> This check uses a heuristic to determine which GF glyphsets a font supports. Then it checks the font for correct shaping behaviour for all languages in those glyphsets.




Original proposal: [https://github.com/googlefonts/fontbakery/issues/4147]





- 🔥 **FAIL** Failed language shaping:

| Message                                                              | Languages         |
|----------------------------------------------------------------------|-------------------|
| Mandatory orthography codepoints:                                    | * nl_Latn (Dutch) |
|   Shaper didn't attach uni0301 to uni004A when shaping the text 'ÍJ́' |                   |
|   Shaper didn't attach uni0301 to uni006A when shaping the text 'íj́' |                   | [code: failed-language-shaping]




- ⚠️ **WARN** Warning language shaping:

| Message                                                             | Languages                    |
|---------------------------------------------------------------------|------------------------------|
| Auxiliary orthography codepoints:                                   | * ca_Latn (Catalan)          |
|   The following auxiliary characters are missing from the font: Ĕ   |                              |
|   The following auxiliary characters are missing from the font: Ĭ   |                              |
|   The following auxiliary characters are missing from the font: Ŀ   |                              |
|   The following auxiliary characters are missing from the font: Ŏ   |                              |
|   The following auxiliary characters are missing from the font: Ō   |                              |
|   The following auxiliary characters are missing from the font: Ŭ   |                              |
|   The following auxiliary characters are missing from the font: ĭ   |                              |
|   The following auxiliary characters are missing from the font: ŀ   |                              |
|   The following auxiliary characters are missing from the font: ŏ   |                              |
|   The following auxiliary characters are missing from the font: ō   |                              |
|   The following auxiliary characters are missing from the font: ŭ   |                              |
| Auxiliary orthography codepoints:                                   | * nb_Latn (Norwegian Bokmål) |
|   The following auxiliary characters are missing from the font: Ǎ   |                              |
|   The following auxiliary characters are missing from the font: Ŋ   |                              |
|   The following auxiliary characters are missing from the font: Ŧ   |                              |
|   The following auxiliary characters are missing from the font: ǎ   |                              |
|   The following auxiliary characters are missing from the font: ŋ   |                              |
|   The following auxiliary characters are missing from the font: ŧ   |                              |
| Auxiliary orthography codepoints:                                   | * de_Latn (German)           |
|   The following auxiliary characters are missing from the font: Ĕ   |                              |
|   The following auxiliary characters are missing from the font: Ĭ   |                              |
|   The following auxiliary characters are missing from the font: Ŏ   |                              |
|   The following auxiliary characters are missing from the font: Ō   |                              |
|   The following auxiliary characters are missing from the font: Ŭ   |                              |
|   The following auxiliary characters are missing from the font: ĭ   |                              |
|   The following auxiliary characters are missing from the font: ŏ   |                              |
|   The following auxiliary characters are missing from the font: ō   |                              |
|   The following auxiliary characters are missing from the font: ſ   |                              |
|   The following auxiliary characters are missing from the font: ŭ   |                              |
| Auxiliary orthography codepoints:                                   | * cs_Latn (Czech)            |
|   The following auxiliary characters are missing from the font: Ĕ   | * cy_Latn (Welsh)            |
|   The following auxiliary characters are missing from the font: Ĭ   | * es_Latn (Spanish)          |
|   The following auxiliary characters are missing from the font: Ŏ   | * hu_Latn (Hungarian)        |
|   The following auxiliary characters are missing from the font: Ō   | * pt_Latn (Portuguese)       |
|   The following auxiliary characters are missing from the font: Ŭ   | * sk_Latn (Slovak)           |
|   The following auxiliary characters are missing from the font: ĭ   | * tr_Latn (Turkish)          |
|   The following auxiliary characters are missing from the font: ŏ   |                              |
|   The following auxiliary characters are missing from the font: ō   |                              |
|   The following auxiliary characters are missing from the font: ŭ   |                              |
| Auxiliary orthography codepoints:                                   | * da_Latn (Danish)           |
|   The following auxiliary characters are missing from the font: Ǿ   |                              |
|   The following auxiliary characters are missing from the font: ǿ   |                              |
| Auxiliary orthography codepoints:                                   | * lt_Latn (Lithuanian)       |
|   The following auxiliary characters are missing from the font: Ẽ   |                              |
|   The following auxiliary characters are missing from the font: Ĩ   |                              |
|   The following auxiliary characters are missing from the font: Ũ   |                              |
|   The following auxiliary characters are missing from the font: ẽ   |                              |
|   The following auxiliary characters are missing from the font: ĩ   |                              |
|   The following auxiliary characters are missing from the font: ũ   |                              |
|   Shaper didn't attach uni0301 to uni0104 when shaping the text 'Ą́' |                              |
|   Shaper didn't attach uni0303 to uni0104 when shaping the text 'Ą̃' |                              |
|   Shaper didn't attach uni0301 to uni0118 when shaping the text 'Ę́' |                              |
|   Shaper didn't attach uni0303 to uni0118 when shaping the text 'Ę̃' |                              |
|   Shaper didn't attach uni0301 to uni0116 when shaping the text 'Ė́' |                              |
|   Shaper didn't attach uni0303 to uni0116 when shaping the text 'Ė̃' |                              |
|   Shaper didn't attach uni0301 to uni0130 when shaping the text 'İ́' |                              |
|   Shaper didn't attach uni0301 to uni0130 when shaping the text 'İ́' |                              |
|   Shaper didn't attach uni0300 to uni0130 when shaping the text 'İ̀' |                              |
|   Shaper didn't attach uni0300 to uni0130 when shaping the text 'İ̀' |                              |
|   Shaper didn't attach uni0303 to uni0130 when shaping the text 'İ̃' |                              |
|   Shaper didn't attach uni0303 to uni0130 when shaping the text 'İ̃' |                              |
|   Shaper didn't attach uni0301 to uni012E when shaping the text 'Į́' |                              |
|   Shaper didn't attach uni0307 to uni012E when shaping the text 'Į̇́' |                              |
|   Shaper didn't attach uni0301 to uni0307 when shaping the text 'Į̇́' |                              |
|   Shaper didn't attach uni0303 to uni012E when shaping the text 'Į̃' |                              |
|   Shaper didn't attach uni0307 to uni012E when shaping the text 'Į̇̃' |                              |
|   Shaper didn't attach uni0303 to uni0307 when shaping the text 'Į̇̃' |                              |
|   Shaper didn't attach uni0303 to uni004A when shaping the text 'J̃' |                              |
|   Shaper didn't attach uni0307 to uni004A when shaping the text 'J̇̃' |                              |
|   Shaper didn't attach uni0303 to uni0307 when shaping the text 'J̇̃' |                              |
|   Shaper didn't attach uni0303 to uni004C when shaping the text 'L̃' |                              |
|   Shaper didn't attach uni0303 to uni004D when shaping the text 'M̃' |                              |
|   Shaper didn't attach uni0303 to uni0052 when shaping the text 'R̃' |                              |
|   Shaper didn't attach uni0301 to uni0172 when shaping the text 'Ų́' |                              |
|   Shaper didn't attach uni0303 to uni0172 when shaping the text 'Ų̃' |                              |
|   Shaper didn't attach uni0301 to uni016A when shaping the text 'Ū́' |                              |
|   Shaper didn't attach uni0303 to uni016A when shaping the text 'Ū̃' |                              |
|   Shaper didn't attach uni0301 to uni0105 when shaping the text 'ą́' |                              |
|   Shaper didn't attach uni0303 to uni0105 when shaping the text 'ą̃' |                              |
|   Shaper didn't attach uni0301 to uni0119 when shaping the text 'ę́' |                              |
|   Shaper didn't attach uni0303 to uni0119 when shaping the text 'ę̃' |                              |
|   Shaper didn't attach uni0301 to uni0117 when shaping the text 'ė́' |                              |
|   Shaper didn't attach uni0303 to uni0117 when shaping the text 'ė̃' |                              |
|   Shaper didn't attach uni0307 to uni0069 when shaping the text 'i̇́' |                              |
|   Shaper didn't attach uni0301 to uni0307 when shaping the text 'i̇́' |                              |
|   Shaper didn't attach uni0307 to uni0069 when shaping the text 'i̇̀' |                              |
|   Shaper didn't attach uni0300 to uni0307 when shaping the text 'i̇̀' |                              |
|   Shaper didn't attach uni0307 to uni0069 when shaping the text 'i̇̃' |                              |
|   Shaper didn't attach uni0303 to uni0307 when shaping the text 'i̇̃' |                              |
|   Shaper didn't attach uni0301 to uni012F when shaping the text 'į́' |                              |
|   Shaper didn't attach uni0307 to uni012F when shaping the text 'į̇́' |                              |
|   Shaper didn't attach uni0301 to uni0307 when shaping the text 'į̇́' |                              |
|   Shaper didn't attach uni0303 to uni012F when shaping the text 'į̃' |                              |
|   Shaper didn't attach uni0307 to uni012F when shaping the text 'į̇̃' |                              |
|   Shaper didn't attach uni0303 to uni0307 when shaping the text 'į̇̃' |                              |
|   Shaper didn't attach uni0303 to uni006A when shaping the text 'j̃' |                              |
|   Shaper didn't attach uni0307 to uni006A when shaping the text 'j̇̃' |                              |
|   Shaper didn't attach uni0303 to uni0307 when shaping the text 'j̇̃' |                              |
|   Shaper didn't attach uni0303 to uni006C when shaping the text 'l̃' |                              |
|   Shaper didn't attach uni0303 to uni006D when shaping the text 'm̃' |                              |
|   Shaper didn't attach uni0303 to uni0072 when shaping the text 'r̃' |                              |
|   Shaper didn't attach uni0301 to uni0173 when shaping the text 'ų́' |                              |
|   Shaper didn't attach uni0303 to uni0173 when shaping the text 'ų̃' |                              |
|   Shaper didn't attach uni0301 to uni016B when shaping the text 'ū́' |                              |
|   Shaper didn't attach uni0303 to uni016B when shaping the text 'ū̃' |                              |
| Auxiliary orthography codepoints:                                   | * lv_Latn (Latvian)          |
|   The following auxiliary characters are missing from the font: Ō   |                              |
|   The following auxiliary characters are missing from the font: Ŗ   |                              |
|   The following auxiliary characters are missing from the font: ō   |                              |
|   The following auxiliary characters are missing from the font: ŗ   |                              |
| Auxiliary orthography codepoints:                                   | * fi_Latn (Finnish)          |
|   The following auxiliary characters are missing from the font: Ǧ   |                              |
|   The following auxiliary characters are missing from the font: Ǥ   |                              |
|   The following auxiliary characters are missing from the font: Ȟ   |                              |
|   The following auxiliary characters are missing from the font: Ǩ   |                              |
|   The following auxiliary characters are missing from the font: Ŋ   |                              |
|   The following auxiliary characters are missing from the font: Ŝ   |                              |
|   The following auxiliary characters are missing from the font: Ţ   |                              |
|   The following auxiliary characters are missing from the font: Ŧ   |                              |
|   The following auxiliary characters are missing from the font: Ʒ   |                              |
|   The following auxiliary characters are missing from the font: Ǯ   |                              |
|   The following auxiliary characters are missing from the font: ǧ   |                              |
|   The following auxiliary characters are missing from the font: ǥ   |                              |
|   The following auxiliary characters are missing from the font: ȟ   |                              |
|   The following auxiliary characters are missing from the font: ǩ   |                              |
|   The following auxiliary characters are missing from the font: ŋ   |                              |
|   The following auxiliary characters are missing from the font: ŝ   |                              |
|   The following auxiliary characters are missing from the font: ţ   |                              |
|   The following auxiliary characters are missing from the font: ŧ   |                              |
|   The following auxiliary characters are missing from the font: ʒ   |                              |
|   The following auxiliary characters are missing from the font: ǯ   |                              |
| Auxiliary orthography codepoints:                                   | * ro_Latn (Romanian)         |
|   The following auxiliary characters are missing from the font: Ţ   |                              |
|   The following auxiliary characters are missing from the font: ţ   |                              |
| Auxiliary orthography codepoints:                                   | * fr_Latn (French)           |
|   The following auxiliary characters are missing from the font: Ǔ   |                              |
|   The following auxiliary characters are missing from the font: ſ   |                              |
|   The following auxiliary characters are missing from the font: ǔ   |                              |
| Auxiliary orthography codepoints:                                   | * en_Latn (English)          |
|   The following auxiliary characters are missing from the font: Ĕ   |                              |
|   The following auxiliary characters are missing from the font: Ĭ   |                              |
|   The following auxiliary characters are missing from the font: Ŏ   |                              |
|   The following auxiliary characters are missing from the font: Ō   |                              |
|   The following auxiliary characters are missing from the font: Ŭ   |                              |
|   The following auxiliary characters are missing from the font: ĭ   |                              |
|   The following auxiliary characters are missing from the font: ŏ   |                              |
|   The following auxiliary characters are missing from the font: ō   |                              |
|   The following auxiliary characters are missing from the font: ŭ   |                              |
|   The following auxiliary characters are missing from the font: ʻ   |                              | [code: warning-language-shaping]



</div>
</details>





<details>
    <summary>🔥 <b>FAIL</b> Check font names are correct (googlefonts/font_names)</summary>
    <div>


> Google Fonts has several rules which need to be adhered to when setting a font's name table. Please read: https://googlefonts.github.io/gf-guide/statics.html#supported-styles https://googlefonts.github.io/gf-guide/statics.html#style-linking https://googlefonts.github.io/gf-guide/statics.html#unsupported-styles https://googlefonts.github.io/gf-guide/statics.html#single-weight-families




Original proposal: [https://github.com/fonttools/fontbakery/pull/3800]





- 🔥 **FAIL** Font names are incorrect:

| Name                       | Current       | Expected          |
|----------------------------|---------------|-------------------|
| Family Name                | Fluma         | Fluma             |
| Subfamily Name             | Regular       | Regular           |
| Full Name                  | **Fluma**     | **Fluma Regular** |
| Postscript Name            | Fluma-Regular | Fluma-Regular     |
| Typographic Family Name    | N/A           | N/A               |
| Typographic Subfamily Name | N/A           | N/A               | [code: bad-names]




- ⚠️ **WARN** Regular missing from full name [code: lacks-regular]



</div>
</details>





<details>
    <summary>🔥 <b>FAIL</b> Version format is correct in 'name' table? (googlefonts/name/version_format)</summary>
    <div>


> For Google Fonts, the version string must be in the format "Version X.Y". The version number must be greater than or equal to 1.000. (Additional information following the numeric version number is acceptable.) The "Version " prefix is a recommendation given by the OpenType spec.




Original proposal: [https://github.com/fonttools/fontbakery/issues/4829]





- 🔥 **FAIL** The NameID.VERSION_STRING (nameID=5) value must follow the pattern "Version X.Y" with X.Y greater than or equal to 1.000.

The "Version" prefix is a recommendation given by the OpenType spec.

Current version string is: "1.000" [code: bad-version-strings]




- 🔥 **FAIL** The NameID.VERSION_STRING (nameID=5) value must follow the pattern "Version X.Y" with X.Y greater than or equal to 1.000.

The "Version" prefix is a recommendation given by the OpenType spec.

Current version string is: "1.000" [code: bad-version-strings]




- 🔥 **FAIL** The NameID.VERSION_STRING (nameID=5) value must follow the pattern "Version X.Y" with X.Y greater than or equal to 1.000.

The "Version" prefix is a recommendation given by the OpenType spec.

Current version string is: "1.000" [code: bad-version-strings]



</div>
</details>





<details>
    <summary>🔥 <b>FAIL</b> Check font follows the Google Fonts vertical metric schema (googlefonts/vertical_metrics)</summary>
    <div>


> This check generally enforces Google Fonts’ vertical metrics specifications. In particular: * lineGap must be 0 * Sum of hhea ascender + abs(descender) + linegap must be   between 120% and 200% of UPM * Warning if sum is over 150% of UPM
>
> The threshold levels 150% (WARN) and 200% (FAIL) are somewhat arbitrarily chosen and may hint at a glaring mistake in the metrics calculations or UPM settings.
>
> Our documentation includes further information: https://github.com/googlefonts/gf-docs/tree/main/VerticalMetrics




Original proposal: [https://github.com/fonttools/fontbakery/pull/3762 and https://github.com/fonttools/fontbakery/pull/3921]





- 🔥 **FAIL** OS/2.sTypoLineGap is 58; it should be 0 [code: bad-OS/2.sTypoLineGap]




- 🔥 **FAIL** hhea.lineGap is 58; it should be 0 [code: bad-hhea.lineGap]




- 🔥 **FAIL** The sum of hhea.ascender + abs(hhea.descender) + hhea.lineGap is 2328 when it should be at least 2457 [code: bad-hhea-range]



</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Check that OS/2 fsSelection WWS bit is set correctly. (opentype/fsselection_wws)</summary>
    <div>


> According to the OpenType specification, OS/2.fsSelection bit 8 (WWS) should be set if the font has name table strings consistent with a weight/width/slope family without requiring use of name IDs 21 and 22.
>
> Conversely, if name IDs 21 and 22 are present (indicating the font names are not WWS-conformant), the WWS bit should not be set.




Original proposal: [https://github.com/fonttools/fontspector/issues/577]





- ⚠️ **WARN** OS/2 fsSelection WWS bit is not set, and the font does not have name IDs 21/22 (WWS Family/Subfamily). If the font's naming is WWS-conformant, the WWS bit should be set. [code: no-wws-without-wws-names]



</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Checking OS/2 fsSelection value. (opentype/xavgcharwidth)</summary>
    <div>


> The OS/2.xAvgCharWidth field is used to calculate the width of a string of characters. It is the average width of all non-zero width glyphs in the font.
>
> This check ensures that the value is correct. A failure here may indicate a bug in the font compiler, rather than something that the designer can do anything about.




Original proposal: [https://github.com/fonttools/fontbakery/issues/4829]





- ⚠️ **WARN** OS/2 xAvgCharWidth is 873 but it should be 975 which corresponds to the average of the widths of all glyphs in the font. This may indicate a problem with the font editor or the font compiler. [code: xAvgCharWidth-wrong]



</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Checking Vertical Metric linegaps. (linegaps)</summary>
    <div>


> The LineGap value is a space added to the line height created by the union of the (typo/hhea)Ascender and (typo/hhea)Descender. It is handled differently according to the environment.
>
> This leading value will be added above the text line in most desktop apps. It will be shared above and under in web browsers, and ignored in Windows if Use_Typo_Metrics is disabled.
>
> For better linespacing consistency across platforms, (typo/hhea)LineGap values must be 0.




Original proposal: [https://github.com/fonttools/fontbakery/issues/4133, https://googlefonts.github.io/gf-guide/metrics.html]





- ⚠️ **WARN** hhea lineGap is not equal to 0. [code: hhea]




- ⚠️ **WARN** OS/2 sTypoLineGap is not equal to 0. [code: OS/2]



</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Check math signs have the same width. (math_signs_width)</summary>
    <div>


> #,         It is a common practice to have math signs sharing the same width         (preferably the same width as tabular figures accross the entire font family).
>
> This probably comes from the will to avoid additional tabular math signs knowing that their design can easily share the same width.




Original proposal: [https://github.com/fonttools/fontbakery/issues/3832]





- ⚠️ **WARN** The most common width is 778 among a set of 9  math glyphs.
The following math glyphs have a different width, though:
width=702: uni003C
width=676: uni00AC
width=662: uni00F7
width=791: uni003D
width=701: uni003E [code: width-outliers]



</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Ensure indic fonts have the Indian Rupee Sign glyph. (rupee)</summary>
    <div>


> Per Bureau of Indian Standards every font supporting one of the official Indian languages needs to include Unicode Character “₹” (U+20B9) Indian Rupee Sign.




Original proposal: [https://github.com/fonttools/fontbakery/issues/2967]





- ⚠️ **WARN** Font is missing the Indian Rupee Sign glyph. Please add a glyph for Indian Rupee Sign (₹) at codepoint U+20B9. [code: missing-rupee]



</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Does the font contain a soft hyphen? (soft_hyphen)</summary>
    <div>


> The 'Soft Hyphen' character (codepoint 0x00AD) is used to mark a hyphenation possibility within a word in the absence of or overriding dictionary hyphenation.
>
> It is sometimes designed empty with no width (such as a control character), sometimes the same as the traditional hyphen, sometimes double encoded with the hyphen.
>
> That being said, it is recommended to not include it in the font at all, because discretionary hyphenation should be handled at the level of the shaping engine, not the font. Also, even if present, the software would not display that character.
>
> More discussion at: https://typedrawers.com/discussion/2046/special-dash-things-softhyphen-horizontalbar




Original proposal: [https://github.com/fonttools/fontbakery/issues/4046, https://github.com/fonttools/fontbakery/issues/3486]





- ⚠️ **WARN** This font has a 'Soft Hyphen' character. [code: softhyphen]



</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Check font contains no unreachable glyphs (unreachable_glyphs)</summary>
    <div>


> Glyphs are either accessible directly through Unicode codepoints or through        substitution rules.
>
> In Color Fonts, glyphs are also referenced by the COLR table. And mathematical fonts also reference glyphs via the MATH table.
>
> Any glyphs not accessible by these means are redundant and serve only to increase the font's file size.




Original proposal: [https://github.com/fonttools/fontbakery/issues/3160]





- ⚠️ **WARN** The following glyphs could not be reached by codepoint or substitution rules:

* comp_22
* comp_23 [code: unreachable-glyphs]



</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Glyph names are all valid? (valid_glyphnames)</summary>
    <div>


> Microsoft's recommendations for OpenType Fonts states the following:
>
> 'NOTE: The PostScript glyph name must be no longer than 31 characters, include only uppercase or lowercase English letters, European digits, the period or the underscore, i.e. from the set `[A-Za-z0-9_.]` and should start with a letter, except the special glyph name `.notdef` which starts with a period.'
>
> https://learn.microsoft.com/en-us/typography/opentype/otspec181/recom#-post--table
>
> In practice, though, particularly in modern environments, glyph names can be as long as 63 characters.
>
> According to the "Adobe Glyph List Specification" available at:
>
> https://github.com/adobe-type-tools/agl-specification
>
> Glyph names must also be unique, as duplicate glyph names prevent font installation on Mac OS X.




Original proposal: [https://github.com/fonttools/fontbakery/issues/2832]





- ⚠️ **WARN** Glyph 0x0020 is called uni0020; must be named 'space'. [code: not-recommended-0020]



</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Font has correct separator glyphs? (googlefonts/separator_glyphs)</summary>
    <div>


> U+2028 and U+2029 should be present; otherwise tofu is displayed. (whitespace_ink will check that they are empty)




Original proposal: [https://github.com/fonttools/fontspector/issues/93]





- ⚠️ **WARN** Missing separator glyph U+2028 [code: missing-separator-glyphs]




- ⚠️ **WARN** Missing separator glyph U+2029 [code: missing-separator-glyphs]



</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Ensure soft_dotted characters lose their dot when combined with marks that
replace the dot. (soft_dotted)</summary>
    <div>


> An accent placed on characters with a "soft dot", like i or j, causes the dot to disappear. An explicit dot above can be added where required. See "Diacritics on i and j" in Section 7.1, "Latin" in The Unicode Standard.
>
> Characters with the Soft_Dotted property are listed in https://www.unicode.org/Public/UCD/latest/ucd/PropList.txt
>
> See also: https://googlefonts.github.io/gf-guide/diacritics.html#soft-dotted-glyphs




Original proposal: [https://github.com/fonttools/fontbakery/issues/4059]





- ⚠️ **WARN** The dot of soft dotted characters used in orthographies _must_ disappear in the following strings:

* j́
* j̀
* j̃
* j̄
* j̈
* i̋
* i̊
* į̌
* į́
... and 4 othersThe dot of soft dotted characters _should_ disappear in other cases, for example:

* ǰ
* j̋
* j̆
* ĵ
* j̇
* j̊
* ǐ
* ĭ
* ĩ
... and 6 others [code: soft-dotted]



</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Do any segments have colinear vectors? (outline_colinear_vectors)</summary>
    <div>


> This check looks for consecutive line segments which have the same angle. This normally happens if an outline point has been added by accident.
>
> This check is not run for variable fonts, as they may legitimately have colinear vectors.




Original proposal: [https://github.com/fonttools/fontbakery/pull/3088]





- ⚠️ **WARN** The following glyphs have colinear vectors:

* uni0023 (U+0023): from (630.0, 580.0) to (630.0, 580.0) is colinear with segment from (630.0, 580.0) to (630.0, 580.0)
* uni0024 (U+0024): from (489.0, 311.0) to (490.0, 311.0) is colinear with segment from (490.0, 311.0) to (490.0, 311.0)
* uni0030 (U+0030): from (673.0, 231.0) to (674.0, 231.0) is colinear with segment from (674.0, 231.0) to (674.0, 231.0)
* uni0034 (U+0034): from (866.0, 611.0) to (867.0, 611.0) is colinear with segment from (867.0, 611.0) to (867.0, 611.0)
* uni0045 (U+0045): from (395.0, 167.0) to (396.0, 167.0) is colinear with segment from (396.0, 167.0) to (396.0, 167.0)
* uni0056 (U+0056): from (994.0, 1458.0) to (995.0, 1458.0) is colinear with segment from (995.0, 1458.0) to (995.0, 1458.0)
* uni005B (U+005B): from (343.0, 197.0) to (345.0, 197.0) is colinear with segment from (345.0, 197.0) to (345.0, 197.0)
* uni0061 (U+0061): from (391.0, 608.0) to (391.0, 608.0) is colinear with segment from (391.0, 608.0) to (391.0, 608.0)
* uni0077 (U+0077): from (851.0, 965.0) to (852.0, 965.0) is colinear with segment from (852.0, 965.0) to (852.0, 965.0)
... and 39 others [code: found-colinear-vectors]



</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Check the direction of the outermost contour in each glyph (outline_direction)</summary>
    <div>


> In TrueType fonts, the outermost contour of a glyph should be oriented clockwise, while the inner contours should be oriented counter-clockwise. Getting the path direction wrong can lead to rendering issues in some software.




Original proposal: [https://github.com/fonttools/fontbakery/issues/2056]





- ⚠️ **WARN** The following glyphs have a counter-clockwise outer contour:

* uni0041 (U+0041) has a counter-clockwise outer contour
* uni006A (U+006A) has a counter-clockwise outer contour
* uni006A (U+006A) has a counter-clockwise outer contour
* uni00AC (U+00AC) has a counter-clockwise outer contour
* uni00C0 (U+00C0) has a counter-clockwise outer contour
* uni00C0 (U+00C0) has a counter-clockwise outer contour
* uni00C1 (U+00C1) has a counter-clockwise outer contour
* uni00C2 (U+00C2) has a counter-clockwise outer contour
* uni00C3 (U+00C3) has a counter-clockwise outer contour
... and 62 others [code: ccw-outer-contour]



</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Check there are no overlapping path segments (overlapping_path_segments)</summary>
    <div>


> Some rasterizers encounter difficulties when rendering glyphs with overlapping path segments.
>
> A path segment is a section of a path defined by two on-curve points. When two segments share the same coordinates, they are considered overlapping.




Original proposal: [https://github.com/google/fonts/issues/7594#issuecomment-2401909084]





- ⚠️ **WARN** The following glyphs have overlapping path segments:

* uni0023 (U+0023): Line(Line { p0: (630.0, 580.0), p1: (630.0, 580.0) }) has the same coordinates as a previous segment.
* uni0061 (U+0061): Line(Line { p0: (391.0, 608.0), p1: (391.0, 608.0) }) has the same coordinates as a previous segment.
* uni00AA (U+00AA): Line(Line { p0: (231.0, 1045.0), p1: (231.0, 1045.0) }) has the same coordinates as a previous segment.
* uni00AC (U+00AC): Line(Line { p0: (611.0, 912.0), p1: (611.0, 912.0) }) has the same coordinates as a previous segment.
* uni00B2 (U+00B2): Line(Line { p0: (434.0, 991.0), p1: (434.0, 991.0) }) has the same coordinates as a previous segment.
* uni00B6 (U+00B6): Line(Line { p0: (664.0, 824.0), p1: (664.0, 824.0) }) has the same coordinates as a previous segment.
* uni00BC (U+00BC): Line(Line { p0: (951.0, 316.0), p1: (951.0, 316.0) }) has the same coordinates as a previous segment.
* uni00BC (U+00BC): Line(Line { p0: (157.0, 517.0), p1: (157.0, 517.0) }) has the same coordinates as a previous segment.
* uni00BC (U+00BC): Line(Line { p0: (401.0, 209.0), p1: (401.0, 209.0) }) has the same coordinates as a previous segment.
... and 15 others [code: overlapping-path-segments]



</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Is the Grid-fitting and Scan-conversion Procedure ('gasp') table
set to optimize rendering? (googlefonts/gasp)</summary>
    <div>


> Traditionally version 0 'gasp' tables were set so that font sizes below 8 ppem had no grid fitting but did have antialiasing. From 9-16 ppem, just grid fitting. And fonts above 17ppem had both antialiasing and grid fitting toggled on. The use of accelerated graphics cards and higher resolution screens make this approach obsolete. Microsoft's DirectWrite pushed this even further with much improved rendering built into the OS and apps.
>
> In this scenario it makes sense to simply toggle all 4 flags ON for all font sizes.




Original proposal: [https://github.com/fonttools/fontbakery/issues/4829]







- ⚠️ **WARN** The gasp range 0xFFFF value 0x0A should be set to 0x0F [code: unset-flags]



</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Ensure fonts have ScriptLangTags declared on the 'meta' table. (googlefonts/meta/script_lang_tags)</summary>
    <div>


> The OpenType 'meta' table originated at Apple. Microsoft added it to OT with just two DataMap records:
>
> - dlng: comma-separated ScriptLangTags that indicate which scripts,   or languages and scripts, with possible variants, the font is designed for.
>
> - slng: comma-separated ScriptLangTags that indicate which scripts,   or languages and scripts, with possible variants, the font supports.
>
> The slng structure is intended to describe which languages and scripts the font overall supports. For example, a Traditional Chinese font that also contains Latin characters, can indicate Hant,Latn, showing that it supports Hant, the Traditional Chinese variant of the Hani script, and it also supports the Latn script.
>
> The dlng structure is far more interesting. A font may contain various glyphs, but only a particular subset of the glyphs may be truly "leading" in the design, while other glyphs may have been included for technical reasons. Such a Traditional Chinese font could only list Hant there, showing that it’s designed for Traditional Chinese, but the font would omit Latn, because the developers don’t think the font is really recommended for purely Latin-script use.
>
> The tags used in the structures can comprise just script, or also language and script. For example, if a font has Bulgarian Cyrillic alternates in the locl feature for the cyrl BGR OT languagesystem, it could also indicate in dlng explicitly that it supports bul-Cyrl. (Note that the scripts and languages in meta use the ISO language and script codes, not the OpenType ones).
>
> This check ensures that the font has the meta table containing the slng and dlng structures.
>
> All families in the Google Fonts collection should contain the 'meta' table. Windows 10 already uses it when deciding on which fonts to fall back to. The Google Fonts API and also other environments could use the data for smarter filtering. Most importantly, those entries should be added to the Noto fonts.
>
> In the font making process, some environments store this data in external files already. But the meta table provides a convenient way to store this inside the font file, so some tools may add the data, and unrelated tools may read this data. This makes the solution much more portable and universal.




Original proposal: [https://github.com/fonttools/fontbakery/issues/3349]





- ⚠️ **WARN** This font file does not have a 'meta' table. [code: lacks-meta-table]



</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Checking OS/2 achVendID. (googlefonts/vendor_id)</summary>
    <div>


> Microsoft keeps a list of font vendors and their respective contact info. This list is updated regularly and is indexed by a 4-char "Vendor ID" which is stored in the achVendID field of the OS/2 table.
>
> Registering your ID is not mandatory, but it is a good practice since some applications may display the type designer / type foundry contact info on some dialog and also because that info will be visible on Microsoft's website:
>
> https://docs.microsoft.com/en-us/typography/vendors/
>
> This check verifies whether or not a given font's vendor ID is registered in that list or if it has some of the default values used by the most common font editors.
>
> Each new FontBakery release includes a cached copy of that list of vendor IDs. If you registered recently, you're safe to ignore warnings emitted by this check, since your ID will soon be included in one of our upcoming releases.




Original proposal: [https://github.com/fonttools/fontbakery/issues/3943, https://github.com/fonttools/fontbakery/issues/4829]





- ⚠️ **WARN** OS/2 VendorID value 'XXXX' is not yet recognized.
If you registered it recently, then it's safe to ignore this warning message. Otherwise, you should set it to your own unique 4 character code, and register it with Microsoft at https://www.microsoft.com/typography/links/vendorlist.aspx
 [code: unknown]



</div>
</details>


</div>
</details>


<details><summary>[3] /private/tmp/fluma-font-qa/fluma</summary>
<div>


<details>
    <summary>🔥 <b>FAIL</b> Copyright notices match canonical pattern in fonts (googlefonts/font_copyright)</summary>
    <div>


> This check aims at ensuring a uniform and legally accurate copyright statement on the name table entries and METADATA.pb files of font files across the Google Fonts library.
>
> We also check that the copyright field in METADATA.pb matches the contents of the name table nameID 0 (Copyright), and that the copyright notice within the METADATA.pb file is not too long; if it is more than 500 characters, this may be an indication that either a full license or the font's description has been included in this field by mistake.
>
> The expected pattern for the copyright string adheres to the following rules:
>
> * It must say "Copyright" followed by a 4 digit year (optionally followed by   a hyphen and another 4 digit year)
>
> * Additional years or year ranges are also valid.
>
> * An optional comma can be placed here.
>
> * Then it must say "The <familyname> Project Authors" and, within parentheses,   a URL for a git repository must be provided. But we have an exception   for the fonts from the Noto project, that simply have   "google llc. all rights reserved" here.
>
> * The check is case insensitive and does not validate whether the familyname   is correct, even though we'd obviously expect it to be.
>
> Here is an example of a valid copyright string:
>
> "Copyright 2017 The Archivo Black Project Authors  (https://github.com/Omnibus-Type/ArchivoBlack)"




Original proposal: [https://github.com/fonttools/fontbakery/pull/2383, https://github.com/fonttools/fontbakery/issues/4829]





- 🔥 **FAIL** Fluma-Regular.ttf: Name Table entry: Copyright notices should match a pattern similar to:

"Copyright 2020 The Familyname Project Authors (git url)"

But instead we have got:

" " [code: bad-notice-format]




- 🔥 **FAIL** Fluma-Regular.ttf: Name Table entry: Copyright notices should match a pattern similar to:

"Copyright 2020 The Familyname Project Authors (git url)"

But instead we have got:

" " [code: bad-notice-format]




- 🔥 **FAIL** Fluma-Regular.ttf: Name Table entry: Copyright notices should match a pattern similar to:

"Copyright 2020 The Familyname Project Authors (git url)"

But instead we have got:

" " [code: bad-notice-format]



</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Ensure Fonts have 'ital' STAT axis. (opentype/STAT/ital_axis)</summary>
    <div>


> Check that related Upright and Italic have an 'ital' axis in the STAT table.
>
> Since the STAT table can be used to create new instances, it is important to ensure that such an 'ital' axis be the last one declared in the STAT table so that the eventual naming of new instances follows the subfamily traditional scheme (RIBBI / WWS) where "Italic" is always last.
>
> The 'ital' axis should also be strictly boolean, only accepting values of 0 (for Uprights) or 1 (for Italics). This usually works as a mechanism for selecting between two linked variable font files.
>
> Also, the axis value name for uprights must be set as elidable.




Original proposal: [https://github.com/fonttools/fontbakery/issues/2934, https://github.com/fonttools/fontbakery/issues/3668, https://github.com/fonttools/fontbakery/issues/3669]





- ⚠️ **WARN** Static font is missing the 'STAT' table. [code: no-stat-table]



</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Check for codepoints not covered by METADATA subsets. (googlefonts/metadata/unreachable_subsetting)</summary>
    <div>


> This check ensures that all encoded glyphs in the font are covered by a subset declared in the METADATA.pb. Google Fonts splits the font into a set of subset fonts based on the contents of the `subsets` field and the subset definitions in the `glyphsets` repository.
>
> Any encoded glyphs which are not by any of these subset definitions will not be served in the subsetted fonts, and so will be unreachable to the end user.




Original proposal: [https://github.com/fonttools/fontbakery/issues/4097 and https://github.com/fonttools/fontbakery/pull/4273]





- ⚠️ **WARN** /private/tmp/fluma-font-qa/fluma/Fluma-Regular.ttf: The following codepoints supported by the font are not covered by any subsets defined in the font's metadata file, and will never be served. You can solve this by either manually adding additional subset declarations to METADATA.pb, or by editing the glyphset definitions.

* U+02D8 BREVE: try adding one of: yi, canadian-aboriginal
* U+02D9 DOT ABOVE: try adding one of: canadian-aboriginal, yi
* U+02DB OGONEK: try adding one of: yi, canadian-aboriginal
* U+0302 COMBINING CIRCUMFLEX ACCENT: try adding one of: cherokee, math, tifinagh, coptic
* U+0306 COMBINING BREVE: try adding one of: old-permic, tifinagh
* U+0307 COMBINING DOT ABOVE: try adding one of: malayalam, math, old-permic, tai-le, syriac, canadian-aboriginal, coptic, tifinagh, duployan, hebrew, todhri
* U+030A COMBINING RING ABOVE: try adding one of: duployan, syriac
* U+030B COMBINING DOUBLE ACUTE ACCENT: try adding one of: osage, cherokee
* U+030C COMBINING CARON: try adding one of: tai-le, cherokee
... and 2 others

Or you can add the above codepoints to one of the subsets supported by the font: latin-ext, latin [code: unreachable-subsetting]



</div>
</details>


</div>
</details>






### Summary

| 🔥 FAIL | ⚠️ WARN | ℹ️ INFO | ✅ PASS | ⏩ SKIP |
| ---|---|---|---|---|
| 71 | 23 | 6 | 83 | 90 |
| 26% | 8% | 2% | 30% | 33% |
