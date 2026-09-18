# -*- coding: utf-8 -*-
"""design.py — Basis desain terkonsolidasi PLTS Ground Mount 2,75 kWp.
Semua ukuran dalam mm. Tinggi dihitung dari puncak sloof (0) kecuali disebutkan lain.
"""
import math

# ---- modul & array ----
N_MOD = 5
MOD_L, MOD_W, MOD_T = 2278.0, 1134.0, 35.0          # panjang (arah kemiringan), lebar, tebal
TILT = 15.0                                        # derajat
ARR_L = N_MOD * MOD_W                              # 5670
PLAN_D = MOD_L * math.cos(math.radians(TILT))      # 2200.2 -> label 2200
H_DIFF = MOD_L * math.sin(math.radians(TILT))       # 589.1
TAN = math.tan(math.radians(TILT))                  # 0.26795

# ---- kaki & sumbu ----
AXES = [550.0, 2835.0, 5120.0]                     # posisi rangka (dari tepi barat)
AX_EDGE, AX_SP = 550.0, 2285.0
LEG_SPACING = 990.0                                # jarak horizontal antar baris kaki
OVERHANG = (PLAN_D - LEG_SPACING) / 2.0             # 605.1 -> label 605
Y_FRONT = OVERHANG                                 # baris kaki depan (utara) 605
Y_REAR = PLAN_D - OVERHANG                         # baris kaki belakang (selatan) 1595
H_REAR_LEG = 1400.0
H_FRONT_EDGE = H_REAR_LEG - (PLAN_D - Y_FRONT) * TAN   # 972.6 -> label 973
H_FRONT_LEG = H_FRONT_EDGE + Y_FRONT * TAN          # 1135
H_REAR_EDGE = H_FRONT_EDGE + PLAN_D * TAN           # 1562.5 -> 1563
H_TOP_REAR = H_REAR_EDGE + MOD_T / math.cos(math.radians(TILT))  # 1599

# ---- profil rangka (baja hollow galvanis 40x20) ----
RAIL_W, RAIL_H = 20.0, 40.0       # rail: 20 (U-S) x 40 (tegak)
LEG_NS, LEG_EW = 40.0, 20.0       # kaki: 40 arah kemiringan x 20 arah barat-timur
LEG_FRONT_LEN = H_FRONT_LEG - RAIL_H - 5.0   # 1090
LEG_REAR_LEN = H_REAR_LEG - RAIL_H - 5.0     # 1355
BRACE_Y0, BRACE_Y1 = 150.0, 1050.0           # pengaku: dari kaki depan h=150 ke kaki blkg h=1050

# ---- box panel control ----
BOX_EW, BOX_H, BOX_NS = 400.0, 300.0, 200.0
BOX_BOTTOM = 400.0                              # dari puncak sloof
BOX_XC = AXES[1]                                # pada rangka tengah (sumbu 2)
BOX_YC = (Y_FRONT + Y_REAR) / 2.0               # 1100

# ---- beton ----
SLOOF_W, SLOOF_H = 300.0, 250.0                 # 30 x 25 cm
SLOOF_TOP_ABOVE_FLOOR = 150.0                    # +0.15 di atas lantai kerja
TIE_N = 3                                        # balok ikat melintang pada tiap sumbu
FOOT_TOP, FOOT_BOT, FOOT_DEPTH = 300.0, 600.0, 500.0
FOOT_PLAN = 600.0                                # 60 x 60 cm
LANTAI_T = 100.0
PLATE = 100.0                                    # plat besi 5 mm 100x100
PLATE_T = 5.0
N_DYNA = 4                                        # dynabolt M12 per plat

# ---- konversi rencana (koordinat model) ----
# TAMPAK ATAS: x = 0..5670 (barat->timur), y = 0..2200 (utara/rendah -> selatan/tinggi)
# TAMPAK SAMPING: x = 0..2200 (utara -> selatan), h = tinggi di atas puncak sloof
# TAMPAK DEPAN:  x = 0..5670, h = tinggi di atas puncak sloof

def plan_pts():
    """Titik-titik penting rencana."""
    return dict(axes=AXES, y_front=Y_FRONT, y_rear=Y_REAR)


