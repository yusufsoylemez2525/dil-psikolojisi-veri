# Kod kitabı

Bu dosya, depodaki türetilmiş veri dosyalarının değişkenlerini ve elle ya da kurala bağlı olarak verilen ulamları açıklar. Ek A'daki elle yapılan bütün sınıflamalar (çağrışım yanıtlarının ilişki türü, başlıkların son ögesi, sürçme örneklerinin üretim düzeyi) tek kodlayıcıya dayanmaktadır ve kodlayıcılar arası uyum hesaplanmamıştır. Bölüm 21'deki tez konu kodlaması da tek kodlayıcı tarafından ve yalnızca başlıklara dayanılarak yapılmıştır.

Ondalık değerler dosyalarda nokta ile, kitapta virgülle gösterilmiştir. `tablolar_ek_a.py` ve `tablolar_21.py` betiklerinin ürettiği `results/tablo_*.csv` dosyalarında hücreler kitaptaki biçimle (virgül) yazılır.

## Ek A

### A.1 Çocuk dilinde çekim ekleri (otomatik çözümleme)

Dosyalar: `ek_a/data/derived/a1_zeyrek_cozumlemeleri.json`, `ek_a/results/a1_results.json`, `ek_a/results/a1_island_child_results.json`.

* `a1_zeyrek_cozumlemeleri.json`: anahtar küçük harfe çevrilmiş sözcük yazılışı, değer Zeyrek 0.1.3'ün döndürdüğü çözümleme dizileri (`[lemma:POS] gövde:POS+ek:Etiket...`). Boş liste ya da `Unk` tanınmayan sözcük demektir.
* Kesitler: `Altınkamış (1;4-2;4)` (Turkay klasörü, tek çocuk); `Aksu 2;0-2;8` (yaş < 36 ay), `Aksu 3;0-3;8` (36-47 ay), `Aksu 4;0-4;8` (48 ay ve üzeri). Yaş, dosyanın CHAT `ID` başlık satırındaki çocuk yaşından alınır.
* Konuşucu: `CHI` çocuk; öteki bütün konuşucular yetişkin girdisi (`ADU`) sayılır.
* ZGK (zaman, görünüş, kip) ekleri (`tam`): `Prog1` -(I)yor, `Past` -DI, `Narr` -mIş, `Aor` geniş zaman, `Fut` -(y)AcAk, `Imp` emir kipi, `Opt` istek kipi -(y)A. Birleşik çekimlerde (ör. -(I)yordu) iki ek de sayılır. Bir belirteç yalnızca bütün aday çözümlemeleri aynı ZGK ekini ve aynı gövdeyi veriyorsa sayılır.
* Durum ekleri (`case`): `Nom` yalın, `Acc` belirtme, `Dat` yönelme, `Loc` bulunma, `Abl` ayrılma, `Gen` ilgi, `Ins` vasıta. Yalnızca bütün adayların aynı durumu verdiği ad belirteçleri sayılır.
* Ölçüler: `children` (konuşucu adına göre farklı çocuk), `files` (oturum), `utts` (söyleyiş), `tokens` (sözcük belirteci), `known` (çözümleyicide tanınan belirteç payı), `mlu_w` (söyleyiş başına sözcük), `morph_per_word` (tanınan sözcük başına biçim birimi = 1 + açık ek sayısı), `verb_tokens` ve `verb_lemmas` (çekimli fiil belirteci ve ayrı fiil), `overt_per_verb`, `tam_types` (kullanılan ZGK eki türü, en çok 7), `rho_tam` ve `rho_case` (çocuk ve yetişkin sıklık sıralamaları arasında Spearman katsayısı).
* Fiil adacığı sınaması (`island`; çocuk düzeyinde `a1_island_child_results.json`): çocuğun en az 4 kez kullandığı ve yetişkin girdisinde en az aynı sayıda geçen her fiil için çocuğun ayrı çekimli biçim sayısı (`child`) ile girdiden yerine koymadan eşit sayıda çekilen belirteçlerdeki ayrı biçim sayısının 500 yinelemedeki ortalaması (`adult`). `pairs` çocuk-fiil çifti, `gt`/`lt` çocuğun girdiden çok ya da az biçim kullandığı çift sayısı, `sign_p` iki yönlü işaret sınaması, `children_gt`/`children_lt` çocuk ortalamasının girdiden yüksek ya da düşük olduğu çocuk sayısı. `per_child` anahtarları kesit içi takma kimliklerdir (K01, K02, ...); CHILDES'taki çocuk adları yayımlanan dosyada yer almaz. `adult_mean_range_seeds2_21` 20 farklı tohumla eşitlenmiş girdi ortalamasının aralığıdır.

