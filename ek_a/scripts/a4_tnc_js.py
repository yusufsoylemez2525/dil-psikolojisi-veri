# A.4 yardımcı betiği: Türkçe Ulusal Derlemi (TUD 3.0) web arayüzünde bir uyarıcının eş dizim sorgusu
# (yalın biçim, sağda ve solda 5'er sözcük, log-olabilirlik sırası, en güçlü 2.500 eş dizim) açıkken tarayıcı konsolunda
# çalıştırılacak JavaScript kodunu üretir. Kullanım: python3 a4_tnc_js.py <uyarıcı>  (ör. anne)
# Konsolun döndürdüğü metin ek_a/data/external/tnc_esdizim/<uyarıcı>.txt dosyasına kaydedilir. Ayrıntı: DATA_SOURCES.md.
import json, sys
P = {
 'beyaz': [('siyah','^siyah'),('ak','^ak$'),('temiz','^temiz(?!li)'),('temizlik','^temizli[kğ]')],
 'savaş': [('barış','^barış'),('ölüm','^ölüm'),('kan','^kan(ı|a|da|dan|ın|ını|lar|ları|larını|lı|ını)?$')],
 'gazete': [('haber','^haber'),('dergi','^dergi'),('okumak','^oku(?!l)')],
 'göz': [('görmek','^gör(?!ev|ün|üş|kem|gü)'),('organ','^organ(?!iz)'),('yeşil','^yeşil'),('kulak','^kula[kğ]')],
 'ses': [('müzik','^müzi[kğ]'),('gürültü','^gürültü'),('duymak','^duy(?!gu|ur|ar)')],
 'kız': [('erkek','^erke[kğ]'),('güzel','^güzel'),('bayan','^bayan')],
 'gün': [('zaman','^zaman'),('güneş','^güneş'),('gece','^gece')],
 'çocuk': [('bebek','^bebe[kğ]'),('sevimli','^sevimli'),('sevgi','^sevgi'),('mutluluk','^mutlulu[kğ]')],
 'iyi': [('kötü','^kötü'),('güzel','^güzel'),('melek','^mele[kğ]')],
 'ev': [('yuva','^yuva'),('huzur','^huzur'),('araba','^araba')],
 'arkadaş': [('dost','^dost(?!lu|oy)'),('kardeş','^kardeş'),('dostluk','^dostlu[kğ]')],
 'hayat': [('yaşam','^yaşam'),('ölüm','^ölüm'),('zor','^zor(u|a|da|dan|dur|du)?$'),('su','^su(yu|ya|da|dan|yun|lar)?$')],
 'kitap': [('okumak','^oku(?!l)'),('bilgi','^bilgi'),('dost','^dost(?!lu|oy)'),('edebiyat','^edebiyat')],
 'anne': [('sevgi','^sevgi'),('baba','^baba'),('can','^can(ı|a|ım|ını|lar|dan)?$'),('aşk','^aşk')],
 'genç': [('yaşlı','^yaşlı'),('dinamik','^dinami[kğ]'),('ergen','^ergen')],
 'el': [('yabancı','^yabancı'),('parmak','^parma[kğ]'),('ayak','^aya[kğ](?!kab)')],
 'masa': [('sandalye','^sandalye'),('yemek','^yeme[kğ]'),('tahta','^tahta')],
 'sabah': [('güneş','^güneş'),('uyku','^uyku'),('akşam','^akşam')],
 'para': [('güç','^(güç|gücü|güce|gücün|gücünü|güçlü)$'),('zenginlik','^zenginli[kğ]')],
 'ağaç': [('yeşil','^yeşil'),('orman','^orman'),('yaprak','^yapra[kğ]')],
}
w = sys.argv[1]
js = """(()=>{const pats=%s;
const t=[...document.querySelectorAll('table')].find(t=>t.id=='collocations' && $.fn.dataTable.isDataTable(t));
if(!t) return 'NO TABLE '+document.title;
const rows=$(t).DataTable().rows().data().toArray().map(r=>({w:r.teksozcuk.toLocaleLowerCase('tr'),o:+r.gozlenen_collocate_frekans,f:+r.derlemdeki_sayisi,ll:+r.loglikelihood,ld:+r.logdice}));
rows.sort((a,b)=>b.ll-a.ll); rows.forEach((r,i)=>r.rk=i+1);
const m=document.body.innerText.match(/Gözlenen sıklık\\s*([\\d.]+)/);
let out='Q '+document.body.innerText.match(/Arama\\s*\\n?\\s*(\\S+)/)?.[1]+' F '+(m?m[1]:'?')+' N '+rows.length+' minLL '+rows[rows.length-1].ll.toFixed(1)+'\\nTOP '+rows.slice(0,45).map(r=>r.w).join(' ')+'\\n';
for(const [nm,re] of pats){const R=new RegExp(re); const x=rows.filter(r=>R.test(r.w)).slice(0,6); out+=nm+' >> '+x.map(r=>r.rk+' '+r.w+' '+r.o+' '+r.f+' '+r.ll.toFixed(0)+' '+r.ld.toFixed(2)).join(' ; ')+'\\n';}
return out.replace(/[=&?]/g,' ');})()""" % json.dumps(P[w], ensure_ascii=False)
print(js)
