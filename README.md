# PLTS Ground Mount 2,75 kWp — Gambar Kerja Teknik

Repositori ini berisi **gambar kerja teknik (construction drawings)** untuk instalasi
Pembangkit Listrik Tenaga Surya (PLTS) tipe **ground mount** berskala **2,75 kWp**,
tersusun dari **5 modul surya 550 Wp** (dimensi **1990 × 1130 × 35 mm**) yang dipasang
vertikal (portrait) dengan **kemiringan 15° menghadap utara**. Seluruh lembar digambar
pada kertas **A3** dengan skala **1:25 (tampak) / 1:20 (potongan) / 1:5 (detail)**,
lengkap dengan kop standar, dimensi, arah utara, legenda garis, catatan teknis, dan
Bill of Material (BOM).

Gambar ini merupakan penyempurnaan dari draft awal (tersimpan di folder
`draft-original/`) — teks yang rusak telah diperbaiki, dimensi antar tampak
diserasikan, dan geometri disesuaikan dengan modul 550 Wp sesungguhnya.

## Riwayat Revisi

| Revisi | Isi Perubahan |
|--------|---------------|
| **0** | Penyempurnaan draft awal → gambar kerja A3 lengkap (skala 1:100) |
| **1** | Gambar diperbesar menjadi 1:25 / 1:20 agar dominan dan mudah dibaca |
| **2** | Revisi teknis sesuai instruksi pemilik proyek: modul 1990 × 1130 mm; balok kaki rangka tinggi **30 cm** di atas lantai kerja; sloof tinggi **25 cm** di atas lantai kerja; pondasi batu kali **4 titik** dengan kedalaman **30 cm di bawah tanah asli**; kaki tengah (sumbu 2) **tanpa pondasi batu kali** — tumpuan langsung pada sloof; **semua tampak atas menampilkan panel secara tersembunyi (disamarkan)** agar rangka, balok kaki, sloof, pembesian, dan plat angkur terlihat jelas |

## Daftar Lembar Gambar

| No. | Judul Lembar | Isi Utama |
|-----|--------------|-----------|
| G-01 | TAMPAK ATAS (PANEL DISAMARKAN) | Denah umum 5650 × 1922 mm — rangka + sloof + balok kaki + pondasi terlihat, modul hanya proyeksi putus-putus; BOM, catatan, legenda |
| G-02 | TAMPAK DEPAN | Elevasi depan: balok kaki +0,30, sloof +0,25, pondasi 4 titik + **DETAIL A-1 / A-2 (1:5)** sambungan plat 5 mm & dynabolt M12 |
| G-03 | TAMPAK SAMPING (POTONGAN A-A) | Potongan sumbu 2: kaki tengah langsung di atas sloof; proyeksi putus-putus pondasi & balok kaki (sumbu 1 & 3); kemiringan 15°, tinggi kaki |
| G-04 | TAMPAK ATAS — RANGKA PANEL | Denah rangka baja (panel disamarkan) + daftar batang (cut list) |
| G-05 | TAMPAK ATAS — RANGKA & STRUKTUR BETON | Rangka + sloof + balok kaki + pondasi 4 titik + balok ikat |
| G-06 | TAMPAK ATAS — STRUKTUR BETON & ANGKUR | Denah beton murni: sloof, balok ikat, balok kaki 30 × 30, pondasi 4 titik, plat + dynabolt |

### Skala Gambar

| Lembar | Skala |
|--------|-------|
| G-01, G-04, G-05, G-06 (tampak atas) | **1 : 25** |
| G-02 (tampak depan) | **1 : 25** |
| G-03 (potongan A-A) | **1 : 20** |
| DETAIL A-1 / A-2 (sambungan kaki, pada G-02) | **1 : 5** |

File per lembar tersedia dalam tiga format: **SVG** (vektor, dapat diedit di
Inkscape/Illustrator), **PNG** (220 dpi, untuk presentasi), dan satu **PDF**
gabungan 6 halaman (vektor, siap cetak).

## Spesifikasi Teknis Ringkas (Revisi 2)

