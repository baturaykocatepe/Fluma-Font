## FontSpector report

fontspector version: 1.8.0






## Check results




<details><summary>[8] /private/tmp/fluma-font-qa/final/fluma/Fluma-Regular.ttf</summary>
<div>


<details>
    <summary>⚠️ <b>WARN</b> Check accent of Lcaron, dcaron, lcaron, tcaron (alt_caron)</summary>
    <div>


> Lcaron, dcaron, lcaron, tcaron should NOT be composed with quoteright or quotesingle or comma or caron(comb). It should be composed with a distinctive glyph which doesn't look like an apostrophe.
>
> Source: https://ilovetypography.com/2009/01/24/on-diacritics/ http://diacritics.typo.cz/index.php?id=5 https://www.typotheque.com/articles/lcaron




Original proposal: [https://github.com/fonttools/fontbakery/issues/3308]





- ⚠️ **WARN** Lcaron is decomposed and therefore could not be checked. Please check manually. [code: decomposed-outline]




- ⚠️ **WARN** dcaron is decomposed and therefore could not be checked. Please check manually. [code: decomposed-outline]




- ⚠️ **WARN** lcaron is decomposed and therefore could not be checked. Please check manually. [code: decomposed-outline]




- ⚠️ **WARN** tcaron is decomposed and therefore could not be checked. Please check manually. [code: decomposed-outline]



</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Check if each glyph has the recommended amount of contours. (contour_count)</summary>
    <div>


> Visually QAing thousands of glyphs by hand is tiring. Most glyphs can only be constructured in a handful of ways. This means a glyph's contour count will only differ slightly amongst different fonts, e.g a 'g' could either be 2 or 3 contours, depending on whether its double story or single story.
>
> However, a quotedbl should have 2 contours, unless the font belongs to a display family.
>
> This check currently does not cover variable fonts because there's plenty of alternative ways of constructing glyphs with multiple outlines for each feature in a VarFont. The expected contour count data for this check is currently optimized for the typical construction of glyphs in static fonts.




Original proposal: [https://github.com/fonttools/fontbakery/issues/4829]





- ⚠️ **WARN** This check inspects the glyph outlines and detects the total number of contours in each of them. The expected values are
     inferred from the typical amounts of contours observed in a
     large collection of reference font families. The divergences
     listed below may simply indicate a significantly different
     design on some of your glyphs. On the other hand, some of these
     may flag actual bugs in the font such as glyphs mapped to an
     incorrect codepoint. Please consider reviewing the design and
     codepoint assignment of these to make sure they are correct.


    The following glyphs do not have the recommended number of contours:
* idieresis (U+00EF): found 2, expected one of: [3, 4, 7]
* imacron (U+012B): found 3, expected one of: [2, 6]
* lacute (U+013A): found 1, expected one of: [2, 3, 6]
* dieresis (U+00A8): found 1, expected one of: [2]
* hungarumlaut (U+02DD): found 1, expected one of: [2]
* uni0308 (U+0308): found 1, expected one of: [2]
* uni030B (U+030B): found 1, expected one of: [2] [code: contour-count]



</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Check math signs have the same width. (math_signs_width)</summary>
    <div>


> #,         It is a common practice to have math signs sharing the same width         (preferably the same width as tabular figures accross the entire font family).
>
> This probably comes from the will to avoid additional tabular math signs knowing that their design can easily share the same width.




Original proposal: [https://github.com/fonttools/fontbakery/issues/3832]





- ⚠️ **WARN** The most common width is 779 among a set of 9  math glyphs.
The following math glyphs have a different width, though:
width=702: greater
width=677: logicalnot
width=792: equal
width=703: less
width=662: divide [code: width-outliers]



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
    <summary>⚠️ <b>WARN</b> Shapes languages in all GF glyphsets. (googlefonts/glyphsets/shape_languages)</summary>
    <div>


> This check uses a heuristic to determine which GF glyphsets a font supports. Then it checks the font for correct shaping behaviour for all languages in those glyphsets.




Original proposal: [https://github.com/googlefonts/fontbakery/issues/4147]





- ⚠️ **WARN** Warning language shaping:

| Message                                                                  | Languages                    |
|--------------------------------------------------------------------------|------------------------------|
| Auxiliary orthography codepoints:                                        | * ca_Latn (Catalan)          |
|   The following auxiliary characters are missing from the font: Ĭ        |                              |
|   The following auxiliary characters are missing from the font: Ŀ        |                              |
|   The following auxiliary characters are missing from the font: Ŏ        |                              |
|   The following auxiliary characters are missing from the font: Ō        |                              |
|   The following auxiliary characters are missing from the font: Ŭ        |                              |
|   The following auxiliary characters are missing from the font: ĭ        |                              |
|   The following auxiliary characters are missing from the font: ŀ        |                              |
|   The following auxiliary characters are missing from the font: ŏ        |                              |
|   The following auxiliary characters are missing from the font: ō        |                              |
|   The following auxiliary characters are missing from the font: ŭ        |                              |
| Auxiliary orthography codepoints:                                        | * ro_Latn (Romanian)         |
|   The following auxiliary characters are missing from the font: Ţ        |                              |
|   The following auxiliary characters are missing from the font: ţ        |                              |
| Auxiliary orthography codepoints:                                        | * lt_Latn (Lithuanian)       |
|   The following auxiliary characters are missing from the font: Ẽ        |                              |
|   The following auxiliary characters are missing from the font: Ĩ        |                              |
|   The following auxiliary characters are missing from the font: Ũ        |                              |
|   The following auxiliary characters are missing from the font: ẽ        |                              |
|   The following auxiliary characters are missing from the font: ĩ        |                              |
|   The following auxiliary characters are missing from the font: ũ        |                              |
|   Shaper didn't attach acutecomb to Aogonek when shaping the text 'Ą́'    |                              |
|   Shaper didn't attach tildecomb to Aogonek when shaping the text 'Ą̃'    |                              |
|   Shaper didn't attach acutecomb to Eogonek when shaping the text 'Ę́'    |                              |
|   Shaper didn't attach tildecomb to Eogonek when shaping the text 'Ę̃'    |                              |
|   Shaper didn't attach acutecomb to Edotaccent when shaping the text 'Ė́' |                              |
|   Shaper didn't attach tildecomb to Edotaccent when shaping the text 'Ė̃' |                              |
|   Shaper didn't attach acutecomb to Idotaccent when shaping the text 'İ́' |                              |
|   Shaper didn't attach acutecomb to Idotaccent when shaping the text 'İ́' |                              |
|   Shaper didn't attach gravecomb to Idotaccent when shaping the text 'İ̀' |                              |
|   Shaper didn't attach gravecomb to Idotaccent when shaping the text 'İ̀' |                              |
|   Shaper didn't attach tildecomb to Idotaccent when shaping the text 'İ̃' |                              |
|   Shaper didn't attach tildecomb to Idotaccent when shaping the text 'İ̃' |                              |
|   Shaper didn't attach acutecomb to Iogonek when shaping the text 'Į́'    |                              |
|   Shaper didn't attach uni0307 to Iogonek when shaping the text 'Į̇́'      |                              |
|   Shaper didn't attach acutecomb to uni0307 when shaping the text 'Į̇́'    |                              |
|   Shaper didn't attach tildecomb to Iogonek when shaping the text 'Į̃'    |                              |
|   Shaper didn't attach uni0307 to Iogonek when shaping the text 'Į̇̃'      |                              |
|   Shaper didn't attach tildecomb to uni0307 when shaping the text 'Į̇̃'    |                              |
|   Shaper didn't attach acutecomb to Uogonek when shaping the text 'Ų́'    |                              |
|   Shaper didn't attach tildecomb to Uogonek when shaping the text 'Ų̃'    |                              |
|   Shaper didn't attach acutecomb to Umacron when shaping the text 'Ū́'    |                              |
|   Shaper didn't attach tildecomb to Umacron when shaping the text 'Ū̃'    |                              |
|   Shaper didn't attach acutecomb to aogonek when shaping the text 'ą́'    |                              |
|   Shaper didn't attach tildecomb to aogonek when shaping the text 'ą̃'    |                              |
|   Shaper didn't attach acutecomb to eogonek when shaping the text 'ę́'    |                              |
|   Shaper didn't attach tildecomb to eogonek when shaping the text 'ę̃'    |                              |
|   Shaper didn't attach acutecomb to edotaccent when shaping the text 'ė́' |                              |
|   Shaper didn't attach tildecomb to edotaccent when shaping the text 'ė̃' |                              |
|   Shaper didn't attach acutecomb to uogonek when shaping the text 'ų́'    |                              |
|   Shaper didn't attach tildecomb to uogonek when shaping the text 'ų̃'    |                              |
|   Shaper didn't attach acutecomb to umacron when shaping the text 'ū́'    |                              |
|   Shaper didn't attach tildecomb to umacron when shaping the text 'ū̃'    |                              |
| Auxiliary orthography codepoints:                                        | * fi_Latn (Finnish)          |
|   The following auxiliary characters are missing from the font: Ǧ        |                              |
|   The following auxiliary characters are missing from the font: Ǥ        |                              |
|   The following auxiliary characters are missing from the font: Ȟ        |                              |
|   The following auxiliary characters are missing from the font: Ǩ        |                              |
|   The following auxiliary characters are missing from the font: Ŋ        |                              |
|   The following auxiliary characters are missing from the font: Ŝ        |                              |
|   The following auxiliary characters are missing from the font: Ţ        |                              |
|   The following auxiliary characters are missing from the font: Ŧ        |                              |
|   The following auxiliary characters are missing from the font: Ʒ        |                              |
|   The following auxiliary characters are missing from the font: Ǯ        |                              |
|   The following auxiliary characters are missing from the font: ǧ        |                              |
|   The following auxiliary characters are missing from the font: ǥ        |                              |
|   The following auxiliary characters are missing from the font: ȟ        |                              |
|   The following auxiliary characters are missing from the font: ǩ        |                              |
|   The following auxiliary characters are missing from the font: ŋ        |                              |
|   The following auxiliary characters are missing from the font: ŝ        |                              |
|   The following auxiliary characters are missing from the font: ţ        |                              |
|   The following auxiliary characters are missing from the font: ŧ        |                              |
|   The following auxiliary characters are missing from the font: ʒ        |                              |
|   The following auxiliary characters are missing from the font: ǯ        |                              |
| Auxiliary orthography codepoints:                                        | * nb_Latn (Norwegian Bokmål) |
|   The following auxiliary characters are missing from the font: Ǎ        |                              |
|   The following auxiliary characters are missing from the font: Ŋ        |                              |
|   The following auxiliary characters are missing from the font: Ŧ        |                              |
|   The following auxiliary characters are missing from the font: ǎ        |                              |
|   The following auxiliary characters are missing from the font: ŋ        |                              |
|   The following auxiliary characters are missing from the font: ŧ        |                              |
| Auxiliary orthography codepoints:                                        | * lv_Latn (Latvian)          |
|   The following auxiliary characters are missing from the font: Ō        |                              |
|   The following auxiliary characters are missing from the font: Ŗ        |                              |
|   The following auxiliary characters are missing from the font: ō        |                              |
|   The following auxiliary characters are missing from the font: ŗ        |                              |
| Auxiliary orthography codepoints:                                        | * en_Latn (English)          |
|   The following auxiliary characters are missing from the font: Ĭ        |                              |
|   The following auxiliary characters are missing from the font: Ŏ        |                              |
|   The following auxiliary characters are missing from the font: Ō        |                              |
|   The following auxiliary characters are missing from the font: Ŭ        |                              |
|   The following auxiliary characters are missing from the font: ĭ        |                              |
|   The following auxiliary characters are missing from the font: ŏ        |                              |
|   The following auxiliary characters are missing from the font: ō        |                              |
|   The following auxiliary characters are missing from the font: ŭ        |                              |
|   The following auxiliary characters are missing from the font: ʻ        |                              |
| Auxiliary orthography codepoints:                                        | * cs_Latn (Czech)            |
|   The following auxiliary characters are missing from the font: Ĭ        | * cy_Latn (Welsh)            |
|   The following auxiliary characters are missing from the font: Ŏ        | * es_Latn (Spanish)          |
|   The following auxiliary characters are missing from the font: Ō        | * hu_Latn (Hungarian)        |
|   The following auxiliary characters are missing from the font: Ŭ        | * pt_Latn (Portuguese)       |
|   The following auxiliary characters are missing from the font: ĭ        | * sk_Latn (Slovak)           |
|   The following auxiliary characters are missing from the font: ŏ        | * tr_Latn (Turkish)          |
|   The following auxiliary characters are missing from the font: ō        |                              |
|   The following auxiliary characters are missing from the font: ŭ        |                              |
| Auxiliary orthography codepoints:                                        | * de_Latn (German)           |
|   The following auxiliary characters are missing from the font: Ĭ        |                              |
|   The following auxiliary characters are missing from the font: Ŏ        |                              |
|   The following auxiliary characters are missing from the font: Ō        |                              |
|   The following auxiliary characters are missing from the font: Ŭ        |                              |
|   The following auxiliary characters are missing from the font: ĭ        |                              |
|   The following auxiliary characters are missing from the font: ŏ        |                              |
|   The following auxiliary characters are missing from the font: ō        |                              |
|   The following auxiliary characters are missing from the font: ſ        |                              |
|   The following auxiliary characters are missing from the font: ŭ        |                              |
| Auxiliary orthography codepoints:                                        | * da_Latn (Danish)           |
|   The following auxiliary characters are missing from the font: Ǿ        |                              |
|   The following auxiliary characters are missing from the font: ǿ        |                              |
| Auxiliary orthography codepoints:                                        | * fr_Latn (French)           |
|   The following auxiliary characters are missing from the font: Ǔ        |                              |
|   The following auxiliary characters are missing from the font: ſ        |                              |
|   The following auxiliary characters are missing from the font: ǔ        |                              | [code: warning-language-shaping]



</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Do outlines contain any jaggy segments? (outline_jaggy_segments)</summary>
    <div>


> This check heuristically detects outline segments which form a particularly small angle, indicative of an outline error. This may cause false positives in cases such as extreme ink traps, so should be regarded as advisory and backed up by manual inspection.




Original proposal: [https://github.com/fonttools/fontbakery/issues/3064]





- ⚠️ **WARN** The following glyphs have jaggy segments:

* hungarumlaut (U+02DD): Line(Line { p0: (131.0, 1180.0), p1: (130.0, 1173.0) })/Quad(QuadBez { p0: (130.0, 1173.0), p1: (145.0, 1219.0), p2: (163.0, 1233.5) }) = 9.93036958204319 degrees
* uni030B (U+030B): Line(Line { p0: (-25.0, 1180.0), p1: (-26.0, 1173.0) })/Quad(QuadBez { p0: (-26.0, 1173.0), p1: (-11.0, 1219.0), p2: (7.0, 1233.5) }) = 9.93036958204319 degrees [code: found-jaggy-segments]



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





- ⚠️ **WARN** OS/2 VendorID value 'NONE' is not yet recognized.
If you registered it recently, then it's safe to ignore this warning message. Otherwise, you should set it to your own unique 4 character code, and register it with Microsoft at https://www.microsoft.com/typography/links/vendorlist.aspx
 [code: unknown]



</div>
</details>


</div>
</details>


<details><summary>[1] /private/tmp/fluma-font-qa/final/fluma</summary>
<div>


<details>
    <summary>⚠️ <b>WARN</b> Check for codepoints not covered by METADATA subsets. (googlefonts/metadata/unreachable_subsetting)</summary>
    <div>


> This check ensures that all encoded glyphs in the font are covered by a subset declared in the METADATA.pb. Google Fonts splits the font into a set of subset fonts based on the contents of the `subsets` field and the subset definitions in the `glyphsets` repository.
>
> Any encoded glyphs which are not by any of these subset definitions will not be served in the subsetted fonts, and so will be unreachable to the end user.




Original proposal: [https://github.com/fonttools/fontbakery/issues/4097 and https://github.com/fonttools/fontbakery/pull/4273]





- ⚠️ **WARN** /private/tmp/fluma-font-qa/final/fluma/Fluma-Regular.ttf: The following codepoints supported by the font are not covered by any subsets defined in the font's metadata file, and will never be served. You can solve this by either manually adding additional subset declarations to METADATA.pb, or by editing the glyphset definitions.

* U+02D8 BREVE: try adding one of: canadian-aboriginal, yi
* U+02D9 DOT ABOVE: try adding one of: yi, canadian-aboriginal
* U+02DB OGONEK: try adding one of: canadian-aboriginal, yi
* U+0302 COMBINING CIRCUMFLEX ACCENT: try adding one of: math, cherokee, tifinagh, coptic
* U+0306 COMBINING BREVE: try adding one of: tifinagh, old-permic
* U+0307 COMBINING DOT ABOVE: try adding one of: todhri, hebrew, math, tai-le, duployan, syriac, canadian-aboriginal, old-permic, malayalam, coptic, tifinagh
* U+030A COMBINING RING ABOVE: try adding one of: syriac, duployan
* U+030B COMBINING DOUBLE ACUTE ACCENT: try adding one of: osage, cherokee
* U+030C COMBINING CARON: try adding one of: tai-le, cherokee
... and 3 others

Or you can add the above codepoints to one of the subsets supported by the font: latin-ext, latin [code: unreachable-subsetting]



</div>
</details>


</div>
</details>






### Summary

| ⚠️ WARN | ℹ️ INFO | ✅ PASS | ⏩ SKIP |
| ---|---|---|---|
| 12 | 8 | 107 | 81 |
| 6% | 4% | 51% | 39% |
