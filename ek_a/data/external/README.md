# Üçüncü taraf veriler (depoda yok)

Bu klasöre, lisansı yeniden dağıtıma izin vermediği için depoya konmayan veriler yerleştirilir. Klasörün içeriği (bu dosya dışında) `.gitignore` ile depo dışında tutulur. Her kaynağın künyesi, sürümü, lisansı ve edinme adımları kök dizindeki `DATA_SOURCES.md` dosyasındadır.

```
childes-tr/                 # https://github.com/coltekin/childes-tr (işleme 49761a7)
frequencywords/tr_full.txt  # https://github.com/hermitdave/FrequencyWords, content/2018/tr/tr_full.txt
meco/meco_xglm              # MECO L1 + XGLM şaşırtıcılık değerleri (de Varda ve Marelli, 2023)
UD_Turkish-IMST/            # https://github.com/UniversalDependencies/UD_Turkish-IMST (işleme 0c93911)
tnc_esdizim/<uyarıcı>.txt   # TUD 3.0 eş dizim listeleri (19 dosya; a4_tnc_js.py ile)
manset/manset.tsv           # yeniden kurulan 2025 gazete başlıkları
```
