# A.5 yardımcı betiği: yeniden kurulan başlık dosyasının (data/external/manset/manset.tsv) satırlarını, depodaki
# başlık metni içermeyen kod dosyasıyla (data/derived/manset_kodlar.tsv) başlık kimliği üzerinden eşleştirir.
# Kimlik, "tarih|gazete|başlık" dizgesinin SHA-1 özetinin ilk 12 karakteridir (a5_manset.py, hid()).
# Eşleşmeyen satırlar, aktarımın kitaptaki aktarımdan harf, noktalama ya da büyük-küçük harf düzeyinde ayrıldığını gösterir.
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]  # depo kökü (dil-psikolojisi-veri/)
EKA = ROOT / 'ek_a'
EXT, WORK, DER = EKA / 'data' / 'external', EKA / 'data' / 'work', EKA / 'data' / 'derived'
import csv, hashlib, collections
def hid(r): return hashlib.sha1(f"{r['tarih']}|{r['gazete']}|{r['baslik'].strip()}".encode('utf-8')).hexdigest()[:12]
K = {r['id']: r for r in csv.DictReader(open(DER / 'manset_kodlar.tsv', encoding='utf-8'), delimiter='\t')}
R = [r for r in csv.DictReader(open(EXT / 'manset' / 'manset.tsv', encoding='utf-8'), delimiter='\t') if r['duzey'] != 'spot']
ids = {hid(r) for r in R}
print('kod dosyasındaki başlık', len(K), '| yeniden kurulan dosyadaki başlık (spot dışı)', len(R), '| eşleşen', len(ids & set(K)))
miss = collections.Counter((K[i]['tarih'], K[i]['gazete']) for i in set(K) - ids)
for (t, g), n in sorted(miss.items()): print('  eşleşmeyen:', t, g, n, 'başlık')
