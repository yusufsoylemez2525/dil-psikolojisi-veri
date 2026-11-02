# dil-psikolojisi-veri
# Dil Psikolojisi: Ek A ve Bölüm 21 veri ve betik paketi

Bu depo, Yusuf Söylemez'in *Dil Psikolojisi* (Fenomen Yayıncılık, 2026) kitabında iki kesimin sayısal sonuçlarını yeniden üretmek için gereken betikleri, türetilmiş verileri, sonuç dosyalarını ve şekilleri içerir:

* **Ek A. Kuramların Derlem Üzerinde Gösterimi**: Türkçe derlemler ve yayımlanmış veri setleri üzerinde yedi çözümleme (Tablo A.1-A.13, Şekil A.1-A.4).
* **Bölüm 21. Türkiye'de Dil Psikolojisinin Tarihi ve Bugünü**: YÖK Ulusal Tez Merkezi ve OpenAlex verileriyle tez ve yayın görünümü (Tablo 21.4-21.8, Şekil 21.1).

Lisansı yeniden dağıtıma açıkça izin vermeyen üçüncü taraf derlemler depoda yoktur. Bu verilerin künyesi, sürümü, lisansı ve edinme adımları `DATA_SOURCES.md` dosyasında, kodlanmış değişkenler ve ulamlar `CODEBOOK.md` dosyasında açıklanmıştır. Bölüm 21'in bütün adımları ile Ek A'daki tabloların ve şekillerin son adımı yalnızca depodaki dosyalarla çalışır.

## English summary

This repository is the reproducibility package for Appendix A (seven corpus analyses illustrating psycholinguistic theories on Turkish data) and Chapter 21 (theses and publications on psycholinguistics in Turkey) of the Turkish book *Dil Psikolojisi* (Psychology of Language) by Yusuf Söylemez (Fenomen Yayıncılık, 2026). It contains the Python 3.13 scripts, derived data (counts, coded categories), result files and figures. Third-party corpora whose licences do not clearly permit redistribution (CHILDES/TalkBank transcripts, UD Turkish IMST, MECO, the OpenSubtitles frequency list, Turkish National Corpus outputs, newspaper headline texts) are not included; `DATA_SOURCES.md` gives the exact source, version, licence and step-by-step instructions to obtain each of them and where to place them (`ek_a/data/external/`). All Chapter 21 steps (YÖK thesis coding, OpenAlex coding from the stored CC0 API responses) and the final table and figure steps of Appendix A run from the files in this repository alone; they were run from a clean copy and reproduce the numbers printed in the book. Code is released under the MIT licence; data, text and figures under CC BY 4.0 (see `LICENSE`). The OpenAlex API key is read only from the environment variable `OPENALEX_API_KEY`.

## Klasör düzeni

```
dil-psikolojisi-veri/
├── README.md               bu dosya
├── DATA_SOURCES.md         veri kaynakları, lisanslar, edinme ve yerleştirme adımları
├── CODEBOOK.md             kodlanmış değişkenler ve ulamlar
├── LICENSE                 MIT (kod) ve CC BY 4.0 (veri, metin, şekiller)
├── CITATION.cff            atıf bilgisi
├── requirements.txt        sabitlenmiş Python paketleri
├── ek_a/
│   ├── scripts/            a1_* ... a7_* çözümleme betikleri, tablolar_ek_a.py, yardımcı betikler
│   ├── data/
│   │   ├── derived/        yazarın türettiği ya da yayımlanmış tezlerden aktardığı veriler (depoda)
│   │   ├── external/       üçüncü taraf ham veriler (depoda yok; DATA_SOURCES.md'ye göre yerleştirilir)
│   │   └── work/           betiklerin ürettiği, ham metin içerebilen ara dosyalar (depoda yok)
│   ├── results/            sonuç JSON dosyaları ve tablolar_ek_a.py'nin ürettiği tablo_A*.csv
│   └── figures/            sekil_A_1.png ... sekil_A_4.png
└── bolum_21/
    ├── scripts/            tez_kod.py, tez_tablo.py, sekil_tez.py, oa21_key.py, oa_kod.py, oa_key_kod.py, tablolar_21.py
    ├── data/
    │   ├── raw/            YÖK arama sonuçları, OpenAlex API yanıtları (CC0), ön tarama kayıtları
    │   └── derived/        tez ve OpenAlex konu kodları, ön tarama elle kodlaması
    ├── results/            ozet2.json ve tablolar_21.py'nin ürettiği tablo_21_*.csv
    └── figures/            sekil_21_1.png
```

