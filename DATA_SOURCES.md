# Veri kaynakları

Bu dosya, *Dil Psikolojisi* kitabının (Söylemez, 2026) Ek A ve Bölüm 21 çözümlemelerinde kullanılan bütün veri kaynaklarını, kaynakta belirtildiği biçimiyle lisans ya da kullanım koşullarını ve depoda yer almayan verilerin nasıl edinilip nereye yerleştirileceğini açıklar. Erişim tarihleri kitaptaki künyelerden alınmıştır.

Depo iki tür veri içerir:

* **Depoda bulunan veriler.** Yazarın ürettiği türetilmiş dosyalar (sayımlar, kodlanmış ulamlar, sonuç JSON dosyaları), kamuya açık YÖK Ulusal Tez Merkezi kayıtlarından kurulan tez listesi ve OpenAlex üst verisi (CC0). Bunlar `*/data/derived/`, `*/results/` ve `bolum_21/data/raw/` klasörlerindedir.
* **Depoda bulunmayan üçüncü taraf veriler.** Lisansı yeniden dağıtıma açıkça izin vermeyen ya da yalnızca ticari olmayan, aynı lisansla paylaşım koşuluna bağlı (NC-SA) derlemler depoya konmamıştır. Bu veriler `ek_a/data/external/` klasörüne aşağıdaki adımlarla yerleştirilir. Bu klasör `.gitignore` ile depo dışında tutulur.

Tablo ve şekillerin hangi verilere bağlı olduğu `README.md` dosyasındaki eşleme tablosunda verilmiştir.

## Özet

| Kaynak | Kullanıldığı yer | Depoda | Lisans / kullanım koşulu (kaynakta belirtildiği gibi) | Yerleştirileceği yer |
|---|---|---|---|---|
| CHILDES Türkçe, childes-tr (Çöltekin, 2015) | Ek A: Tablo A.1, A.11; Şekil A.1, A.3 | Hayır | Özgün veri CC BY-NC-SA 3.0; Çöltekin'in düzeltmeleri için CC BY-NC-SA 3.0 ya da CC0 | `ek_a/data/external/childes-tr/` |
| CHILDES Frogs Turkish Aksu-Koç ve Frogs English Slobin (TalkBank) | Ek A: Tablo A.2, A.3 | Hayır | TalkBank kullanım koşulları (kullanıcı hesabıyla erişim) | Betik korunmadı (bkz. README) |
| OpenSubtitles 2018 Türkçe sıklık listesi, FrequencyWords (Dave, 2018) | Ek A: Tablo A.4, Şekil A.2 | Hayır | CC BY-SA 4.0 (kitaptaki künyeye göre) | `ek_a/data/external/frequencywords/tr_full.txt` |
| Türkçe Ulusal Derlemi (TUD) 3.0 web arayüzü sayımları | Ek A: Tablo A.4 | Yalnız sayımlar (betik içinde) | Kayıtlı kullanıcı erişimi; derlem çıktılarının yeniden dağıtımına izin veren açık bir lisans belirtilmemiştir | Gerekmez |
| TUD 3.0 eş dizim listeleri | Ek A: Tablo A.5, A.6 | Hayır (yalnız sıra ve özet istatistikler) | Aynı | `ek_a/data/external/tnc_esdizim/` |
| Yapıcı (2015) çağrışım yanıtları, YÖK Tez No. 384575 | Ek A: Tablo A.5, A.6 | Seçilen 19 uyarıcının en sık 3 yanıtı | YÖK Ulusal Tez Merkezinde açık erişimli tez | `ek_a/data/derived/` (depoda) |
| UD Turkish IMST | Ek A: Tablo A.7 | Hayır | README: CC BY-NC-SA 4.0; LICENSE.txt: CC BY-NC-SA 3.0 | `ek_a/data/external/UD_Turkish-IMST/` |
| Gazete birinci sayfaları, haber7.com manşet galerileri | Ek A: Tablo A.8 | Yalnız tarih, gazete, düzey, kaynak adresi ve kodlar | Üçüncü taraf haber sitesi; yeniden dağıtım izni yok | `ek_a/data/external/manset/manset.tsv` (yeniden kurulur) |
| Altıparmak (2015), YÖK Tez No. 410342 | Ek A: Tablo A.9, A.10 | Tezde yayımlanan ortancalar ve örnekler | YÖK Ulusal Tez Merkezinde açık erişimli tez | `ek_a/data/derived/` (depoda) |
| MECO Türkçe alt kümesi ve XGLM şaşırtıcılık değerleri (de Varda ve Marelli, 2023) | Ek A: Tablo A.12, Şekil A.4 | Hayır | MECO ve şaşırtıcılık değerleri OSF'de açık erişimle yayımlanmaktadır; kullanılan dosyanın yanında lisans metni bulunmamaktadır | `ek_a/data/external/meco/meco_xglm` |
| wordfreq 3.1.1 (Speer, 2023) | Ek A: Tablo A.12 | Hayır (Python paketi) | Paketin kendi lisansı; `pip` ile kurulur | `requirements.txt` |
| YÖK Ulusal Tez Merkezi arama sonuçları | Bölüm 21: Tablo 21.4-21.6, 21.8; Şekil 21.1 | Evet | Kamuya açık tez kayıtları (künye üst verisi) | `bolum_21/data/raw/yok/` |
| OpenAlex API yanıtları | Bölüm 21: Tablo 21.7, 21.8 | Evet | CC0 | `bolum_21/data/raw/openalex/` |
| Ön tarama (OpenAlex tabanlı tarama aracı çıktısı) | Bölüm 21: kural-elle kodlama karşılaştırması | Evet, özetler çıkarılmış olarak | OpenAlex üst verisi, CC0 | `bolum_21/data/raw/on_tarama/yz.json` |

