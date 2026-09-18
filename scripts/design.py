# -*- coding: utf-8 -*-
"""design.py — Basis desain terkonsolidasi PLTS Ground Mount 2,75 kWp.
Semua ukuran dalam mm. Referensi tinggi = PUNCAK SLOOF (h = 0).
Elevasi mutlak: lantai kerja ±0.00 = h -250; tanah asli = h -350.

REVISI 2 (per permintaan pemilik proyek):
  - Modul surya 550 Wp, dimensi 1990 x 1130 x 35 mm.
  - Balok kaki rangka panel: tinggi 30 cm di atas lantai kerja (4 bh, sumbu 1 & 3).
  - Sloof: tinggi 25 cm di atas lantai kerja.
  - Pondasi batu kali: hanya 4 titik, kedalaman 30 cm di bawah tanah asli.
  - Kaki rangka tengah (sumbu 2, 2 tiang) tanpa pondasi batu kali — tumpuan
    langsung pada sloof.
  - Semua TAMPAK ATAS: modul surya disamarkan (garis putus-putus) agar
    rangka, balok kaki, sloof, pembesian & plat angkur terlihat jelas.
"""
import math

# ---- modul & array ----
N_MOD = 5
MOD_L, MOD_W, MOD_T = 1990.0, 1130.0, 35.0       # panjang (arah kemiringan), lebar, tebal
TILT = 15.0                                        # derajat
ARR_L = N_MOD * MOD_W                              # 5650
PLAN_D = MOD_L * math.cos(math.radians(TILT))      # 1922.2 -> label 1922
H_DIFF = MOD_L * math.sin(math.radians(TILT))      # 514.7
TAN = math.tan(math.radians(TILT))                 # 0.26795

# ---- kaki & sumbu ----
AXES = [550.0, 2825.0, 5100.0]                     # posisi rangka (dari tepi barat)
AX_EDGE, AX_SP = 550.0, 2275.0
LEG_SPACING = 990.0                                # jarak horizontal antar baris kaki
OVERHANG = (PLAN_D - LEG_SPACING) / 2.0            # 466.1 -> label 466
Y_FRONT = OVERHANG                                 # baris kaki depan (utara) 466
Y_REAR = PLAN_D - OVERHANG                         # baris kaki belakang (selatan) 1456
H_REAR_LEG = 1400.0                                # puncak kaki belakang di atas sloof
H_FRONT_EDGE = H_REAR_LEG - (PLAN_D - Y_FRONT) * TAN   # 1009.8 -> label 1010
H_FRONT_LEG = H_FRONT_EDGE + Y_FRONT * TAN          # 1134.7 -> label 1135
H_REAR_EDGE = H_FRONT_EDGE + PLAN_D * TAN           # 1524.9 -> label 1525
H_TOP_REAR = H_REAR_EDGE + MOD_T / math.cos(math.radians(TILT))  # 1561

# ---- profil rangka (baja hollow galvanis 40x20) ----
RAIL_W, RAIL_H = 20.0, 40.0       # rail: 20 (U-S) x 40 (tegak)
LEG_NS, LEG_EW = 40.0, 20.0       # kaki: 40 arah kemiringan x 20 arah barat-timur
# Panjang batang kaki: sumbu 1 & 3 alas di atas BALOK KAKI (+50 rel. sloof);
# sumbu 2 (tengah) alas langsung di atas SLOOF (+0 rel. sloof) -> 50 mm lebih panjang.
LEG_FRONT_OUT = H_FRONT_LEG - RAIL_H - 5.0 - 50.0   # 1040 (sumbu 1 & 3)
LEG_FRONT_MID = H_FRONT_LEG - RAIL_H - 5.0          # 1090 (sumbu 2)
LEG_REAR_OUT = H_REAR_LEG - RAIL_H - 5.0 - 50.0     # 1305 (sumbu 1 & 3)
LEG_REAR_MID = H_REAR_LEG - RAIL_H - 5.0            # 1355 (sumbu 2)
BRACE_Y0, BRACE_Y1 = 150.0, 1050.0           # pengaku: kaki depan h=150 ke kaki blkg h=1050