### A.2 Kurbağa öyküleri (elle sınıflama; veri ve betik depoda yok)

Ek A metnindeki ölçütler: hareket fiilleri Talmy'nin (1985) ayrımına göre yol fiilleri (path; *çık-*, *in-*, *gir-*, *düş-*, *kaç-*; *fall*, *escape*, *leave*) ve biçim fiilleri (manner; *koş-*, *uç-*, *tırman-*, *atla-*; *run*, *climb*, *fly*, *crawl*) olarak iki kümeye ayrılmıştır. İngilizcede hareket fiilinden sonraki iki sözcük içindeki yön ögeleri (*out*, *down*, *up*, *into*, *off*) sayılmıştır. Türkçe yüklemlerde zaman ve kanıtsallık eki yüklemin son zaman ekine göre (-mIş, -(I)yor, -DI, öteki) kodlanmış; bir anlatının "ağırlıklı eki" yüklemlerin en az yarısını oluşturan ektir, yoksa "karma". Sayımlar anlatı başınadır ve anlatı uzunluğuna göre düzeltilmemiştir.

### A.3 Ekli sözcüklerde gövde ve ek sıklığı

Dosyalar: `ek_a/results/a3_grid.json`, `ek_a/results/a3_forms.json`.

* `grid`: 7 ad (*ev*, *köy*, *yol*, *okul*, *kitap*, *kapı*, *araba*) × 11 çekim hücresi için alt yazı derlemindeki ham sıklık. Hücre sırası `cells` alanındadır: `yalın`, `-lAr`, `-(y)A`, `-DA`, `-DAn`, `-(I)m`, `-lArDA`, `-lArIndA`, `-(I)mIz`, `-(I)mDA`, `-lArImIzDAn`; `nsuf` her hücrenin ek sayısıdır.
* `N` ve `types`: listenin toplam sözcük ve farklı yazılış sayısı. `R2`, `stem`, `cell`: log10(f + 1) için toplamsal (ad + hücre) modelin açıkladığı varyans ve bunun ad ile hücre bileşenlerine düşen payı. `W`: hücre sıralamalarının adlar arasındaki Kendall uyum katsayısı. `cm`: hücre ortalamaları.
* `a3_forms.json`: her ad için Zeyrek'in o adın çekimli ad biçimi saydığı (türetme eki taşımayan) yazılışların sayısı (`types`), belirteç toplamı (`tokens`), belirteçlerin yüzde 90'ını karşılayan biçim sayısı (`k90`), en çok iki kez geçen biçim sayısı ve payı (`low`, `lowshare`), en sık 5 biçim (`top`) ve en uzun biçim (`maxsuf`).

### A.4 Çağrışım ve eş dizim (elle kodlanmış ilişki türü)

Dosyalar: `ek_a/results/a4_results.json`, `ek_a/data/derived/yapici2015_secilen_uyaricilar.tsv`, `ek_a/data/derived/tud_esdizim_ozet.tsv`.