| Komponen | Spesifikasi |
|----------|-------------|
| Array | 5 × modul 550 Wp = **2,75 kWp**, orientasi portrait |
| Modul surya | **1990 × 1130 × 35 mm** per unit |
| Jejak rencana | **5650 mm** (barat–timur) × **1922 mm** (utara–selatan, proyeksi 1990·cos 15°) |
| Kemiringan | **15°** menghadap utara |
| Sumbu rangka | Sumbu 1-2-3 pada 550 / 2825 / 5100 mm dari tepi barat (jarak antar sumbu **2275 mm**); kantilever rail 550 mm |
| Kaki rangka | **6 titik**: sumbu 1 & 3 alas pada balok kaki (**+0,30**); sumbu 2 (tengah) alas langsung pada sloof (**+0,25**) → kaki tengah 50 mm lebih panjang |
| Panjang batang kaki | Depan: 2 × 1,040 m + 1 × 1,090 m; belakang: 2 × 1,305 m + 1 × 1,355 m; tinggi rail atas ±1135 / ±1400 mm di atas puncak sloof; jarak horizontal antar baris 990 mm |
| Rangka | Baja hollow galvanis **40 × 20 mm** tebal min. 1,6 mm, sambungan dilas |
| **Balok kaki rangka** | Beton K-225 **30 × 30 cm**, tinggi **+0,30 m di atas lantai kerja**, **4 bh** (sumbu 1 & 3), berdiri di atas pondasi batu kali |
| Sloof & balok ikat | Beton **300 × 250 mm** mutu **K-225**, tinggi **+0,25 m di atas lantai kerja** (2 sloof memanjang + 3 balok ikat), tulangan Ø8 sengkang @15 cm, monolit |
| Pondasi | **Batu kali 1:5, hanya 4 titik** (sumbu 1 & 3, baris A & B) — lebar atas 30 cm, bawah 60 cm, **kedalaman 30 cm di bawah tanah asli**; kaki tengah tanpa pondasi batu kali (tumpuan hanya sloof) |
| Lantai kerja | Beton K-100 tebal 10 cm di sekeliling struktur (elevasi ±0,00) |
| Angkuran | Plat besi 5 mm (100 × 100 mm) + **4 dynabolt M12** per titik kaki (4 titik di balok kaki, 2 titik langsung di sloof) |
| Peralatan | Box panel control IP65 400 × 300 × 200 mm pada rangka tengah |

> **Catatan kop gambar**: kolom *Nama Proyek*, *Lokasi*, tanggal, dan kolom tanda
> tangan (Dibuat/Diperiksa/Disetujui) sengaja dikosongkan — silakan diisi sesuai
> identitas proyek Anda.

## Struktur Repositori

```
SolarPumpProject/
├── README.md                 # dokumen ini
├── worklog.md                # catatan proses penyempurnaan dari draft
├── requirements.txt          # dependensi Python
├── gambar-kerja/             # 13 file hasil akhir (6 SVG + 6 PNG + 1 PDF)
├── scripts/                  # generator gambar (Python, reproducible)
│   ├── design.py             # SEMUA parameter desain di sini (single source of truth)
│   ├── svgcad.py             # pustaka CAD mini untuk SVG (dimensi, arsir, kop, simbol)
│   ├── sheets_plan.py        # generator lembar G-01, G-04, G-05, G-06
│   ├── sheets_elev.py        # generator lembar G-02, G-03
│   ├── build.py              # perakit: SVG -> PNG (220 dpi) -> PDF gabungan
│   └── validate_bounds.py    # validator: teks keluar bingkai lembar
└── draft-original/           # 6 file SVG draft awal (sebelum penyempurnaan)
```

## Cara Regenerasi / Revisi Gambar

Seluruh gambar dihasilkan secara **programatik dan deterministik** — mengubah
parameter lalu menjalankan ulang skrip akan menghasilkan seluruh 6 lembar secara
konsisten (dimensi, BOM, catatan ikut ter-update otomatis).