# ---- box panel control ----
BOX_EW, BOX_H, BOX_NS = 400.0, 300.0, 200.0
BOX_BOTTOM = 400.0                              # dari puncak sloof
BOX_XC = AXES[1]                                # pada rangka tengah (sumbu 2)
BOX_YC = (Y_FRONT + Y_REAR) / 2.0               # 961

# ---- beton & pondasi ----
SLOOF_W, SLOOF_H = 300.0, 250.0                 # sloof 30 x 25 cm
SLOOF_TOP_ABOVE_FLOOR = 250.0                   # puncak sloof +0.25 di atas lantai kerja
FLOOR_TOP = -250.0                              # lantai kerja ±0.00 (rel. puncak sloof)
LANTAI_T = 100.0                                # tebal lantai kerja 10 cm
GROUND = FLOOR_TOP - LANTAI_T                   # tanah asli -0.10 (-350 rel. sloof)
# Balok kaki rangka (4 bh): beton K-225 30 x 30, tinggi 30 cm dari lantai kerja
PAD_PLAN = 300.0                                # 30 x 30 cm
PAD_TOP = 50.0                                  # +0.30 di atas lantai kerja (rel. sloof)
PAD_H = 300.0                                   # dari lantai kerja (±0.00) ke +0.30
# Pondasi batu kali (4 titik — hanya sumbu 1 & 3):
STONE_TOP = FLOOR_TOP                           # atas batu kali pada ±0.00
STONE_BOT = GROUND - 300.0                      # -0.40 mutlak = 30 cm di bawah tanah
STONE_TOP_W = 300.0                             # lebar atas 30 cm
STONE_BOT_W = 600.0                             # lebar bawah 60 cm
OUTER_AXES = (AXES[0], AXES[2])                 # sumbu dengan pondasi batu kali
TIE_N = 3                                       # balok ikat melintang pada tiap sumbu
PLATE = 100.0                                   # plat besi 5 mm 100x100
PLATE_T = 5.0
N_DYNA = 4                                      # dynabolt M12 per plat

# ---- konversi rencana (koordinat model) ----
# TAMPAK ATAS: x = 0..5650 (barat->timur), y = 0..1922 (utara/rendah -> selatan/tinggi)
# TAMPAK SAMPING: x = 0..1922 (utara -> selatan), h = tinggi di atas puncak sloof
# TAMPAK DEPAN:  x = 0..5650, h = tinggi di atas puncak sloof

def plan_pts():
    """Titik-titik penting rencana."""
    return dict(axes=AXES, y_front=Y_FRONT, y_rear=Y_REAR)


# ---- BOM ----
BOM = [
    ("1", "Modul surya 550 Wp", "1990 x 1130 x 35 mm", "unit", "5"),
    ("2", "Baja hollow galvanis 40 x 20 x 1,6 mm — balk rail memanjang", "2 x 5,65 m", "m", "11,30"),
    ("3", "Baja hollow galvanis 40 x 20 x 1,6 mm — kaki rangka",
     "depan: 2x1,040 + 1x1,090; belakang: 2x1,305 + 1x1,355", "m", "7,14"),
    ("4", "Baja hollow galvanis 40 x 20 x 1,6 mm — pengaku & braket box",
     "3 x 1,34 m + 2 x 0,35 m", "m", "4,72"),
    ("5", "Klem modul (tengah & ujung) + baut M8", "sesuai pabrikan modul", "set", "24"),
    ("6", "Plat besi alas kaki", "5 mm, 100 x 100 mm", "pcs", "6"),
    ("7", "Dynabolt / angkur ekspanansi", "M12 x 100 mm (4 bh/titik)", "pcs", "24"),
    ("8", "Beton sloof, balok ikat & balok kaki rangka", "mutu K-225", "m3", "1,10"),
    ("9", "Pondasi batu kali (1 : 5)", "atas 30, bawah 60, dalam 30 cm di bawah tanah",
     "titik", "4"),
    ("10", "Beton lantai kerja", "K-100, tebal 10 cm", "m3", "2,00"),
    ("11", "Besi beton polos Ø8", "tulangan + sengkang @15 cm", "kg", "60"),
    ("12", "Box panel control + dudukan", "IP65, sesuai spesifikasi", "unit", "1"),
]