# ---- BOM ----
BOM = [
    ("1", "Modul surya 550 Wp", "2278 x 1134 x 35 mm", "unit", "5"),
    ("2", "Baja hollow galvanis 40 x 20 x 1,6 mm — balk rail memanjang", "2 x 5,67 m", "m", "11,34"),
    ("3", "Baja hollow galvanis 40 x 20 x 1,6 mm — kaki rangka", "3 x 1,09 m + 3 x 1,36 m", "m", "7,35"),
    ("4", "Baja hollow galvanis 40 x 20 x 1,6 mm — pengaku & braket box", "6 x 1,34 m + braket", "m", "5,30"),
    ("5", "Klem modul (tengah & ujung) + baut M8", "sesuai pabrikan modul", "set", "24"),
    ("6", "Plat besi alas kaki", "5 mm, 100 x 100 mm", "pcs", "6"),
    ("7", "Dynabolt / angkur ekspanansi", "M12 x 100 mm (4 bh/titik)", "pcs", "24"),
    ("8", "Beton sloof & balok ikat", "mutu K-225", "m3", "1,05"),
    ("9", "Pondasi batu kali (1 : 5)", "atas 30, bawah 60, dalam 50 cm", "titik", "6"),
    ("10", "Beton lantai kerja", "K-100, tebal 10 cm", "m3", "2,00"),
    ("11", "Besi beton polos Ø8", "tulangan + sengkang @15 cm", "kg", "60"),
    ("12", "Box panel control + dudukan", "IP65, sesuai spesifikasi", "unit", "1"),
]

# ---- catatan teknis ----
NOTES = [
    "Semua ukuran dalam milimeter (mm), elevasi dalam meter dari ±0.00 lantai kerja. "
    "Gambar menyempurnakan draft awal; dimensi antar tampak telah diserasikan.",
    "Modul surya 550 Wp sebanyak 5 unit (total 2,75 kWp), dipasang portrait, kemiringan "
    "15 derajat menghadap UTARA (sesuaikan azimuth dengan lokasi site).",
    "Rangka seluruhnya baja hollow galvanis 40 x 20 mm (tebal min. 1,6 mm). Semua sambungan "
    "rangka DILAS dan diperiksa kerataannya.",
    "Kaki rangka diangkur ke sloof melalui plat besi 5 mm (100 x 100 mm) dengan 4 dynabolt "
    "M12 per titik. Pastikan plat rata & level (toleransi ±5 mm).",
    "Sloof & balok ikat beton mutu K-225, tulangan Ø8 mm, besi cincin (sengkang) jarak 15 cm. "
    "Semua struktur beton dituang monolit (disatukan).",
    "Pondasi batu kali 6 titik: lebar atas 30 cm, bawah 60 cm, kedalaman 50 cm di bawah "
    "sloof. Lantai kerja beton tebal 10 cm di sekeliling struktur.",
    "Jarak antar rangka (sumbu 1-2-3) 2285 mm; kantilever rail di ujung 550 mm. "
    "Rail memanjang 2 jalur di atas baris kaki.",
    "Pembumian (grounding) rangka & modul serta instalasi kabel DC mengikuti PUIL 2011 dan "
    "petunjuk pabrikan modul.",
]

# ---- legenda ----
LEGEND = [
    ("visible", None, "Tepi benda terlihat"),
    ("hidden", "2,1", "Tepi benda tersembunyi"),
    ("dim", None, "Garis dimensi / leader"),
    ("center", "4,0.8,0.8", "Garis sumbu"),
]

SHEETS = [
    ("G-01", "TAMPAK ATAS"),
    ("G-02", "TAMPAK DEPAN"),
    ("G-03", "TAMPAK SAMPING (POTONGAN A-A)"),
    ("G-04", "TAMPAK ATAS - PANEL SURYA DISAMARKAN (RANGKA)"),
    ("G-05", "TAMPAK ATAS - PANEL DIHILANGKAN (RANGKA & BETON)"),
    ("G-06", "TAMPAK ATAS - PANEL & RANGKA DISAMARKAN (BETON)"),
]