* `yapici2015_secilen_uyaricilar.tsv`: `liste` ve `no` (tezdeki uyarıcı listesi ve yorum bölümündeki sıra), `uyarici`, `tr1`-`tr3` (Türkçe katılımcıların en sık 1., 2. ve 3. yanıtı; eşit sıklıktaki yanıtlar `/` ile ayrılır), `pdf_page`.
* `tud_esdizim_ozet.tsv`: `uyarici`, `tud_yazili_siklik` (uyarıcının yalın biçiminin TUD yazılı bölümündeki sıklığı), `esdizim_listesi_uzunlugu` (2.500), `en_dusuk_LL` (listenin son girdisinin log-olabilirlik değeri), `en_guclu_4_icerik_esdizimi` (işlev sözcükleri ve uyarıcının kendisi çıkarıldıktan sonra listenin başındaki 4 içerik sözcüğü; Tablo A.5'in son sütunu).
* `a4_results.json` (her satır bir uyarıcı-yanıt çifti): `uyarici`, `sira` (yanıtın çağrışım deneyindeki sırası: 1, 2, 3), `yanit`, `tur` (ilişki türü, aşağıda), `F` (uyarıcının derlem sıklığı), `rank` (yanıt sözcüğünün biçimlerinden eş dizim listesinde en üstte yer alanın sırası; listede yoksa `null`), `form` (o biçim), `o` (gözlenen birlikte geçme sıklığı), `ld` (logDice).
* İlişki türü (`tur`; kitapta parantez içindeki harf):
  * `P` = dizisel (paradigmatic, kitapta **D**): eş anlam, karşıt anlam, aynı ulamın üyeliği, üst ya da alt kavram, parça-bütün.
  * `S` = dizimsel (syntagmatic, kitapta **M**): uyarıcıya sıfat ya da fiil olarak bağlanıp onunla öbek kurabilen yanıt.
  * `T` = tematik (kitapta **T**): aynı durum ya da sahnede yer alan, değer ya da duygu bildiren yanıt.
* Dışlama: *anne* ve *para* uyarıcılarına verilen iki sözcüklü *her şey* yanıtı eş dizim listesinde sınanamadığından çözümleme dışıdır. Ortanca sıra hesaplanırken listede bulunmayan yanıtlar 2.501. sıraya konur.

### A.5 Geçici yapısal belirsizlik

**IMST (kurala bağlı, otomatik).** Dosya: `ek_a/results/a5_results.json`.

* `all`: belirtme durumlu nesnelerin (Case=Acc, NOUN/PROPN/PRON, `obj` bağı, başı VERB ya da AUX) bağlandığı fiilin yapı türüne göre sayısı. Ulamlar: `çekimli yüklem` (VerbForm=Fin ya da VerbForm yok); `ilgi cümleciği (sıfat-fiil)` (VerbForm=Part ve fiil bir ada `acl`, `amod` ya da `nmod` bağıyla bağlı); `sıfat-fiil (öteki)` (öteki VerbForm=Part); `ad-fiil tümleci` (VerbForm=Vnoun); `zarf-fiil` (VerbForm=Conv).
* `after_nom`: cümlede kendisinden önce yalın durumlu bir özne (`nsubj`) bulunan nesneler için aynı dağılım.
* `amb`: yüzey biçimi -mIş ya da -(y)AcAk ile biten fiillerin (VERB/AUX) dağılımı: `çekimli yüklem`, `ad niteleyen sıfat-fiil` (Part ve `acl`/`amod`), `öteki sıfat-fiil`, `öteki`.

**Gazete başlıkları (otomatik çözümleme ve elle denetim).** Dosya: `ek_a/data/derived/manset_kodlar.tsv` (568 satır, başlık metni yok).

| Değişken | Açıklama |
|---|---|
| `id` | Başlık kimliği: `tarih|gazete|başlık` dizgesinin SHA-1 özetinin ilk 12 onaltılık karakteri |
| `tarih` | Sayının tarihi (YYYY-AA-GG) |
| `gazete` | Hürriyet, Sabah, Milliyet |
| `duzey` | `manşet` (sayfadaki en büyük puntolu başlık) ya da `diğer` (öteki haber başlıkları). Spotlar çözümleme dışıdır |
| `sayfa_sira` | Başlığın aynı sayfanın aktarılan satırları içindeki sırası (spotlar dahil, 1'den başlar) |
| `kaynak_url` | Sayfa görüntüsünün okunduğu haber7.com galerisi |
| `son_oge_oto` | Zeyrek çözümlemesine dayanan otomatik sınıf: `F` çekimli fiil; `F?` çekimli fiil ya da yalın ad olabilen son sözcük; `K` ek-fiil ya da *var*, *yok*, *değil*; `N` yalın ya da iyelik ekli ad; `N?` çözümlenemeyen; `D:<durumlar>` yalnız durum ekli okunuşu olan ad; `N/D:<durumlar>` hem yalın hem durum ekli okunabilen ad |
| `son_oge` | Elle denetlenmiş son sınıf (Tablo A.8): `F` çekimli fiil; `K` ek-fiil ya da *var*, *yok*, *değil*; `D` durum ekli ad (yüklemi düşmüş); `N` yalın ya da iyelik ekli ad. Kurallar: `F?` → `F`, `N/D` → `N`, `D:*` → `D`; bu kuralların dışında kalan 30 karar `elle_duzeltme` ile işaretlidir |
| `elle_duzeltme` | 1: son sınıf `a5_manset_final.py` içindeki `OV` listesinden elle verildi |
| `soru` | 1: başlık soru eki ya da soru işaretiyle bitiyor |
| `ic_fiil` | 1: son sözcükten önce otomatik olarak çekimli fiil sayılan bir sözcük var |
| `tirnak` | 1: başlık tırnak işaretiyle başlıyor (alıntı başlık) |
| `n_sifatfiil_aday` | Son sözcükten önce yalnızca sıfat-fiil okunuşu olan sözcük sayısı (otomatik aday) |
| `n_belirtme_aday` | Son sözcükten önce belirtme durumu okunuşu olan sözcük sayısı (otomatik aday; belirtme ile iyelik arasında belirsiz biçimler dahil) |

Elle sınıflama ilkeleri: çözümleyicinin ad ile fiil arasında karar veremediği son sözcükler (*tepki*, *savunma*, *gelir* gibi) ve hitap sözcüğüyle biten başlıklar elle sınıflandırılmış; çözümsüz kalan son sözcükler ad satırında sayılmış; son sözcüğü belirtme ile iyelik eki arasında belirsiz kalan 73 başlık yalın ya da iyelik ekli ad satırına alınmıştır. Başlıklarda belirtme durumlu nesnelerin bağlandığı yüklem (Ek A metnindeki 67 nesne) de elle belirlenmiştir; bu satır düzeyindeki kodlama pakete aktarılmamıştır (bkz. README).

### A.6 Konuşma akıcısızlıkları ve hizalanma

**Altıparmak (2015) ortancaları.** Dosya: `ek_a/data/derived/altiparmak2015_ortancalar.csv`. `akicisizlik_turu` (dolu durak, tereddüt, uzatma, yanlış başlangıç, dil sürçmesi, tekrar; tanımlar Ek A'dadır), `kosul` (hazırlıksız ya da hazırlıklı konuşma), dört yaş grubunun 100 sözcükteki ortanca sıklığı (4-8 yaş grubundan hazırlıklı konuşma toplanmamıştır), `p_kruskal_wallis` (tezde bildirilen değer), `kaynak_sayfa`. Grup büyüklükleri: 4-8 yaş 14, 18-23 yaş 14, 33-50 yaş 28, 50 yaş üzeri 28 konuşucu.

**Sürçme ve onarım örnekleri (elle kodlama).** Dosya: `ek_a/data/derived/tablo_A10_surcme_kodlari.tsv`. `soyleyis` (tezde verilen örnek; köşeli ayraç konuşucunun bıraktığı başlangıcı, kısa çizgi yarıda kesilen sözcüğü gösterir), `konusucu_yasi`, `hedef_bicim`, `sapma_turu`, `etkilenen_duzey`, `kaynak`. Etkilenen düzey ulamları, Levelt (1989) ve Dell (1986) modellerinin üretim aşamalarına göre: `Ses bilimsel kodlama`; `Biçim bilimsel kodlama`; `Sözcük seçimi ile ses biçimi arası`; `Sözcük biçimine erişim`; `Sözcük seçimi, izleyici`; `Kavramlaştırma, izleyici`. Örnekler sıklık hesabı için değil kuramların sınıflamalarını göstermek için seçilmiştir.

**Hizalanma (otomatik).** Dosyalar: `ek_a/results/a6_results.json`, `ek_a/results/a6_cluster_results.json`.

* Yön ve süzgeç anahtarları: `AC` yetişkin söyleyişini izleyen çocuk söyleyişi; `CA` çocuk söyleyişini izleyen yetişkin söyleyişi; `AC_q` önceki yetişkin söyleyişi soru; `AC_s` önceki yetişkin söyleyişi soru değil; `AC_lag` 1-12 söyleyiş uzaklıktaki yetişkin söyleyişleri. İkinci düzey anahtar kesit, üçüncü düzey uzaklıktır (`"1"` hemen önceki söyleyiş).
* Ölçüler: `form` en az bir ortak sözcük biçimi; `lemma` son çekimli fiillerin gövdesi aynı (iki söyleyişte de çekimli fiil varsa); `tam` son çekimli fiillerin ZGK eki aynı; `tam_dl` gövdeler farklıyken ZGK eki aynı.
* Her ölçü için `n` çift sayısı, `k` gözlenen eşleşme, `E` taban çizgisi beklentisi toplamı, `V` Poisson-binom varyansı (Σp(1 − p)), `obs` = k/n, `base` = E/n. Taban çizgisi: aynı oturumda hedef söyleyişten en az 10 söyleyiş uzaktaki kaynak konuşucu söyleyişlerinden 40'ı rastgele seçilip ölçünün bu söyleyişlerdeki ortalaması alınır (tohum 7).
* Soru söyleyişi: CHAT çeviri yazısında soru işaretiyle ya da `+/?`, `+..?` bitiş işaretiyle biten söyleyiş. Yetişkin rolleri: Investigator, Mother, Adult, Father, Grandmother, Grandfather, Uncle, Aunt, Teacher.
* `a6_cluster_results.json`: soru olmayan yetişkin söyleyişinden sonra gövde farklıyken ZGK eki eşleşmesi için `pairs`, `children`, `obs`, `base`, `diff` (yüzde puan), `z_independent` (bağımsız çiftler varsayımı), `z_cluster` (çocuk düzeyinde kümeye dayanıklı sandviç varyansı, C/(C − 1) düzeltmesi), `boot_ci95` (çocuklar yerine koyarak 5.000 kez yeniden örnekleme, tohum 11).

### A.7 Şaşırtıcılık ve okuma süresi

Dosya: `ek_a/results/a7_results.json`. `n_items` çözümlemedeki sözcük, `n_all` metinlerdeki sözcük, `readers`, `texts`, `r2_base` temel modelin (uzunluk, Zipf sıklığı, önceki sözcüğün uzunluğu ve sıklığı) R². `models` her XGLM büyüklüğü için şaşırtıcılık katsayısı `b` (ms/bit), `se`, `p`, önceki sözcüğün şaşırtıcılığı için `b_prev`, `se_prev`, `p_prev` ve eklenen iki terimin açıkladığı ek varyans `dr2`. `quad` karesel terim; `mixed` okur için rastgele kesişimli karma model (564M); `bins` Şekil A.4a'daki şaşırtıcılık aralıkları (aralık ortalaması `s`, ortalama ilk geçiş süresi `gaze`, `sd`, `n`); `corr_len_s`, `corr_zipf_s` ilişki katsayıları; `multi_share` birden çok alt sözcük birimine bölünen sözcük payı. Şaşırtıcılık değerleri doğal logaritmadan bit birimine çevrilmiştir. Bağımlı ölçü sözcüğün okurlar arasındaki ortalama ilk geçiş süresidir (`firstrun.dur`); dışlama: metnin ilk sözcüğü, noktalama taşıyan sözcükler, wordfreq listesinde bulunmayan sözcükler, ilk geçişte ondan az okurun baktığı sözcükler.

## Bölüm 21

### YÖK tez kayıtları

Dosya: `bolum_21/data/raw/yok/yoktez_tum_kayitlar.csv` (167 kayıt, tez numarasıyla tekilleştirilmiş).

| Değişken | Açıklama |
|---|---|
| `no` | YÖK tez numarası |
| `yil` | Tezin yılı |
| `tur` | Yüksek Lisans, Doktora, Tıpta Uzmanlık |
| `dil` | Tez dili |
| `uni` | Üniversite (YÖK kaydındaki ad) |
| `konu` | YÖK konu alanları (`;` ile ayrılmış) |
| `baslik` | Özgün tez başlığı |
| `terim` | İlk sayımda özgün başlıkta saptanan arama terimleri (Bölüm 21'deki başlık sayımı `tez_tablo.py` içindeki düzenli ifadelerle yeniden yapılır) |
| `ilgi` | Kapsam kararı: `ilgili`; `ilgisiz-A` ("psycholinguistic" ya da "psikolinguistik" sözcüğünü bir ölçeğin dil ve kültür uyarlaması anlamında kullanan, çoğu hemşirelik ve halk sağlığı alanından tezler, 20 kayıt); `ilgisiz-B` (edebiyat, psikoterapi, bilgisayar mühendisliği gibi dil ile zihin ilişkisini konu edinmeyen tezler, 13 kayıt) |
| `sorgular` | Kaydı döndüren arama terimleri (`;` ile ayrılmış; Tablo 21.4) |

İkinci okumadaki kapsam kararları betiklerdeki `EXC`, `DUP` ve `NORM` kümeleriyle uygulanır: kişisel gelişim yöntemi olarak nörolinguistik programlama, psikanaliz, emojiler, ana dili eğitiminin kişilik gelişimine etkisi, öğretim programı ve öğretim yöntemi değerlendirmesi, öğrenme platformu kullanımı ve çeviri eğitimi üzerine 8 tez ile yurt dışındaki üniversitelerde yazılıp YÖK'e kaydedilmiş 3 tez (`EXC`; bir numara aynı zamanda yinelenen kayıttır); aynı tezin ikinci numarası (`DUP`, 2 durum); Yüzüncü Yıl ve Van Yüzüncü Yıl üniversitelerinin tek kurum sayılması (`NORM`). Kırgızistan-Türkiye Manas Üniversitesi kapsamda tutulmuştur. Sonuç: 121 tez.

`yoktez_ilgisiz.csv`: kapsam dışı 33 kaydın `no`, `yil`, `tur`, `konu`, `baslik`, `ilgi` alanları. `ham/q_*.tsv`: her terimin ham arama sonucu (tez numarası, yıl, tür kısaltması, dil, üniversite, konu, başlık).

### Tez konu kümeleri

Dosyalar: `bolum_21/data/derived/tez_kod_oto.json` (yalnız kurallar), `bolum_21/data/derived/tez_kod.json` (kurallar ve elle düzeltmeler; `kod` tez numarası → küme, `lab` küme adları).

Kodlama `tez_kod.py` içindeki anahtar sözcük kurallarının tez başlığına sırayla uygulanmasıyla yapılır; ilk eşleşen kural kodu belirler, hiçbiri eşleşmezse `DIG` verilir. Kuralların belirsiz kaldığı 20 tez elle denetlenmiş, 19'unun kodu değiştirilmiştir (`OV`).

| Kod | Küme | Kural sırası |
|---|---|---|
| `BOZ` | Dil ve iletişim bozuklukları | 1 |
| `SIN` | Nörodilbilim ve fizyolojik ölçümler | 2 |
| `IKI` | İki dillilik | 3 |
| `L2` | İkinci dil edinimi ve yabancı dil öğrenimi | 4 |
| `EDI` | Birinci dil edinimi ve çocuk dili | 5 |
| `SOZ` | Sözcük tanıma, biçim bilimi ve okuma | 6 |
| `CUM` | Cümle ve söylem işlemleme | 7 |
| `URE` | Dil üretimi | 8 |
| `ANL` | Anlam, kavram ve dil ile düşünce | 9 |
| `DIG` | Kuramsal, tarihsel ve sınır çalışmaları | (kalan) |

### OpenAlex konu grupları (kurala bağlı)

Dosyalar: `bolum_21/data/derived/kod2.json` (`id` OpenAlex kimliği, `kod` grup), `bolum_21/results/ozet2.json`.

Kurallar `oa_key_kod.py` içinde sırayla uygulanır:

1. **Başlık kuralı.** Başlıkta `COMP_TERMS` listesindeki bir hesaplama terimi geçen kayıt (natural language processing, NLP, machine learning, deep learning, neural network(s), BERT, transformer(s), large language model(s), LLM(s), language model(s), sentiment, chatbot(s), text classification, speech recognition, artificial intelligence, word embedding(s), text mining, convolutional, LSTM; büyük-küçük harf duyarsız, sözcük sınırıyla) `M` grubuna alınır. İstisna: birincil konusu çekirdek kümesinde olup başlığında `PSY_MARKERS` (aphasia, acquisition, bilingual, reading, child ve Türkçe karşılıkları afazi, edinim, iki dilli, okuma, çocuk) geçen kayıt çekirdekte kalır.
2. `P` **Dil psikolojisi ve dil bozuklukları (çekirdek):** birincil konu (primary topic) şunlardan biri: Neurobiology of Language and Bilingualism; Language Development and Disorders; Reading and Literacy Development; Second Language Acquisition and Learning; Categorization, perception, and language; Phonetics and Phonology Research; Syntax, Semantics, Linguistic Variation; Hemispheric Asymmetry in Neuroscience; Hearing Impairment and Communication.
3. `E` **Dil öğretimi ve eğitim:** konu EFL/ESL Teaching and Learning, English Language Learning and Teaching, Multilingual Education and Policy, Second Language Learning and Teaching ya da Education and experiences of immigrants and refugees; ya da alt alan Education; ya da Social Sciences alanında adında Education geçen konu.
4. `M` **Bilgisayar bilimi ve mühendislik:** alan Computer Science, Engineering, Mathematics ya da Decision Sciences; ya da alt alan Health Informatics, Health Information Management.
5. `N` **Tıp ve sağlık:** alan Medicine, Neuroscience, Health Professions, Nursing, Biochemistry, Genetics and Molecular Biology, Pharmacology, Toxicology and Pharmaceutics, Immunology and Microbiology, Dentistry; ya da alt alan Clinical Psychology.
6. `O` **Diğer:** kalan kayıtlar.

`ozet2.json` alanları: `toplam` tekil kayıt, `indirilen_satir`, `yinelenen`, `gecis_v1_v2` (başlık kuralının grup değiştirdiği kayıtlar), `gruplar` (her grup için `n`, dönem sayıları `a` 1936-2009, `b` 2010-2019, `c` 2020-2026 ve `ortanca_atif`), `eksik_yillar` (sunucu sayımı ile indirilen kayıtlar arasındaki fark), `karsilastirma` (elle kodlanmış ön tarama kesitiyle uyum: eşleşen kayıt, uyum yüzdesi, Cohen kappa, kesinlik, duyarlık, karışıklık matrisi), çekirdek kayıtların kurum, ülke, dil, tür ve kaynak dağılımları, `en_cok_atif` (OpenAlex'in 2 Kasım 2026'daki atıf sayılarına göre ilk 15 çekirdek kayıt), `donem` (dünya ve Türkiye dönem sayımları ve paylar).

### Ön tarama elle kodlaması

Dosya: `bolum_21/data/derived/on_tarama_kod.json` (`i` ön tarama kaydının yıla göre sıralanmış listedeki sırası, `kod`). Normalleştirilmiş başlıkla tekilleştirilen 208 kayıt başlık ve özetlerine göre tek kodlayıcı tarafından kodlanmıştır:

| Kod | Ulam |
|---|---|
| `P` | Dil psikolojisi araştırmaları |
| `K` | Afazi ve dil bozukluklarında dil bilimsel ve terapi çalışmaları (karşılaştırmada `P` ile birleştirilir) |
| `N` | Tıbbi olgu ve tedavi çalışmaları |
| `E` | İkinci dil öğretimi ve dil eğitimi |
| `M` | Doğal dil işleme, konuşma ve işaret tanıma |
| `O` | Diğer (ölçek uyarlama, odyoloji, deneme) |