# ---- catatan teknis ----
NOTES = [
    "Semua ukuran dalam milimeter (mm), elevasi dalam meter dari ±0.00 permukaan "
    "LANTAI KERJA. Gambar menyempurnakan draft awal; dimensi antar tampak telah "
    "diserasikan.",
    "Modul surya 550 Wp sebanyak 5 unit (total 2,75 kWp), dimensi 1990 x 1130 x 35 mm, "
    "dipasang portrait, kemiringan 15 derajat menghadap UTARA (sesuaikan azimuth "
    "dengan lokasi site).",
    "Pada semua gambar TAMPAK ATAS, modul surya DISAMARKAN (garis putus-putus) agar "
    "rangka, balok kaki, sloof, pembesian dan plat angkur terlihat jelas.",
    "Rangka seluruhnya baja hollow galvanis 40 x 20 mm (tebal min. 1,6 mm). Semua "
    "sambungan rangka DILAS dan diperiksa kerataannya. Kaki tengah (sumbu 2) 50 mm "
    "lebih panjang karena alasnya langsung di atas sloof (+0,25).",
    "Kaki rangka sumbu 1 & 3 diangkur ke BALOK KAKI RANGKA (beton K-225, 30 x 30 cm, "
    "tinggi 30 cm di atas lantai kerja) yang berdiri di atas pondasi batu kali. Kaki "
    "sumbu 2 (tengah) diangkur langsung ke SLOOF (tinggi 25 cm di atas lantai kerja), "
    "tanpa pondasi batu kali. Plat besi 5 mm (100 x 100 mm) + 4 dynabolt M12 per titik.",
    "Sloof & balok ikat beton mutu K-225, tinggi 25 cm di atas lantai kerja, tulangan "
    "Ø8 mm, sengkang jarak 15 cm. Semua struktur beton dituang monolit (disatukan).",
    "Pondasi batu kali hanya 4 TITIK (sumbu 1 & 3, baris A & B): lebar atas 30 cm, "
    "bawah 60 cm, kedalaman 30 cm di bawah tanah asli. Lantai kerja beton K-100 "
    "tebal 10 cm di sekeliling struktur.",
    "Jarak antar rangka (sumbu 1-2-3) 2275 mm; kantilever rail di ujung 550 mm. "
    "Rail memanjang 2 jalur di atas baris kaki.",
    "Pembumian (grounding) rangka & modul serta instalasi kabel DC mengikuti PUIL 2011 "
    "dan petunjuk pabrikan modul.",
]

# ---- legenda ----
LEGEND = [
    ("visible", None, "Tepi benda terlihat"),
    ("hidden", "2,1", "Tepi benda tersembunyi / proyeksi"),
    ("dim", None, "Garis dimensi / leader"),
    ("center", "4,0.8,0.8", "Garis sumbu"),
]

SHEETS = [
    ("G-01", "TAMPAK ATAS (PANEL DISAMARKAN)"),
    ("G-02", "TAMPAK DEPAN"),
    ("G-03", "TAMPAK SAMPING (POTONGAN A-A)"),
    ("G-04", "TAMPAK ATAS — RANGKA PANEL"),
    ("G-05", "TAMPAK ATAS — RANGKA & STRUKTUR BETON"),
    ("G-06", "TAMPAK ATAS — STRUKTUR BETON & ANGKUR"),
]