Bütün yerleştirmeler bittiğinde `ek_a/data/external/` klasörü şöyle görünmelidir:

```
ek_a/data/external/
├── childes-tr/                 # git deposu: Aksu/, Turkay/, README.md, LICENSE.md
├── frequencywords/tr_full.txt
├── meco/meco_xglm
├── UD_Turkish-IMST/            # git deposu: tr_imst-ud-{train,dev,test}.conllu
├── tnc_esdizim/<uyarıcı>.txt   # 19 dosya
└── manset/manset.tsv           # yeniden kurulan başlık dosyası
```

Dosyaların kitaptakiyle aynı sürüm olduğu aşağıdaki SHA-256 değerleriyle denetlenebilir (`sha256sum <dosya>`).

| Dosya | SHA-256 |
|---|---|
| `frequencywords/tr_full.txt` | `62fed3d295a3250920f8a151f597cb28208633b6ff6e7bff90faed51ee86a9a5` |
| `meco/meco_xglm` | `a75af19710ee0310465969ac393af90dfec19e0c47e7fb2fa9993ebee35fea20` |
| `UD_Turkish-IMST/tr_imst-ud-train.conllu` | `d7d65fb10bd0f6ed6ecb0258938d6d126a2b93b409582759d2b52195dd5b7313` |
| `UD_Turkish-IMST/tr_imst-ud-dev.conllu` | `f58d60666d3a9a7fea843b36444da5d6a7849b1172a851b2223479682c53d0d4` |
| `UD_Turkish-IMST/tr_imst-ud-test.conllu` | `299d3af2adb8722b5dd09cd17a20302af3670d36f2e57ed26170bf21526fd3d4` |
| `manset/manset.tsv` (kitaptaki aktarım) | `6676473316309ac2415e889c512905e99525d562fd1d771c63e7b27644e069aa` |

## Ek A

### CHILDES Türkçe derlemleri (Aksu-Koç ve Altınkamış), childes-tr

