# BUILD REPORT — news-image-20261122, slot 1

Built Sun 22 Nov 2026 ~07:45–09:00 WIB. Bounty open since 22 Nov 00:00 UTC,
deadline Tue 24 Nov 00:00 UTC (07:00 WIB). $100, top 50 paid (1st $20).
At build time: ~702 submissions; early dev leader @hazel-badger-99
"Honest Pulse" 961,867; most early entries are generic "Global Digest
Infographic" templates at 830–880k.

## Scope verdict: LAYAK, build selesai

- transcripts_required: true, **bukan** strict_transcripts (competition.yaml
  `submission_rule`: transcripts_required true, no strict flag) → jalur
  bundle normal, tidak ada blocker recording.
- Tidak butuh API key / wallet / akun apa pun untuk build.
- Metric: AI judge z-ai/glm-5.3-flash, pairwise, kriteria: (1) namai harinya
  + event spesifik hari itu, (2) seleksi & breadth, (3) terbaca, (4) faithful,
  (5) craft/legible ~300px.

## Entry: "The World in One Day" — Sunday 22 November 2026

Layout koran padat mengikuti pola pemenang hari sebelumnya (20 Nov slot 3
"D3" skor 990,422 #19; 21 Nov slot 1): 36 cerita, 7 region, 3 hero dengan
gambar orisinal, 10 panel bergambar, peta dunia bernomor, daftar ALSO 23
cerita, BY THE CLOCK, DATE CHECK box.

Heroes: (1) COP31 masih tanpa deal — talks lanjut ke Minggu, draft ke-3
ditunggu; (2) kapal kargo Rusia Sparta II terbakar di Teluk Finlandia
setelah dihantam 2 drone, 16 kru dievakuasi, Finlandia: kemungkinan Ukraina;
(3) IRGC klaim jatuhkan 2 drone AS di atas Hormuz/Qeshm.
Panels: El Chapo Isidro ditangkap (11 tewas), Estonia tutup perbatasan
1 Des, Bolsonaro ICU, Prancis minta aksi DK PBB soal Myanmar, bomber China
putar balik 170 km dari Manila, 4 tewas di Gaza, Modi resmikan Nitish Setu,
peringatan teror untuk maskapai AS, AS "open to" Sekjen PBB dari Belahan
Barat, 4 tewas kebakaran di Basra.
ALSO 14–36 termasuk Somalia usir dubes UEA, ~700.000 mengungsi di Ethiopia
selatan, 40 warga tewas di Cantine (Kongo), vonis 19 tahun N. Gupta,
Swedia panggil dubes Rusia, Hegseth batasi kerja sama keamanan dengan
Kanada, dan lain-lain. Detail + sumber tiap cerita di AUDIT.md.

Audit: semua cerita diverifikasi dari pelaporan live; yang DITOLAK sebagai
berita 22 Nov: serangan Iran ke pangkalan AS di Kuwait/Bahrain (18 Nov),
gempa Peru M6.9 (20 Nov lokal), trilateral Shenzhen (19 Nov), barrage Kyiv
+ misil di Polandia (20 Nov), koreksi Wall Street (20 Nov), plot Denmark
(20 Nov), IPO Anthropic + peluncuran GTA VI (19 Nov).

## Verifikasi

- `entry.png`: 1024×1024, 199.173 byte (< 1 MiB), PNG utuh.
- Determinisme: `compose.py` 2× run → sha256 identik
  `2654a2402c529015e81e3dbb90e900bdf408aa4d8cf1459e251f21ed79853590`.
- `main.py` (stdlib only, copy entry.png) 2× run → byte-identik dengan
  `entry.png`, sha256 sama.
- Visual check: layout terbaca, tidak ada teks terpotong/tertimpa setelah
  2 ronde perbaikan (stat strip, region strip, dot peta yang bertabrakan
  diberi leader line).

## File (siap submit; BELUM push, BELUM submit)

- `~/workspace/makefun-news-image-20261122/entry.png` (199.173 B)
- `~/workspace/makefun-news-image-20261122/main.py` (entrypoint stdlib)
- `~/workspace/makefun-news-image-20261122/compose.py` (renderer, ditulis
  dari nol di sesi ini)
- `~/workspace/makefun-news-image-20261122/README.md`, `LICENSE` (MIT),
  `AUDIT.md`, `BUILD-REPORT.md`
- File kerja (bukan bagian repo submit): `competition.json`, `rules.txt`,
  `kit/`, `kit.tar.gz`.

## Penilaian peluang — jujur

Peluang nyata masuk top 50, dengan kemungkinan top 20 kalau kualitas
dinilai setara D3 (990,422 #19 pada 20 Nov). Alasannya: (1) pola layout
yang sama sudah terbukti 2 hari berturut-turut; (2) 36 cerita terverifikasi
dengan breadth 7 region termasuk 3 cerita Afrika; (3) hero adalah 3 cerita
terbesar hari itu (COP31, Sparta II, Hormuz) — bukan template generik
seperti mayoritas 702 entry awal yang skornya 830–880k. Risiko utama:
hari masih muda saat build (00:45 UTC) — berita besar yang terjadi Minggu
siang/malam UTC belum masuk; dan final heat menilai ulang semua entry
fresh (provisional dev bukan jaminan). Slot 2 masih tersedia untuk grind
lanjutan kalau ada berita besar muncul sebelum deadline.