Ek A betiklerinin adlarındaki numara çözümlemenin Ek A'daki sırasıdır: `a1` çocuk dilinde çekim ekleri, `a2` kurbağa öyküleri (betik pakette yok, bkz. "Bilinen sınırlılıklar"), `a3` ekli sözcüklerde sıklık, `a4` çağrışım ve eş dizim, `a5` geçici yapısal belirsizlik, `a6` akıcısızlıklar ve diyalogda hizalanma, `a7` şaşırtıcılık ve okuma süresi.

Bütün betikler yolları depo köküne göre (`ROOT = Path(__file__).resolve().parents[2]`) kurar; herhangi bir çalışma dizininden çalıştırılabilir.

## Ortam

* Python 3.13 (sınama Python 3.13 ile yapılmıştır).
* Paketler, betiklerin içe aktardığı sürümlerle `requirements.txt` dosyasında sabitlenmiştir:

| Paket | Sürüm | Kullanıldığı betikler |
|---|---|---|
| matplotlib | 3.11.2 | şekil betikleri (`a1_figure.py`, `a3_figure.py`, `a6_figure.py`, `a7_figure.py`, `sekil_tez.py`) |
| numpy | 2.5.3 | şekil betikleri, `a7_meco.py`, `a7_cluster_se.py` |
| pandas | 3.0.5 | `a7_meco.py`, `a7_cluster_se.py` |
| statsmodels | 0.15.0 | `a7_meco.py`, `a7_cluster_se.py` (OLS ve karma etkili model) |
| wordfreq | 3.1.1 | `a7_meco.py`, `a7_cluster_se.py` (Zipf sıklığı) |
| zeyrek | 0.1.3 | `a1_parse.py`, `a3_forms.py`, `a4_assoc.py`, `a5_manset.py` (biçim bilimsel çözümleme) |

```
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Bölüm 21 betikleri yalnızca standart kitaplığı ve matplotlib'i kullanır. Şekiller DejaVu Serif yazı tipiyle çizilir; farklı bir matplotlib ya da yazı tipi sürümü görsel olarak küçük farklar doğurabilir, sayıları etkilemez.

## Hızlı doğrulama (üçüncü taraf veri gerektirmez)

Aşağıdaki komutlar depo kökünden, `ek_a/data/external/` boşken çalışır. Her biri depodaki sonuç, tablo ya da şekil dosyasının üzerine aynı içeriği yazar; `git diff` ile fark olmadığı görülebilir.

```
# Bölüm 21 (bütün adımlar)
python3 bolum_21/scripts/tez_kod.py          # tez konu kodları -> data/derived/tez_kod*.json
python3 bolum_21/scripts/tez_tablo.py        # Tablo 21.5, 21.6 ve metindeki tez sayımları (ekrana)
python3 bolum_21/scripts/sekil_tez.py        # Şekil 21.1
python3 bolum_21/scripts/oa21_key.py         # depodaki OpenAlex yanıtlarını birleştirir (ağ bağlantısı gerekmez)
python3 bolum_21/scripts/oa_kod.py           # ön tarama elle kodlaması -> data/derived/on_tarama_kod.json
python3 bolum_21/scripts/oa_key_kod.py       # OpenAlex konu grupları -> results/ozet2.json, data/derived/kod2.json
python3 bolum_21/scripts/tablolar_21.py      # Tablo 21.4-21.7 ve 21.8 sayıları -> results/tablo_21_*.csv