* **Kaynak.** Çöltekin, Ç. (2015). *childes-tr: An improved version of the Turkish section of CHILDES database* [Veri seti]. GitHub. https://github.com/coltekin/childes-tr. Derlemlerin özgün künyeleri: Aksu-Koç, A. (2004b). *CHILDES Turkish Aksu Koç corpus*. TalkBank. https://doi.org/10.21415/T5SP6C; Altınkamış, F. (2012). *CHILDES Turkish Altinkamis corpus*. TalkBank. https://doi.org/10.21415/T5H89W
* **Sürüm.** 2 Mart 2015 tarihli resmî CHILDES sürümüne dayanan düzeltilmiş biçim; kullanılan depo durumu `49761a75632fb062fc5f38c56925b063adb508dc` (16 Mart 2015). Erişim: 1 Kasım 2026.
* **Lisans (deponun README.md ve LICENSE.md dosyalarına göre).** "The original data seems to be licensed under Creative Commons by-nc-sa (3.0)." Çöltekin'in yaptığı değişiklikler için kullanıcı CC BY-NC-SA 3.0 ile CC0 arasında seçim yapabilir. README ayrıca verinin uygun kullanımı için CHILDES sitesine yönlendirmektedir. Ticari olmayan kullanım ve aynı lisansla paylaşım koşulu bu deponun CC BY 4.0 lisansıyla bağdaşmadığından çeviri yazılar depoya konmamıştır.
* **Edinme ve yerleştirme.**
  1. `cd ek_a/data/external`
  2. `git clone https://github.com/coltekin/childes-tr.git`
  3. `cd childes-tr && git checkout 49761a75632fb062fc5f38c56925b063adb508dc`
  4. `ek_a/data/external/childes-tr/Aksu/*.cha` (54 dosya) ve `ek_a/data/external/childes-tr/Turkay/*.cha` (15 dosya) bulunmalıdır. `2haf.cha` (aynı oturumun ikinci çeviri yazısı) ve `6fb.cha` (konuşucu kodlaması bozuk) betiklerde dışarıda bırakılır.
* **Depodaki türetilmiş dosya.** `ek_a/data/derived/a1_zeyrek_cozumlemeleri.json`, derlemdeki 9.220 farklı sözcük yazılışının Zeyrek 0.1.3 çözümlemelerini içerir. Dosya söyleyiş, sıra, konuşucu ya da oturum bilgisi taşımaz. Zeyrek aynı sözcük için aday çözümlemelerin sırasını Python'un karma tohumuna bağlı olarak değiştirebildiğinden kitaptaki değerler bu sözlükle üretilir (bkz. README, "Belirlenimcilik").

### CHILDES Frogs derlemleri (Tablo A.2 ve A.3)

* **Kaynak.** Aksu-Koç, A. (2004a). *CHILDES Frogs Turkish Aksu-Koç corpus*. TalkBank. https://doi.org/10.21415/T5D015; Marchman, V., Renner, T. ve Slobin, D. (2010). *CHILDES Frogs English Slobin corpus*. TalkBank. https://doi.org/10.21415/T5DG78
* **Erişim.** TalkBank üzerinden kullanıcı hesabıyla, 1 Kasım 2026. Türkçe 40 anlatı (3, 5, 9 ve 20 yaş), İngilizce 47 anlatı (aynı yaş grupları).
* **Lisans.** TalkBank kullanım koşulları; verilere kullanıcı hesabıyla erişilir. Veriler depoya konmamıştır.
* **Durum.** Bu iki tabloyu üreten sınıflama betiği ve ara sayımlar paket hazırlanırken bulunamamıştır; tablolar bu depodan yeniden üretilemez. Verinin edinilmesi için https://talkbank.org adresinden hesap açılır ve yukarıdaki DOI'lerle gösterilen iki derlem CHILDES'ın Frogs bölümünden indirilir. Sınıflama ölçütleri `CODEBOOK.md` dosyasında ve Ek A metninde verilmiştir.

### OpenSubtitles 2018 Türkçe sıklık listesi (FrequencyWords)

* **Kaynak.** Dave, H. (2018). *FrequencyWords* [OpenSubtitles 2018 derleminden üretilen Türkçe sözcük sıklığı listesi]. GitHub. https://github.com/hermitdave/FrequencyWords; Lison, P., Tiedemann, J. ve Kouylekov, M. (2018). OpenSubtitles2018. *LREC 2018*. https://aclanthology.org/L18-1275/
* **Sürüm.** `content/2018/tr/tr_full.txt`; 224.163.257 sözcük, 2.035.629 farklı yazılış. Erişim: 1 Kasım 2026.
* **Lisans.** Kitaptaki künyede belirtildiği gibi Creative Commons BY-SA 4.0. Aynı lisansla paylaşım koşulu nedeniyle liste depoya konmamıştır; depoda yalnızca 7 adın 77 çekim hücresine ait sayımlar (`ek_a/results/a3_grid.json`) ve ad başına özet sayımlar (`ek_a/results/a3_forms.json`) bulunur.
* **Edinme ve yerleştirme.**
  1. https://github.com/hermitdave/FrequencyWords deposundan `content/2018/tr/tr_full.txt` dosyasını indirin (ör. `https://raw.githubusercontent.com/hermitdave/FrequencyWords/master/content/2018/tr/tr_full.txt`).
  2. Dosyayı `ek_a/data/external/frequencywords/tr_full.txt` olarak kaydedin ve SHA-256 değerini denetleyin.

