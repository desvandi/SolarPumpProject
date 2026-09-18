# PLTS Ground Mount 2,75 kWp — Gambar Kerja Teknik

Repositori ini berisi **gambar kerja teknik (construction drawings)** untuk instalasi
Pembangkit Listrik Tenaga Surya (PLTS) tipe **ground mount** berskala **2,75 kWp**,
tersusun dari **5 modul surya 550 Wp** yang dipasang vertikal (portrait) dengan
**kemiringan 15° menghadap utara**. Seluruh lembar digambar pada kertas **A3 dengan
skala 1:100**, lengkap dengan kop standar, dimensi, arah utara, legenda garis,
catatan teknis, dan Bill of Material (BOM).

Gambar ini merupakan penyempurnaan dari draft awal (tersimpan di folder
`draft-original/`) — teks yang rusak telah diperbaiki, dimensi antar tampak
diserasikan, elevasi depan diberi anotasi lengkap, dan geometri disesuaikan dengan
modul 550 Wp sesungguhnya (2278 × 1134 mm).

## Daftar Lembar Gambar

| No. | Judul Lembar | Isi Utama |
|-----|--------------|-----------|
| G-01 | TAMPAK ATAS | Denah array 5670 × 2200 mm, garis sumbu rangka, arah utara, BOM, catatan teknis, legenda garis |
| G-02 | TAMPAK DEPAN | Elevasi depan dengan dimensi lengkap + **DETAIL A (1:5)** sambungan plat besi & dynabolt M12 |
| G-03 | TAMPAK SAMPING (POTONGAN A-A) | Potongan melintang: kemiringan 15°, tinggi kaki, sloof 30/25, pondasi batu kali, lantai kerja |
| G-04 | PANEL SURYA DISAMARKAN (RANGKA) | Denah rangka baja + daftar batang (cut list) |
| G-05 | PANEL DIHILANGKAN (RANGKA & BETON) | Rangka + sloof + pondasi + garis sumbu |
| G-06 | PANEL & RANGKA DISAMARKAN (BETON) | Denah beton murni: sloof, balok ikat, pondasi, lantai kerja |

File per lembar tersedia dalam tiga format: **SVG** (vektor, dapat diedit di
Inkscape/Illustrator), **PNG** (220 dpi, untuk presentasi), dan satu **PDF**
gabungan 6 halaman (vektor, siap cetak).

## Spesifikasi Teknis Ringkas

| Komponen | Spesifikasi |
|----------|-------------|
| Array | 5 × modul 550 Wp = **2,75 kWp**, orientasi portrait |
| Modul surya | 2278 × 1134 × 35 mm per unit |
| Jejak rencana | 5670 mm (barat–timur) × 2200 mm (utara–selatan, proyeksi 2278·cos 15°) |
| Kemiringan | **15°** menghadap utara |
| Kaki rangka | Depan ±1135 mm, belakang ±1400 mm dari puncak sloof; jarak horizontal antar baris 990 mm (sudut tepat 15,0°) |
| Sumbu rangka | Sumbu 1-2-3 pada 550 / 2835 / 5120 mm dari tepi barat (jarak antar sumbu 2285 mm); kantilever rail 550 mm — **6 titik kaki** |
| Rangka | Baja hollow galvanis **40 × 20 mm** tebal min. 1,6 mm, sambungan dilas |
| Sloof & balok ikat | Beton **300 × 250 mm** mutu **K-225**, +15 cm di atas lantai kerja, tulangan Ø8 sengkang @15 cm |
| Pondasi | **Batu kali 1:5, 6 titik** — lebar atas 30 cm, bawah 60 cm, kedalaman 50 cm di bawah sloof |
| Lantai kerja | Beton K-100 tebal 10 cm |
| Angkuran | Plat besi 5 mm (100 × 100 mm) + **4 dynabolt M12** per titik kaki |
| Peralatan | Box panel control IP65 400 × 300 × 200 mm pada rangka tengah (elevasi bawah +0,40) |