# Ek A (türetilmiş dosyalardan)
python3 ek_a/scripts/a3_tnc.py               # TUD ile alt yazı sıklıklarının Spearman ilişkisi (ρ = 0,85)
python3 ek_a/scripts/a1_figure.py            # Şekil A.1
python3 ek_a/scripts/a3_figure.py            # Şekil A.2
python3 ek_a/scripts/a6_figure.py            # Şekil A.3
python3 ek_a/scripts/a7_figure.py            # Şekil A.4
python3 ek_a/scripts/tablolar_ek_a.py        # Tablo A.1, A.4-A.9, A.11, A.12 -> results/tablo_A*.csv
```

## Tam yeniden üretim (üçüncü taraf veri gerektiren adımlar)

Aşağıdaki betikler önce `DATA_SOURCES.md`'deki verilerin `ek_a/data/external/` klasörüne yerleştirilmesini gerektirir. Her satırdaki betikler sırayla çalıştırılır; son adım olarak `tablolar_ek_a.py` ve şekil betikleri yeniden çalıştırılır.

| Çözümleme | Betikler (sırayla) | Gereken veri (`ek_a/data/external/`) |
|---|---|---|
| A.1 Çekim ekleri | `a1_parse.py` → `a1_analyze.py` → `a1_island_child.py` | `childes-tr/` |
| A.3 Sıklık | `a3_freq.py` → `a3_forms.py` | `frequencywords/tr_full.txt` |
| A.4 Çağrışım | `a4_assoc.py` (eş dizim listeleri `a4_tnc_js.py` ile alınır) | `tnc_esdizim/*.txt` |
| A.5 IMST | `a5_imst.py` | `UD_Turkish-IMST/` |
| A.5 Başlıklar | `a5_manset_eslestir.py` (denetim) → `a5_manset.py` → `a5_manset_final.py` | `manset/manset.tsv` |
| A.6 Hizalanma | `a6_align.py` → `a6_cluster.py` (önce `a1_parse.py` çalışmış olmalı) | `childes-tr/` |
| A.7 Okuma süresi | `a7_meco.py` → `a7_cluster_se.py` | `meco/meco_xglm` |

Zeyrek kullanan betikler için `PYTHONHASHSEED=0` önerilir (bkz. "Belirlenimcilik"):

```
PYTHONHASHSEED=0 python3 ek_a/scripts/a5_manset.py
```

Süre: sınama ortamında `a1_parse.py` yaklaşık 20 saniye, `a7_meco.py` yaklaşık 20 saniye, öteki betikler birkaç saniye sürmüştür.

## Tablo ve şekil eşlemesi

### Ek A

| Kitapta | Betik | Çıktı dosyası | Ham veri gerekir mi |
|---|---|---|---|
| Tablo A.1 | `a1_parse.py` → `a1_analyze.py` → `a1_island_child.py`; tablo: `tablolar_ek_a.py` | `ek_a/results/a1_results.json`, `a1_island_child_results.json` → `ek_a/results/tablo_A1.csv` | Sonuç JSON için evet (CHILDES); tablo için hayır |
| Tablo A.2 | betik pakette yok | - | TalkBank Frogs (bkz. sınırlılıklar) |
| Tablo A.3 | betik pakette yok | - | TalkBank Frogs (bkz. sınırlılıklar) |
| Tablo A.4 | `a3_freq.py`, `a3_tnc.py`; tablo: `tablolar_ek_a.py` | `ek_a/results/a3_grid.json` → `ek_a/results/tablo_A4.csv` | `a3_grid.json` için evet (FrequencyWords); tablo için hayır |
| Tablo A.5 | `a4_assoc.py`; tablo: `tablolar_ek_a.py` | `ek_a/results/a4_results.json`, `ek_a/data/derived/tud_esdizim_ozet.tsv` → `ek_a/results/tablo_A5.csv` | Sonuç JSON için evet (TUD eş dizim listeleri); tablo için hayır |
| Tablo A.6 | `a4_assoc.py` (ekrana); tablo: `tablolar_ek_a.py` | `ek_a/results/a4_results.json` → `ek_a/results/tablo_A6.csv` | Aynı |
| Tablo A.7 | `a5_imst.py`; tablo: `tablolar_ek_a.py` | `ek_a/results/a5_results.json` → `ek_a/results/tablo_A7.csv` | Sonuç JSON için evet (UD IMST); tablo için hayır |
| Tablo A.8 | `a5_manset.py` → `a5_manset_final.py`; tablo: `tablolar_ek_a.py` | `ek_a/data/derived/manset_kodlar.tsv` → `ek_a/results/tablo_A8.csv` | Kod dosyası için evet (başlık metinleri); tablo için hayır |
| Tablo A.9 | `tablolar_ek_a.py` | `ek_a/data/derived/altiparmak2015_ortancalar.csv` → `ek_a/results/tablo_A9.csv` | Hayır |
| Tablo A.10 | elle kodlama (betik yok) | `ek_a/data/derived/tablo_A10_surcme_kodlari.tsv` | Hayır |
| Tablo A.11 | `a6_align.py` → `a6_cluster.py`; tablo: `tablolar_ek_a.py` | `ek_a/results/a6_results.json`, `a6_cluster_results.json` → `ek_a/results/tablo_A11.csv` | Sonuç JSON için evet (CHILDES); tablo için hayır |
| Tablo A.12 | `a7_meco.py`, `a7_cluster_se.py`; tablo: `tablolar_ek_a.py` | `ek_a/results/a7_results.json` → `ek_a/results/tablo_A12.csv` | Sonuç JSON için evet (MECO); tablo için hayır |
| Tablo A.13 | yedi çözümlemenin metin sentezi (betik yok) | - | - |
| Şekil A.1 | `a1_figure.py` | `ek_a/figures/sekil_A_1.png` (girdi `a1_results.json`) | Hayır |
| Şekil A.2 | `a3_figure.py` | `ek_a/figures/sekil_A_2.png` (girdi `a3_grid.json`) | Hayır |
| Şekil A.3 | `a6_figure.py` | `ek_a/figures/sekil_A_3.png` (girdi `a6_results.json`, `AC_lag`) | Hayır |
| Şekil A.4 | `a7_figure.py` | `ek_a/figures/sekil_A_4.png` (girdi `a7_results.json`) | Hayır |

Metindeki türetilmiş sayıların bir bölümü de `tablolar_ek_a.py` tarafından ekrana yazılır: ortak biçimlerde Spearman ρ (0,85 ve 0,81), toplamsal modelin açıkladığı varyans ve Kendall W, ad başına çekimli biçim sayıları, önünde yalın özne bulunan nesneler, manşetlerdeki yüklemsiz başlıklar, Tablo A.9'daki oranlar, kümelenmiş z değerleri ve güven aralığı, karma model katsayısı ve Şekil A.4a aralıkları.

### Bölüm 21

| Kitapta | Betik | Çıktı dosyası | Ham veri gerekir mi |
|---|---|---|---|
| Tablo 21.4 | `tablolar_21.py` | `bolum_21/results/tablo_21_4.csv` (girdi `data/raw/yok/`) | Hayır (depoda) |
| Tablo 21.5 | `tez_tablo.py` (ekrana), `tablolar_21.py` | `bolum_21/results/tablo_21_5.csv` | Hayır |
| Şekil 21.1 | `sekil_tez.py` | `bolum_21/figures/sekil_21_1.png` | Hayır |
| Tablo 21.6 | `tez_kod.py` → `tez_tablo.py` (ekrana), `tablolar_21.py` | `bolum_21/data/derived/tez_kod.json` → `bolum_21/results/tablo_21_6.csv` | Hayır |
| Tablo 21.7 | `oa21_key.py` → `oa_kod.py` → `oa_key_kod.py` → `tablolar_21.py` | `bolum_21/results/ozet2.json`, `bolum_21/data/derived/kod2.json` → `bolum_21/results/tablo_21_7.csv` | Hayır (OpenAlex yanıtları depoda) |
| Tablo 21.8 | `tablolar_21.py` ("Araştırma çıktısı" sütunundaki tez ve çekirdek kayıt sayıları); öteki hücreler metin sentezidir | `bolum_21/results/tablo_21_8_sayilar.csv` | Hayır |

Kuralların elle kodlanmış ön tarama kesitiyle karşılaştırması (205 eşleşen kayıt, uyum yüzde 75,1, kappa 0,66, kesinlik yüzde 69,1, duyarlık yüzde 79,7) `oa_key_kod.py` tarafından `ozet2.json` dosyasının `karsilastirma` alanına yazılır.

## OpenAlex sorgusu

`oa21_key.py` önce `bolum_21/data/raw/openalex/` klasörüne bakar; bir yanıt dosyası varsa ağdan yeniden indirmez. Bu nedenle betik depodaki 2 Kasım 2026 tarihli yanıtlarla ağ bağlantısı ve API anahtarı olmadan çalışır.

* API anahtarı yalnızca `OPENALEX_API_KEY` ortam değişkeninden okunur; betiklerde anahtar yazılı değildir: `export OPENALEX_API_KEY=...` (anahtarsız istekler de çalışır, ancak günlük kota düşüktür).
* Kitaptaki indirme, imleçle (cursor) **200 kayıtlık sayfalar** hâlinde yapılmıştır (`tr_kayit_00.json`-`tr_kayit_15.json`, 3.020 satır). Yeniden çalıştırmada OpenAlex belgelerinin önerdiği **`per_page=100`** de kullanılabilir: `OA_PER_PAGE=100 python3 bolum_21/scripts/oa21_key.py`. Sonuçlar sayfa büyüklüğüne bağlı değildir. 200 dışındaki sayfa büyüklüklerinde sayfalar `bolum_21/data/work/openalex_pp<N>/` klasörüne yazılır ve `python3 bolum_21/scripts/oa_key_kod.py bolum_21/data/work/openalex_pp100` biçiminde kodlanır.
* Tam yeni bir sorgu için `bolum_21/data/raw/openalex/` içindeki yanıtları başka bir yere taşıyın. OpenAlex sürekli güncellendiğinden yeni bir sorgunun kayıt ve atıf sayıları kitaptakilerden ayrılacaktır.

## Rastgele tohumlar

| Betik | Tohum | Kullanım |
|---|---|---|
| `a1_analyze.py` | `random.seed(1)` | birleştirilmiş fiil adacığı karşılaştırması, 500 yineleme |
| `a1_island_child.py` | 1; duyarlılık için 2-21 | çocuk düzeyinde eşitlenmiş girdi, 500 yineleme (duyarlılıkta 200) |
| `a6_align.py` | `random.seed(7)` | taban çizgisi için her çiftte 40 uzak söyleyiş |
| `a6_cluster.py` | 7 (çiftler `a6_align.py` ile aynı sırada üretilir); 11 | çocuklar yerine koyarak yeniden örnekleme, 5.000 yineleme |
| `a5_manset.py` | `PYTHONHASHSEED=0` | Zeyrek çözümlemesinin belirlenimci olması için (aşağıya bakın) |

Öteki betiklerde rastgele çekim yoktur (`a7_meco.py` ve `a7_cluster_se.py` OLS ve karma etkili modelleri belirlenimci olarak kestirir).

## Belirlenimcilik

Zeyrek 0.1.3, aynı sözcük için aday çözümlemelerin sırasını ve kimi adayları Python'un karma tohumuna bağlı olarak değiştirebilmektedir. Bu durum iki yerde sonuca dokunur:

* **A.1 ve A.6.** `a1_parse.py`, kitaptaki değerleri üreten çözümleme sözlüğünü (`ek_a/data/derived/a1_zeyrek_cozumlemeleri.json`) öntanımlı olarak kullanır; bu sözlükle `a1_parse.py`'den `a6_cluster.py`'ye kadar bütün çıktılar kitaptakilerle birebir aynıdır. Sözlük olmadan yeniden çözümleme (`A1_YENIDEN_COZUMLE=1`) sınamada fiil belirteci sayılarını birkaç belirteç değiştirmiştir (ör. Altınkamış derleminde 127 yerine 124 çekimli fiil).
* **A.5 başlıkları.** `a5_manset.py`, `PYTHONHASHSEED=0` ile çalıştırıldığında kitaptaki sınıflamayı birebir verir. Başka tohumlarla 568 başlığın 0-2'sinin otomatik sınıfı değişebilir.

`a3_forms.py` ve `a4_assoc.py` sınanan bütün tohumlarda aynı sonucu vermiştir.

## Doğrulama

Paket, temiz bir kopyada iki biçimde sınanmıştır.

1. **Üçüncü taraf veri olmadan.** "Hızlı doğrulama" bölümündeki bütün komutlar `ek_a/data/external/` boşken çalıştırılmıştır. `tez_kod.json`, `tez_kod_oto.json`, `on_tarama_kod.json`, `kod2.json` ve `ozet2.json` özgün çıktılarla birebir aynıdır; beş şekil piksel düzeyinde özgün şekillerle aynıdır. Tablo 21.4-21.7'nin bütün hücreleri, Tablo 21.8'deki sayılar (8, 26 ve 87 tez; 6, 54 ve 329 çekirdek kayıt) ve Tablo A.1, A.5-A.9, A.11 ve A.12'nin bütün hücreleri kitaptaki değerlerle örtüşmektedir.
2. **Üçüncü taraf verilerle.** `DATA_SOURCES.md`'deki sürümler yerleştirilerek "Tam yeniden üretim" tablosundaki bütün betikler çalıştırılmıştır. `a1_results.json`, `a1_island_child_results.json`, `a3_grid.json`, `a3_forms.json`, `a4_results.json`, `a5_results.json`, `a6_results.json`, `a6_cluster_results.json`, `a7_results.json` ve başlık sınıflaması depodaki dosyalarla aynıdır (`a7_results.json`'a bu pakette önceki sözcüğün şaşırtıcılığı için standart hata, `se_prev`, eklenmiştir).

Bilinen farklar:

* **Tablo A.4, yuvarlama.** Kitapta yalın hücrenin ortalama payı 43,5, -lAr hücresinin aralığı 0,7-9,6 olarak basılmıştır. Bu değerler iki aşamalı yuvarlamadan (önce iki ondalığa) gelmektedir; tek aşamada yuvarlanmış değerler 43,4 (43,448) ve 0,6-9,5'tir (0,648 ve 9,549). `tablolar_ek_a.py` tek aşamalı yuvarlamayı kullanır.
* **Atlanma oranı ile şaşırtıcılık ilişkisi.** Ek A'daki r = −0,36 değeri metnin bütün sözcükleri (1.696) üzerinden hesaplanan ilişkiye (−0,355) karşılık gelir; son dışlama adımından önceki 1.307 sözcükte ilişki −0,349'dur. İki değer de `a7_cluster_se.py` tarafından yazılır.

## Bilinen sınırlılıklar

* **Tablo A.2 ve A.3 (kurbağa öyküleri).** Bu iki tabloyu üreten sınıflama betiği ve ara sayımlar paket hazırlanırken bulunamamıştır; tablolar bu depodan yeniden üretilemez. Ölçütler `CODEBOOK.md`'de ve Ek A metnindedir, verinin kaynağı `DATA_SOURCES.md`'dedir.
* **Başlıklardaki belirtme durumlu nesneler.** Ek A'da başlıklardaki 67 belirtme durumlu nesnenin bağlandığı yüklemin elle belirlenmesi (56'sı ana yükleme) ve 26 -(y)AcAk biçiminin sınıflaması satır düzeyinde bir dosya olarak pakete aktarılmamıştır. `manset_kodlar.tsv` yalnızca otomatik aday sayılarını (`n_belirtme_aday`, `n_sifatfiil_aday`) içerir.
* **Tablo A.10 ve A.13.** Tablo A.10 tezde yayımlanan örneklerin elle kodlamasıdır (`tablo_A10_surcme_kodlari.tsv`); Tablo A.13 çözümlemelerin metin sentezidir. Bölüm 21'de Tablo 21.8'in sayı dışındaki hücreleri de metin sentezidir.
* **Tek kodlayıcı.** Elle yapılan bütün sınıflamalar tek kodlayıcıya dayanır; kodlayıcılar arası uyum hesaplanmamıştır.
* **Üçüncü taraf kaynakların kalıcılığı.** TUD web arayüzü ve haber7.com galerileri değişebilir; bu kaynaklardan baştan üretilen değerler kitaptakilerden ayrılabilir. Depodaki türetilmiş dosyalar kitaptaki durumu korur.

## Gizlilik ve veri ayıklama

* Sorgu günlüğündeki (`bolum_21/data/raw/yok/sorgu_gunlugu.csv`) e-posta adresi kaldırılmıştır. Betiklerde e-posta adresi, API anahtarı ya da kişisel dosya yolu yoktur.
* `a1_island_child_results.json` dosyasında CHILDES'taki çocuk adları yerine kesit içi takma kimlikler (K01, K02, ...) kullanılmıştır. `a1_results.json` dosyasından çeviri yazıdan alınan hata işaretli biçimler çıkarılmıştır (betik bunları yalnızca yerel `ek_a/data/work/` klasörüne yazar; biçimler Ek A metninde verilmiştir). `a5_results.json` dosyasından IMST örnek cümleleri çıkarılmıştır.
* Ön tarama dosyasından (`bolum_21/data/raw/on_tarama/yz.json`) kayıt özetleri çıkarılmıştır.
* OpenAlex ham yanıtlarında yazarların kurum adreslerinde geçen e-posta adresleri kaldırılmıştır (ayrıntı: `DATA_SOURCES.md`). Bu alanlar çözümlemede kullanılmaz; `ozet2.json` ve `kod2.json` ayıklanmış yanıtlarla birebir aynı çıkar.

## Atıf ve lisans

Atıf bilgisi `CITATION.cff` dosyasındadır:

> Söylemez, Y. (2026). *Dil Psikolojisi*. Fenomen Yayıncılık.

Depo adresi `CITATION.cff` dosyasında yer tutucu olarak bırakılmıştır (`https://github.com/KULLANICI/dil-psikolojisi-veri`); depo açıldığında güncellenmelidir.

Kod MIT lisansıyla, veri, metin ve şekiller CC BY 4.0 lisansıyla dağıtılır. OpenAlex verileri CC0 olarak kalır. Ayrıntılar `LICENSE` dosyasındadır.
