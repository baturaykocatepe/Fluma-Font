# FlumaFont teknik denetim, 2026-09-30

## Kapsam ve yöntem

Bu kayıt `sources/Fluma.gs2`, yerel `GF_Latin_Core.nam`, mevcut TTF/OTF exportları ve paket metadata'sının salt okunur denetimidir. `tools/audit_font.py` fontTools 4.60.2 ile çalıştırıldı. TTF ayrıca resmi Fontspector 1.8.0'ın `googlefonts` profiliyle test edildi. Fontspector, aile adı klasörünü doğru okuması için TTF'nin birebir kopyası üzerinde geçici `/private/tmp/fluma-font-qa/fluma/` yolunda çalıştırıldı. Ham sonuç: [Fontspector raporu](qa/fontspector-2026-09-30.md).

TTF/OTF ve `.gs2` değiştirilmedi. Specimen görselleri ve Figma dosyası açılmadı veya düzenlenmedi. Bu denetim görsel glyph kalitesi ya da Google Fonts kabulü anlamına gelmez.

## Doğrulanmış sonuçlar

| Kontrol | Sonuç |
|---|---|
| Yerel GF Latin Core `.nam` | 319 benzersiz encoded codepoint |
| TTF ve OTF `cmap` | Her birinde 334 mapped codepoint; yerel 319 listenin tamamı mevcut |
| Core glyph outline | Space ve non-breaking space dışında boş outline saptanmadı |
| Ekstra mapped glyph | U+0115 `ĕ` hem kaynakta hem exportlarda boş ve sıfır advance width; U+00AD soft hyphen da boş |
| TTF/OTF name tablosu | Copyright (ID 0), license description (ID 13), license URL (ID 14) boşluk karakterinden ibaret; `OFL.txt` başlığı ile eşleşmiyor |
| Kaynak metadata | `copyright`, `license`, `licenseURL` alanları boş |
| Dikey metrik | Kaynak cap height 1480, x-height 1000; export OS/2 cap height 1602, x-height 1002. Farkın nedeni henüz doğrulanmadı |
| Yerel kopyalar | `markdown/fluma/` TTF ve OTF dosyaları font paketindeki karşılıklarıyla SHA-256 düzeyinde aynı |

`cmap` kapsamı glyph'lerin doğru şekillendiği veya tüm dil dizilerinin çalıştığı anlamına gelmez.

## Fontspector, TTF

203 kontrol: **83 PASS, 23 WARN, 71 FAIL, 90 SKIP, 6 INFO, 0 ERROR/FATAL**. 71 FAIL tekil çıktıdır; aşağıdaki yaklaşık 10 kontrol ailesinde gruplanır. Test dosyası geçici `fluma/` klasörüne konarak `dirname_matches_nameid_1` kaynaklı yapay hata giderildi. Başvuru profili bu durumda geçmiyor.

| Öncelik | FAIL ailesi | Bulgular ve gerekli iş |
|---|---|---|
| P0 | `opentype/name/empty_records`, `name/trailing_spaces`, `googlefonts/font_copyright` | Boş name kayıtlarını kaldır veya gerçek değerlerle doldur. Copyright ID 0, `OFL.txt` ilk satırıyla birebir eşleşmeli. Kaynak metadata ve iki export birlikte ele alınmalı. |
| P0 | `base_has_width`, `case_mapping`, `contour_count` | U+0115 `ĕ` boş/sıfır genişlikte; U+0114 `Ĕ` yok. Gerçek glyph çifti çizilip test edilmeli veya yanlışlıkla eklenmiş boş U+0115 haritalaması kaynakta düzeltilmeli. Karakter tasarım kararı ve yeni export gerekir. |
| P0 | `googlefonts/glyphsets/shape_languages` | Dutch `ÍJ́` ve `íj́` dizilerinde combining acute, J/j üzerine bağlanmıyor. GPOS mark attachment veya eşdeğer doğrulanmış shaping çözümü gerekir. |
| P0 | `googlefonts/font_names`, `googlefonts/name/version_format` | Full Name `Fluma` yerine kontrolün beklediği `Fluma Regular`; version name kaydı `1.000` yerine `Version 1.000` biçiminde olmalı. |
| P0 | `googlefonts/vertical_metrics` | `OS/2.sTypoLineGap` ve `hhea.lineGap` 58; profil 0 istiyor. Dikey metrik düzeltmesi gerçek uygulamalarda satır aralığını etkileyebileceğinden kontrollü export/proof ile yapılmalı. |

WARN tarafında özellikle contour direction, colinear/overlapping segments, soft dotted mark davranışı, unreachable glyphs, separator glyphs ve `xAvgCharWidth` incelenmeli. `metadata/unreachable_subsetting` uyarısı tam Google Fonts METADATA.pb paketi olmadan yapılan yerel testte ayrıca yorum gerektirir. Tam liste ham rapordadır.

## Paket ve yayın hazırlığı

- Yerel `googlefont/FlumaFont` klasörü henüz Git deposu değil; public upstream/release doğrulanmadı.
- README'de henüz fontu gösteren bir görsel yok. Mevcut specimen görselleri bu görevde kullanılmadı.
- `.gs2` kaynağından UFO üreten ve fontları tek komutla yeniden kuran doğrulanmış pipeline yok. Mevcut `build_composites.py`, kaynak glyph türetme yardımcısı; TTF/OTF build'i değil.
- `requirements.txt` fontmake içeriyor, ancak mevcut README otomatik fontmake build'i olmadığını açıkça söylüyor. Paket bağımlılığı ile gerçek işlem hattı ayrı tutulmalı.

## Sıradaki teknik sıra

1. U+0115 için karakter tasarım kararını ver, kaynakta düzelt, yeni TTF/OTF export al ve outline/proof kontrolü yap.
2. Kaynak metadata, name kayıtları, copyright, version ve full name'i tutarlı hale getir. Export sonrası doğrula; yalnız binary patch ile kaynak gerçekliğini gizleme.
3. Dikey metrik ve Dutch mark attachment için kaynak tabanlı çözüm geliştir; uygulama render'ını karşılaştır.
4. Kaynak formatından UFO'ya dönüşüm ve tek komutluk build'i kurup taze export üzerinde Fontspector'ı yeniden çalıştır.
5. Teknik FAIL'ler giderildikten sonra outline WARN'lerini görsel proof ile değerlendir. README görseli ve public repo adımlarını specimen hazırlığı tamamlandığında ayrıca ele al.

## Güncel resmi dayanaklar

- [Google Fonts Quality Assurance](https://googlefonts.github.io/gf-guide/qa.html)
- [Google Fonts onboarding requirements](https://googlefonts.github.io/gf-guide/onboarding.html)
- [Google Fonts upstream repository structure](https://googlefonts.github.io/gf-guide/upstream.html)
- [Google Fonts license file requirements](https://googlefonts.github.io/gf-guide/license-file.html)
- [Google Fonts GF Latin Core tanımı](https://github.com/googlefonts/glyphsets/blob/main/GLYPHSETS.md#gf-latin-core)

Not: Resmi kılavuzun onboarding sayfası hâlâ FontBakery adını kullanırken QA sayfası Fontspector'ı güncel araç olarak anlatıyor. Bu denetimde QA sayfasındaki Fontspector komutu uygulandı.