### Türkçe Ulusal Derlemi (TUD) 3.0

* **Kaynak.** Aksan, Y. vd. (2012). Construction of the Turkish National Corpus (TNC). *LREC'12*, 3223-3227. https://aclanthology.org/L12-1590/. Web arayüzü: https://www.tnc.org.tr
* **Sürüm.** Web arayüzünde sunulan 3.0 sürümü: 1990-2013 yılları arasında üretilmiş 5.445 metin, 50.678.199 sözcük; eş dizim sorgularında yaklaşık 49,7 milyon sözcüklük yazılı bölüm. Erişim: 1 Kasım 2026.
* **Kullanım koşulu.** Derleme kayıtlı kullanıcı olarak web arayüzünden erişilir; arayüz çıktılarının yeniden dağıtımına izin veren açık bir lisans belirtilmemiştir. Bu nedenle eş dizim listeleri depoya konmamıştır. Depoda yalnızca kitapta da basılı olan sayımlar (Tablo A.4'teki *ev*, *köy* ve *yol* biçim sıklıkları, `a3_tnc.py` ve `tablolar_ek_a.py` içinde) ve çağrışım yanıtlarının eş dizim sırası, uyarıcının sıklığı ile en güçlü 4 içerik sözcüğü eş dizimi gibi özet istatistikler (`ek_a/results/a4_results.json`, `ek_a/data/derived/tud_esdizim_ozet.tsv`) bulunur.
* **Tablo A.4 sayımlarını yineleme.** TUD arayüzünde standart sorguyla *ev* ve *köy* adlarının 11'er biçimi (`a3_freq.py` içindeki liste) ile *yol*, *yollar*, *yola* biçimleri sorgulanır. Elde edilen sayılar `a3_tnc.py` içindeki `TNC` sözlüğüyle karşılaştırılabilir.
* **Eş dizim listelerini edinme ve yerleştirme (Tablo A.5 ve A.6'yı baştan üretmek için).**
  1. https://www.tnc.org.tr adresinde hesap açıp oturum açın.
  2. Seçilen 19 uyarıcının her biri için (`ek_a/data/derived/yapici2015_secilen_uyaricilar.tsv`, `uyarici` sütunu) yazılı bölümde eş dizim (collocation) sorgusu yapın: arama biçimi uyarıcının yalın biçimi, pencere sağda ve solda 5 sözcük, sıralama log-olabilirlik, liste uzunluğu 2.500.
  3. Sonuç tablosu sayfada açıkken `python3 ek_a/scripts/a4_tnc_js.py <uyarıcı>` komutunun yazdığı JavaScript kodunu tarayıcının geliştirici konsolunda çalıştırın.
  4. Konsolun döndürdüğü metni `ek_a/data/external/tnc_esdizim/<uyarıcı>.txt` dosyasına kaydedin (ör. `anne.txt`). İlk satır `F <uyarıcı sıklığı> N <liste uzunluğu> minLL <en düşük LL>` bilgisini, ikinci satır listenin ilk 45 sözcüğünü, sonraki satırlar her yanıt için listedeki eşleşen biçimleri taşır.
  5. `ek_a/scripts/a4_assoc.py` betiğini çalıştırın. Arayüzün güncellenmesi durumunda sıralar kitaptakilerden ayrılabilir.

### Yapıcı (2015) çağrışım verisi

* **Kaynak.** Yapıcı, F. (2015). *Rus ruhdilbilim kuramları bağlamında çağrışım sözlüğü (Rusça-Türkçe karşılaştırmalı inceleme)* (Tez No. 384575) [Doktora tezi, Gazi Üniversitesi]. YÖK Ulusal Tez Merkezi. Erişim: 1 Kasım 2026.
* **Depoda.** `ek_a/data/derived/yapici2015_secilen_uyaricilar.tsv`: çözümlemede kullanılan 19 uyarıcı için tezin yorum bölümünde verilen en sık 3 yanıt (Tablo A.5'te de basılıdır) ve yanıtın basıldığı PDF sayfası.
* **Tam listeyi yeniden kurma.** Tezin tam metni https://tez.yok.gov.tr adresinde 384575 numarasıyla açılır. Yorum bölümü PDF sayfa 165-230'dadır (basılı sayfa = PDF sayfası - 11). Her uyarıcının "TR-" ile başlayan satırındaki ilk üç yanıt alınır.

### UD Turkish IMST ağaç yapılı derlemi

* **Kaynak.** Sulubacak, U. ve Eryiğit, G. (2018). *Turkish Journal of Electrical Engineering & Computer Sciences, 26*(3), 1662-1672. https://doi.org/10.3906/elk-1706-81; Sulubacak, U. vd. (2016). Universal dependencies for Turkish. *COLING 2016*, 3444-3454. Depo: https://github.com/UniversalDependencies/UD_Turkish-IMST
* **Sürüm.** Deponun 6 Mayıs 2026 tarihli durumu, işleme (commit) `0c939115d8277ecfb39e1bbc3f066b1852ab5ddc`; 5.635 cümle, 58.096 sözcük. Erişim: 1 Kasım 2026.
* **Lisans.** Deponun README.md dosyası: "The IMST-UD Treebank is licensed under Creative Commons (CC BY-NC-SA 4.0)." Aynı depodaki LICENSE.txt dosyası ise CC BY-NC-SA 3.0 metnini içermektedir. İki metin de ticari olmayan kullanım ve aynı lisansla paylaşım koşulu taşıdığından derlem depoya konmamıştır; depoda yalnızca sayımlar (`ek_a/results/a5_results.json`) bulunur. Ek A'da da belirtildiği gibi derlemden kitapta yalnızca kısa alıntılar ve istatistikler verilmektedir.
* **Edinme ve yerleştirme.**
  1. `cd ek_a/data/external`
  2. `git clone https://github.com/UniversalDependencies/UD_Turkish-IMST.git`
  3. `cd UD_Turkish-IMST && git checkout 0c939115d8277ecfb39e1bbc3f066b1852ab5ddc`
  4. Üç `.conllu` dosyasının SHA-256 değerlerini denetleyin.

### Gazete birinci sayfa başlıkları (2025)

* **Kaynak.** Haber7. (2025). *Gazete manşetleri* [Günlük birinci sayfa galerileri, 14 Ocak-12 Aralık 2025]. https://www.haber7.com/gazete-mansetleri. Erişim: 1 Kasım 2026. Hürriyet, Sabah ve Milliyet'in 12 tarihteki birinci sayfaları (36 sayfa); tarihler: 14 Ocak, 14 Şubat, 14 Mart, 16 Nisan, 16 Mayıs, 16 Haziran, 15 Temmuz, 13 Ağustos, 15 Eylül, 15 Ekim, 14 Kasım, 12 Aralık 2025.
* **Kullanım koşulu.** Sayfa görüntüleri üçüncü taraf bir haber sitesinde yayımlanmaktadır ve başlık metinlerinin yeniden dağıtımına ilişkin bir izin bulunmamaktadır. Bu nedenle başlık metinleri depoya konmamıştır.
* **Depoda.** `ek_a/data/derived/manset_kodlar.tsv`: çözümlemedeki 568 başlığın her biri için başlık kimliği, tarih, gazete, düzey (manşet ya da öteki başlık), sayfa içi sıra, galeri adresi ve kodlar (bkz. `CODEBOOK.md`). Tablo A.8 bu dosyadan `tablolar_ek_a.py` ile başlık metni olmadan üretilir.
* **Başlık dosyasını yeniden kurma (a5_manset.py ve a5_manset_final.py için gerekir).** Sınıflama betikleri başlığın sözcüklerini Zeyrek ile çözümlediğinden başlık metnine gereksinim duyar.
  1. `manset_kodlar.tsv` dosyasındaki `kaynak_url` adreslerinden her tarihin galerisini açın; her galeri sayfası bir gazetenin birinci sayfasını 750 piksel genişlikte gösterir. Galeride sıra tarihten tarihe değiştiğinden gazete adını ve tarihi sayfanın künyesinden doğrulayın. Galeri adresi artık çalışmıyorsa sayfalar gazetelerin kendi arşivlerinden ya da kütüphane koleksiyonlarından aynı tarih için edinilebilir.
  2. Her sayfadan şu satırları aktarın: sayfadaki en büyük puntolu başlık (`duzey` = `manşet`, her sayfada bir tane); manşete bağlı spot metni ve manşete ait üst başlık (`spot`); sayfadaki öteki haber başlıkları, üst bant haberleri ve spor kutuları dahil (`diğer`). Haber içindeki madde başı ya da ara başlıklar, fotoğraf altı yazıları, köşe yazarı adları, ilanlar, kutlama bantları, skor grafikleri ve sayfa içindeki küçültülmüş eski gazete görüntüleri alınmaz.
  3. Yazım kuralları: tamamı büyük harfle basılmış başlıklar Türkçe cümle düzenine çevrilir (özel adlar büyük harfle, İ/ı doğru); karışık harfle basılmış başlıklar basıldığı gibi bırakılır; kısaltmalar (CHP, MHP, DEM, İBB, ABD, TİSK, MSB, OGM, HSK, KKTC, DNA, TIR, POS, LGS, YKS) büyük harfle korunur; birden çok satıra bölünmüş başlıklar tek boşlukla birleştirilir; kesin okunamayan küçük başlıklar tahminle doldurulmaz.
  4. Satırları sekmeyle ayrılmış `tarih	gazete	duzey	baslik	kaynak_url` sütunlarıyla (tarih `2025-01-14` biçiminde, gazete `Hürriyet`, `Sabah` ya da `Milliyet`) `ek_a/data/external/manset/manset.tsv` dosyasına yazın.
  5. `python3 ek_a/scripts/a5_manset_eslestir.py` ile her satırın başlık kimliğini kod dosyasıyla eşleştirin. Kimlik `tarih|gazete|başlık` dizgesinin SHA-1 özetinin ilk 12 karakteridir; başlık kitaptaki aktarımla harfi harfine aynıysa kimlik eşleşir ve elle verilen kararlar (`a5_manset_final.py`, `OV`) doğru başlığa uygulanır. Kitaptaki aktarımla birebir aynı dosyanın SHA-256 değeri yukarıdaki tabloda verilmiştir. Manşet bloğu içindeki 4 ara başlık (`a5_manset.py`, `DROP`) çözümleme dışındadır.
  6. `PYTHONHASHSEED=0 python3 ek_a/scripts/a5_manset.py` ve `python3 ek_a/scripts/a5_manset_final.py` komutlarını çalıştırın.

### Altıparmak (2015) akıcısızlık verisi

* **Kaynak.** Altıparmak, A. (2015). *Türkçe konuşmada akıcısızlık: Psikodilbilimsel bir inceleme* (Tez No. 410342) [Doktora tezi, Dokuz Eylül Üniversitesi]. YÖK Ulusal Tez Merkezi. Erişim: 1 Kasım 2026.
* **Depoda.** `ek_a/data/derived/altiparmak2015_ortancalar.csv` (tezin 121-128. sayfalarındaki tablolardan aktarılan ortancalar ve Kruskal-Wallis p değerleri; Tablo A.9) ve `ek_a/data/derived/tablo_A10_surcme_kodlari.tsv` (tezin 117-119. sayfalarındaki örnek söyleyişler ve bu çözümlemede verilen kodlar; Tablo A.10). Çeviri yazılar yayımlanmamıştır.

### MECO Türkçe alt kümesi ve XGLM şaşırtıcılık değerleri

* **Kaynak.** Siegelman, N. vd. (2022). Expanding horizons of cross-linguistic research on reading: The Multilingual Eye-movement Corpus (MECO). *Behavior Research Methods, 54*(6), 2843-2863. https://doi.org/10.3758/s13428-021-01772-6 (veri: https://osf.io/3527a/); de Varda, A. ve Marelli, M. (2023). Scaling in cognitive modelling: A multilingual approach to human reading times. *ACL 2023 (Short papers)*, 139-149. https://doi.org/10.18653/v1/2023.acl-short.14 (kod: https://github.com/Andrea-de-Varda/surprisal-across-languages); Lin, X. V. vd. (2022). XGLM. *EMNLP 2022*. https://doi.org/10.18653/v1/2022.emnlp-main.616
* **Sürüm.** `meco_xglm`: MECO L1 göz izleme verisinin XGLM 564M, 1,7B, 2,9B ve 4,5B sözcük düzeyi şaşırtıcılık değerleriyle (`s`, `s_1.7`, `s_2.9`, `s_4.5`; doğal logaritma; alt sözcük birimi sayısı `m`, ...) birleştirilmiş CSV dosyası (yaklaşık 221 MB, 13 dil; Türkçe 31.930 satır, 29 okur, 12 metin). Dosya, de Varda ve Marelli'nin `code/XGLM_surprisal.py` betiğinin çıktısıdır (betiğin son satırı: `meco.to_csv("meco_xglm")`); kullanılan kod deposu durumu `c337cdc3dc22d7caf630b6d43b5d063f2a3ffd8e` (3 Mayıs 2023). Erişim: 1 Kasım 2026.
* **Lisans.** Ek A'da belirtildiği gibi MECO verisi ve şaşırtıcılık değerleri OSF üzerinde açık erişimle yayımlanmaktadır. Kullanılan dosyanın ve kod deposunun yanında bir lisans metni bulunmamaktadır; yeniden dağıtım koşulu açıkça belirtilmediğinden dosya depoya konmamıştır. Kullanmadan önce OSF proje sayfasındaki lisans alanını denetleyin.
* **Edinme ve yerleştirme.**
  1. `meco_xglm` dosyasını de Varda ve Marelli'nin (2023) OSF'de yayımlanan gereçlerinden indirin (bağlantılar makalede ve kod deposunun README dosyasında verilmektedir).
  2. Dosya bulunamazsa aynı dosya şöyle yeniden üretilebilir: MECO L1 verisini (https://osf.io/3527a/, `Meco_l1.csv` türünden sözcük düzeyi dosya) indirin; `git clone https://github.com/Andrea-de-Varda/surprisal-across-languages.git` ve `git checkout c337cdc3dc22d7caf630b6d43b5d063f2a3ffd8e`; `code/XGLM_surprisal.py` içindeki MECO dosya yolunu düzenleyip betiği çalıştırın (XGLM modelleri Hugging Face'ten indirilir: `facebook/xglm-564M`, `facebook/xglm-1.7B`, `facebook/xglm-2.9B`, `facebook/xglm-4.5B`). Yeniden hesaplanan şaşırtıcılık değerleri donanım ve kitaplık sürümlerine bağlı olarak küçük farklar gösterebilir.
  3. Dosyayı `ek_a/data/external/meco/meco_xglm` olarak kaydedin ve SHA-256 değerini denetleyin.
* **Sözcük sıklığı.** Zipf değerleri `wordfreq` 3.1.1 paketinin Türkçe listesinden hesaplanır (Speer, R. (2023). *wordfreq* (Sürüm 3.1.1). https://pypi.org/project/wordfreq/3.1.1/). Paket `requirements.txt` ile kurulur; farklı bir sürüm Zipf değerlerini ve dışlanan sözcük sayısını değiştirebilir.

## Bölüm 21

### YÖK Ulusal Tez Merkezi aramaları

* **Kaynak.** YÖK Ulusal Tez Merkezi, https://tez.yok.gov.tr. Arama tarihi: 30 Ekim 2026.
* **Sorgu.** 6 terim (psikodilbilim, ruhdilbilim, psikolinguistik, dil psikolojisi, psycholinguistic, psycholinguistics); alan: tümü (tez adı, konu, anahtar sözcük, özet); tez durumu: onaylandı; eşleşme türü: içersin; sayfa başına 50 sonuç. Sorgu günlüğü: `bolum_21/data/raw/yok/sorgu_gunlugu.csv` (günlükteki e-posta adresi kaldırılmıştır; aynı dosyadaki üç başarısız OpenAlex denemesi bilgi amaçlı tutulmuştur).
* **Lisans.** Tez künyeleri kamuya açık YÖK kayıtlarıdır. Depoda yalnızca künye üst verisi (tez numarası, yıl, tür, dil, üniversite, konu alanı, başlık, eşleşen sorgular ve bu çalışmadaki kapsam kararı) bulunur; tez metinleri bulunmaz.
* **Depoda.** `bolum_21/data/raw/yok/ham/q_*.tsv` (her terimin ham arama sonucu), `yoktez_tum_kayitlar.csv` (tez numarasıyla tekilleştirilmiş 167 kayıt), `yoktez_ilgisiz.csv` (kapsam dışı bırakılan 33 kayıt ve nedeni).
* **Yeniden arama.** https://tez.yok.gov.tr/UlusalTezMerkezi/ adresinde "Detaylı tarama" ile yukarıdaki ölçütler kullanılır. YÖK'e gecikmeli yüklenen tezler nedeniyle son yılların sayıları arama tarihine göre artabilir.

### OpenAlex

* **Kaynak.** OpenAlex, https://openalex.org (Priem, J., Piwowar, H. ve Orr, R. (2022). OpenAlex: A fully-open index of scholarly works, authors, venues, institutions, and concepts. arXiv:2205.01833). Sorgu tarihi: 2 Kasım 2026.
* **Lisans.** OpenAlex verisi CC0 ile yayımlanmaktadır.
* **Sorgu.** `title_and_abstract.search:(psycholinguistic OR "sentence processing" OR "word recognition" OR "language acquisition" OR aphasia OR psycholinguistics OR "language processing" OR psikodilbilim OR ruhdilbilim),publication_year:1936-2026,type:!paratext`; Türkiye kümesi için ek süzgeç `authorships.institutions.country_code:tr`.
* **Depoda.** `bolum_21/data/raw/openalex/`: dünya ve Türkiye toplamları (`dunya_toplam.json`, `tr_toplam.json`), yıl, kurum, dil, tür ve alt alan sayımları (`*_yil.json`, `tr_kurum.json`, `tr_dil.json`, `tr_tur.json`, `tr_altalan.json`) ve Türkiye kayıtlarının imleçle (cursor) 200 kayıtlık sayfalar hâlinde indirilmiş 16 ham yanıtı (`tr_kayit_00.json`-`tr_kayit_15.json`; 3.020 satır, 3.010 tekil kayıt). Yanıtlarda API anahtarı yer almaz. Yazarların ham kurum adreslerinde (`raw_affiliation_strings`, `raw_affiliation_string`) geçen 428 e-posta adresi `[e-posta kaldirildi]` ile değiştirilmiş, kurum ve kaynak adlarında kalan üç "at" işareti JSON kaçış dizisiyle (`\u0040`) yazılmıştır; bu alanlar çözümlemede kullanılmadığından sonuçlar değişmez.
* **Yeniden sorgu.** `bolum_21/scripts/oa21_key.py`; ayrıntılar README'dedir. OpenAlex API anahtarı yalnızca `OPENALEX_API_KEY` ortam değişkeninden okunur. Kitaptaki indirme 200 kayıtlık sayfalarla yapılmıştır; yeniden çalıştırmada `OA_PER_PAGE=100` kullanılabilir, sonuçlar sayfa büyüklüğüne bağlı değildir. OpenAlex sürekli güncellendiğinden yeni bir sorgunun sayıları ve atıf sayıları 2 Kasım 2026 tarihli yanıtlardan ayrılacaktır.

### Ön tarama

* **Kaynak.** Aynı dokuz terimle, OpenAlex tabanlı bir bibliyometrik tarama aracıyla 1 Kasım 2026'da yapılan tarama (araç şeması `bibliyometrik-tarama-araci/1.0`). Türkiye süzgeci, ilgi sıralamasıyla indirilen en çok 49.899 kayıt üzerinde yerel olarak uygulanmış ve 218 kayıt vermiştir.
* **Lisans.** OpenAlex üst verisi, CC0.
* **Depoda.** `bolum_21/data/raw/on_tarama/yz.json`: 218 kaydın DOI, başlık, yıl, kaynak, tür, dil, yazar, kurum, ülke, konu ve atıf alanları ile taramanın yöntem künyesi. Kayıt sırası özgün çıktıdaki gibidir (elle kodlama dosyası `bolum_21/data/derived/on_tarama_kod.json` bu sıraya göre numaralanır). Özgün çıktıdaki özetler (yayıncı metni olabileceğinden) ve aracın ürettiği özet göstergeler çıkarılmıştır.