```bash
# 1. Install dependensi
pip install -r scripts/requirements.txt

# 2. (Opsional) ubah parameter desain — semua di scripts/design.py
#    contoh: N_MOD, TILT, MOD_L/MOD_W, SLOOF_H, PAD_TOP, dsb.

# 3. Bangun ulang semua lembar -> folder gambar-kerja/
python3 scripts/build.py

#    atau arahkan ke folder lain:
PLTS_OUT=/path/ke/output python3 scripts/build.py

# 4. (Opsional) validasi tidak ada teks keluar bingkai A3
python3 scripts/validate_bounds.py "gambar-kerja"
```

Contoh revisi yang umum:
- **Mengubah kemiringan**: ubah `TILT` di `design.py` → tinggi kaki, proyeksi,
  dan sudut pada semua tampak terhitung otomatis.
- **Mengubah jumlah modul**: ubah `N_MOD` → panjang array, BOM, dan denah ikut berubah.
- **Mengubah dimensi modul**: ubah `MOD_L` / `MOD_W` (mis. 1990 × 1130) → jejak
  rencana, posisi kaki, dan panjang batang terhitung ulang.
- **Menambah identitas proyek di kop**: edit fungsi kop di `svgcad.py` atau
  isi langsung SVG-nya di Inkscape.

## Bill of Material (BOM)

| No. | Material | Ukuran | Sat. | Qty |
|-----|----------|--------|------|-----|
| 1 | Modul surya 550 Wp | 1990 × 1130 × 35 mm | unit | 5 |
| 2 | Baja hollow galvanis 40 × 20 × 1,6 mm — rail memanjang | 2 × 5,65 m | m | 11,30 |
| 3 | Baja hollow galvanis 40 × 20 × 1,6 mm — kaki rangka | depan: 2×1,040 + 1×1,090; belakang: 2×1,305 + 1×1,355 | m | 7,14 |
| 4 | Baja hollow galvanis 40 × 20 × 1,6 mm — pengaku & braket box | 3 × 1,34 m + 2 × 0,35 m | m | 4,72 |
| 5 | Klem modul (tengah & ujung) + baut M8 | sesuai pabrikan modul | set | 24 |
| 6 | Plat besi alas kaki | 5 mm, 100 × 100 mm | pcs | 6 |
| 7 | Dynabolt / angkur ekspansi | M12 × 100 mm (4 bh/titik) | pcs | 24 |
| 8 | Beton sloof, balok ikat & balok kaki rangka | mutu K-225 | m³ | 1,10 |
| 9 | Pondasi batu kali (1 : 5) | atas 30, bawah 60, dalam 30 cm di bawah tanah | titik | **4** |
| 10 | Beton lantai kerja | K-100, tebal 10 cm | m³ | 2,00 |
| 11 | Besi beton polos Ø8 | tulangan + sengkang @15 cm | kg | 60 |
| 12 | Box panel control + dudukan | IP65 | unit | 1 |

## Perbaikan Utama dari Draft Awal

1. **Teks rusak diperbaiki** — huruf terpecah/tumpang tindih pada draft diubah
   menjadi teks utuh yang rapi dan konsisten.
2. **Dimensi antar tampak diserasikan** — draft memiliki angka berbeda antar
   lembar. Kini semua berasal dari satu basis desain (`design.py`).
3. **TAMPAK DEPAN diberi dimensi lengkap** — draft elevasi depan tanpa satu
   pun anotasi; kini berdimensi penuh + Detail A-1 / A-2 (1:5).
4. **Geometri sesuai modul nyata** — modul 550 Wp ukuran 1990 × 1130 mm sesuai
   spesifikasi pemilik proyek.
5. **Kelengkapan standar gambar kerja** — kop, skala, arah utara, satuan,
   legenda garis, catatan teknis, BOM, dan tanda potongan A-A.
6. **Struktur tumpuan jelas** — balok kaki rangka (+0,30) di atas pondasi batu
   kali 4 titik; kaki tengah di atas sloof (+0,25) tanpa pondasi batu kali.
7. **Visibilitas struktur pada tampak atas** — panel surya disamarkan (garis
   putus-putus) di semua tampak atas agar aplikator dapat membaca rangka,
   balok beton, sloof, pembesian, dan plat angkur.

## Referensi

- Instalasi kabel DC & pembumian mengikuti **PUIL 2011** (SNI 0225) dan
  petunjuk pabrikan modul.
- `worklog.md` — catatan lengkap proses pengerjaan.