> **Catatan kop gambar**: kolom *Nama Proyek*, *Lokasi*, *No. Kontrak*, tanggal, dan
> kolom tanda tangan (Dibuat/Diperiksa/Disetujui) sengaja dikosongkan — silakan
> diisi sesuai identitas proyek Anda.

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
#    contoh: N_MOD, TILT, SLOOF_W/H, FOOT_DEPTH, dsb.

# 3. Bangun ulang semua lembar -> folder gambar-kerja/
python3 scripts/build.py

#    atau arahkan ke folder lain:
PLTS_OUT=/path/ke/output python3 scripts/build.py

# 4. (Opsional) validasi tidak ada teks keluar bingkai A3
python3 scripts/validate_bounds.py "gambar-kerja/G-01 TAMPAK ATAS.svg"
```

Contoh revisi yang umum:
- **Mengubah kemiringan**: ubah `TILT` di `design.py` → tinggi kaki, proyeksi,
  dan sudut pada semua tampak terhitung otomatis.
- **Mengubah jumlah modul**: ubah `N_MOD` → panjang array, BOM, dan denah ikut berubah.
- **Menambah identitas proyek di kop**: edit fungsi kop di `svgcad.py` atau
  isi langsung SVG-nya di Inkscape.

## Bill of Material (BOM)

| No. | Material | Ukuran | Sat. | Qty |
|-----|----------|--------|------|-----|
| 1 | Modul surya 550 Wp | 2278 × 1134 × 35 mm | unit | 5 |
| 2 | Baja hollow galvanis 40 × 20 × 1,6 mm — rail memanjang | 2 × 5,67 m | m | 11,34 |
| 3 | Baja hollow galvanis 40 × 20 × 1,6 mm — kaki rangka | 3 × 1,09 m + 3 × 1,36 m | m | 7,35 |
| 4 | Baja hollow galvanis 40 × 20 × 1,6 mm — pengaku & braket box | 6 × 1,34 m + braket | m | 5,30 |
| 5 | Klem modul (tengah & ujung) + baut M8 | sesuai pabrikan modul | set | 24 |
| 6 | Plat besi alas kaki | 5 mm, 100 × 100 mm | pcs | 6 |
| 7 | Dynabolt / angkur ekspansi | M12 × 100 mm (4 bh/titik) | pcs | 24 |
| 8 | Beton sloof & balok ikat | mutu K-225 | m³ | 1,05 |
| 9 | Pondasi batu kali (1 : 5) | atas 30, bawah 60, dalam 50 cm | titik | 6 |
| 10 | Beton lantai kerja | K-100, tebal 10 cm | m³ | 2,00 |
| 11 | Besi beton polos Ø8 | tulangan + sengkang @15 cm | kg | 60 |
| 12 | Box panel control + dudukan | IP65 | unit | 1 |

## Perbaikan Utama dari Draft Awal

1. **Teks rusak diperbaiki** — huruf terpecah/tumpang tindih pada draft diubah
   menjadi teks utuh yang rapi dan konsisten.
2. **Dimensi antar tampak diserasikan** — draft memiliki angka berbeda antar
   lembar (kedalaman 1990 vs 1968 mm; panjang beton 5136 vs 5670 mm; sloof
   30 × 30 vs 30 × 25 cm). Kini semua berasal dari satu basis desain.
3. **TAMPAK DEPAN diberi dimensi lengkap** — draft elevasi depan tanpa satu
   pun anotasi; kini berdimensi penuh + Detail A (1:5).
4. **Geometri sesuai modul nyata** — 10 kotak kecil pada draft diganti
   5 modul 550 Wp ukuran sebenarnya sesuai label "550 × 5 Wp".
5. **Kelengkapan standar gambar kerja** — kop, skala, arah utara, satuan,
   legenda garis, catatan teknis, BOM, dan tanda potongan A-A.
6. **Pondasi di semua titik kaki** — draft hanya menaruh pondasi di ujung;
   kini seluruh 6 titik kaki didukung pondasi batu kali.

## Referensi

- Instalasi kabel DC & pembumian mengikuti **PUIL 2011** (SNI 0225) dan
  petunjuk pabrikan modul.
- `worklog.md` — catatan lengkap proses pengerjaan.
