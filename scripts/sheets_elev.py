# -*- coding: utf-8 -*-
"""sheets_elev.py — Lembar G-02 TAMPAK DEPAN (1:25) & G-03 TAMPAK SAMPING / POTONGAN A-A (1:20).
REVISI 2:
  - Pondasi batu kali hanya 4 titik (sumbu 1 & 3), kedalaman 30 cm di bawah tanah.
  - Balok kaki rangka beton 30 x 30, tinggi +0,30 di atas lantai kerja (sumbu 1 & 3).
  - Sloof tinggi +0,25 di atas lantai kerja; kaki tengah (sumbu 2) langsung di atas sloof.
  - Detail A dipecah: A-1 (kaki luar di atas balok kaki) & A-2 (kaki tengah di atas sloof),
    keduanya skala 1 : 5.
"""
import math
import design as D
from svgcad import Sheet
from sheets_plan import (kop_sheet, notes_block, legend_block, sheet_list_block,
                         title_under)

X0 = 60.0        # origin elevasi depan (tepi barat) di kertas
Y_ST = 105.0     # kertas y puncak sloof (G-02)
S1 = 0.04        # 1:25


def ex(x):
    return X0 + x * S1


def ey(h):
    return Y_ST - h * S1


# ---------------------------------------------------------------- G-02
def g02():
    sh = Sheet("TAMPAK DEPAN", "G-02", scale_txt="1 : 25", rev="2")
    kop_sheet(sh, "TAMPAK DEPAN — ELEVASI DARI ARAH UTARA")

    xL, xR = ex(0), ex(D.ARR_L)
    y_edge = ey(D.H_FRONT_EDGE)      # bawah band modul (1010)
    y_top = ey(D.H_TOP_REAR)         # atas band (1561)
    y_st = ey(0)                     # puncak sloof (+0.25)
    y_pad = ey(D.PAD_TOP)            # puncak balok kaki (+0.30)
    y_fl = ey(D.FLOOR_TOP)           # lantai kerja ±0.00
    y_gr = ey(D.GROUND)              # tanah asli (-0.10)
    y_fb = ey(D.STONE_BOT)           # dasar pondasi (-0.40)

    # --- lantai kerja ---
    sh.rect(xL - 7.0, y_fl, (xR - xL) + 14.0, y_gr - y_fl, "thin", fill="#f7f6f3")
    sh.hatch_poly([(xL - 7.0, y_fl), (xR + 7.0, y_fl), (xR + 7.0, y_gr), (xL - 7.0, y_gr)],
                  spacing=1.8, ang=-45)
    # --- tanah asli ---
    sh.earth_hatch(xL - 7.0, xR + 7.0, y_gr, depth=3.0)

    # --- pondasi batu kali (HANYA sumbu 1 & 3 — trapesium 30/60) ---
    for ax in D.OUTER_AXES:
        pts = [(ex(ax - 150), y_fl), (ex(ax + 150), y_fl),
               (ex(ax + 300), y_fb), (ex(ax - 300), y_fb)]
        sh.poly(pts, w="visible2", close=True, fill="#efeeea")
        sh.hatch_poly(pts, spacing=1.6)

    # --- sloof (memanjang penuh, tinggi +0.25) ---
    sh.rect(xL, y_st, xR - xL, y_fl - y_st, "visible", fill="#e9e9e6")
    sh.hatch_poly([(xL, y_st), (xR, y_st), (xR, y_fl), (xL, y_fl)], spacing=1.4)
    sh.line(xL, y_st, xR, y_st, "visible")
    sh.line(xL, y_fl, xR, y_fl, "visible2")

    # --- balok kaki rangka (sumbu 1 & 3, tinggi +0.30) ---
    for ax in D.OUTER_AXES:
        xA, xB = ex(ax - 150), ex(ax + 150)
        sh.rect(xA, y_pad, xB - xA, y_fl - y_pad, "visible", fill="#d7d7d0")
        sh.hatch_poly([(xA, y_pad), (xB, y_pad), (xB, y_fl), (xA, y_fl)],
                      spacing=1.4, phase=0.6)
        sh.line(xA, y_pad, xB, y_pad, "visible")

    # --- band modul ---
    sh.rect(xL, y_top, xR - xL, y_edge - y_top, "visible", fill="#3d4f60")
    for i in range(1, D.N_MOD):
        xx = ex(i * D.MOD_W)
        sh.line(xx, y_top, xx, y_edge, "thin", color="#e8eef4")
    for k in (1, 2, 3):
        yy = y_top + (y_edge - y_top) * k / 4.0
        sh.line(xL, yy, xR, yy, "thin", color="#8ba0b4")

    # --- kaki + plat + dynabolt (sumbu 1 & 3 di balok kaki; sumbu 2 di sloof) ---
    for ax in D.AXES:
        xx = ex(ax)
        base = y_pad if ax in D.OUTER_AXES else y_st
        sh.line(xx, base, xx, y_edge, "visible")
        sh.rect(xx - 2.0, base - 0.12, 4.0, 0.3, "visible", fill="#1a1a1a")
        for db in (-1.0, 1.0):
            sh.line(xx + db, base, xx + db, base + 2.2, "thin")

    # --- box panel control (rangka tengah) ---
    bx = ex(D.AXES[1])
    sh.rect(bx - 8.0, ey(D.BOX_BOTTOM + D.BOX_H), 16.0, 12.0, "visible", fill="#c9cdd2")
    sh.circle(bx - 4.0, ey(D.BOX_BOTTOM + D.BOX_H) + 4.0, 1.2, "thin", fill="#c0392b")
    sh.circle(bx + 4.0, ey(D.BOX_BOTTOM + D.BOX_H) + 4.0, 1.2, "thin", fill="#1e8449")
    sh.line(bx - 8.0, ey(D.BOX_BOTTOM), bx - 4.0, y_st, "thin")
    sh.line(bx + 8.0, ey(D.BOX_BOTTOM), bx + 4.0, y_st, "thin")

    # --- level (kanan) ---
    sh.level_mark(xR + 4.0, y_pad, "+0,30")
    sh.level_mark(xR + 4.0, y_st, "+0,25")
    sh.level_mark(xR + 4.0, y_fl, "\u00b10,00")
    sh.level_mark(xR + 4.0, y_fb, "-0,40")

    # --- dimensi atas ---
    ticks = [ex(i * D.MOD_W) for i in range(D.N_MOD + 1)]
    sh.dim_h(xL, xR, y_top - 6.0, "5650", ext_from=(y_top, y_top))
    yy = y_top - 2.5
    sh.line(xL, yy, xR, yy, "dim")
    sh._arrow(xL, yy, 0)
    sh._arrow(xR, yy, 180)
    for tx in ticks[:-1]:
        sh._arrow(tx, yy, 0)
        sh._arrow(tx, yy, 180)
    for i in range(D.N_MOD):
        sh.text((ticks[i] + ticks[i + 1]) / 2, yy - 0.8, "1130", size=2.2, anchor="middle")
    for ax, lbl in zip(D.AXES, ["1", "2", "3"]):
        sh.axis_bubble(ex(ax), y_top - 14.0, lbl)

    # --- dimensi bawah ---
    yb1 = y_fb + 5.5
    for (xa, xb, lbl) in [(xL, ex(D.AXES[0]), "550"), (ex(D.AXES[0]), ex(D.AXES[1]), "2275"),
                           (ex(D.AXES[1]), ex(D.AXES[2]), "2275"), (ex(D.AXES[2]), xR, "550")]:
        sh.dim_h(xa, xb, yb1, lbl, ext_from=(y_fb, y_fb))
    sh.dim_h(ex(D.AXES[0] - 300), ex(D.AXES[0] + 300), yb1 + 6.5, "600", ext_from=(yb1, yb1))

    # --- dimensi kanan (tinggi band) ---
    xr1 = xR + 6.0
    sh.dim_v(y_st, y_edge, xr1, "1010", ext_from=(xR, xR))
    sh.dim_v(y_edge, y_top, xr1, "551", ext_from=(xR, xR))

    # --- dimensi tinggi balok kaki (kiri sumbu 1) ---
    sh.dim_v(y_pad, y_fl, ex(D.AXES[0] - 150) - 4.0, "300", ext_from=(ex(D.AXES[0] - 150),) * 2)

    # --- label kiri (di margin kiri, bebas dari gambar) ---
    sh.leader(ex(D.AXES[0]), ey(700), [(66.0, 74.0), (23.0, 74.0)],
              "KAKI RANGKA HOLLOW 40 x 20", size=2.1, split="(kaki tengah 50 mm lebih panjang)",
              size2=1.9, anchor="start")
    sh.leader(63.0, ey(-60), [(66.0, 86.0), (23.0, 86.0)],
              "BALOK PONDASI RANGKA (SLOOF)", size=2.1, split="BETON 30/25 — TINGGI +0,25 — K-225",
              size2=1.9, anchor="start")
    sh.leader(58.0, y_fl + 1.2, [(66.0, 93.0), (23.0, 93.0)],
              "LANTAI KERJA BETON 10 CM", size=2.1, anchor="start")
    sh.leader(ex(D.AXES[0] - 150), ey(-100), [(70.0, 100.0), (23.0, 100.0)],
              "BALOK KAKI RANGKA BETON 30/30", size=2.1, split="TINGGI +0,30 — DI ATAS PONDASI BATU KALI",
              size2=1.9, anchor="start")
    sh.leader(ex(D.AXES[0] - 280), ey(-450), [(52.0, 118.0), (23.0, 118.0)],
              "PONDASI BATU KALI 60 x 60", size=2.1, split="DALAM 30 cm — 4 TITIK (SUMBU 1 & 3)",
              size2=1.9, anchor="start")

    # --- label kanan (di area interior elevasi yang kosong) ---
    sh.leader(225.0, y_edge + 0.4, [(230.0, 78.0)],
              "MODUL SURYA 550 Wp", size=2.3, bold=True,
              split="1990 x 1130 x 35 mm — 5 UNIT — 15\u00b0 KE SELATAN", size2=2.0, anchor="start")
    sh.leader(bx + 8.0, ey(D.BOX_BOTTOM - 60), [(186.0, 95.0)],
              "BOX PANEL CONTROL", size=2.1, split="(pada rangka tengah)",
              size2=1.9, anchor="start")

    # --- tanda detail A-1 (kaki luar) & A-2 (kaki tengah) ---
    sh.circle(ex(D.AXES[0]), ey(-120), 4.0, "visible", dash="1.5,1")
    sh.axis_bubble(ex(D.AXES[0]) + 9.5, ey(-140), "A-1", r=2.6)
    sh.circle(ex(D.AXES[1]), ey(-65), 4.0, "visible", dash="1.5,1")
    sh.axis_bubble(ex(D.AXES[1]) + 7.7, ey(-90), "A-2", r=2.6)

    title_under(sh, (xL + xR) / 2, yb1 + 14.5, "TAMPAK DEPAN")
    sh.text((xL + xR) / 2, yb1 + 22.5, "DIPANDAT DARI ARAH UTARA (KE SELATAN)",
            size=2.0, anchor="middle", color="#555555")

    # --- detail A-1 & A-2 (skala 1:5) di band bawah ---
    detail_foot(sh, 24.0, 164.0, 58.0,
                "DETAIL A-1 — KAKI LUAR: DI ATAS BALOK KAKI",
                "BALOK KAKI BETON K-225 30 x 30",
                "TINGGI BALOK KAKI +0,30 DI ATAS LANTAI KERJA", "#d7d7d0")
    detail_foot(sh, 140.0, 164.0, 175.0,
                "DETAIL A-2 — KAKI TENGAH: DI ATAS SLOOF",
                "SLOOF BETON K-225 30/25",
                "TINGGI SLOOF +0,25 DI ATAS LANTAI KERJA", "#e9e9e6")
    sh.text(137.0, 242.5, "A-1 = KAKI SUMBU 1 & 3 (4 TITIK) — A-2 = KAKI SUMBU 2 (2 TITIK)",
            size=2.0, bold=True, anchor="middle")

    notes_block(sh, 305.0, 16.0, 106.0)
    legend_block(sh, 305.0, 94.0)
    sheet_list_block(sh, 305.0, 132.0, 106.0)
    return sh


def detail_foot(sh, x, y, cx, judul, support_lbl, caption, support_fill):
    """DETAIL A-1 / A-2 — sambungan kaki, plat angkur & tumpuan. Skala 1:5."""
    sh.text(x, y, judul, size=2.4, bold=True)
    sh.text(x, y + 3.8, "SKALA 1 : 5", size=2.0)
    R_top = y + 13.0                       # puncak rail
    # rail hollow (potongan sisi)
    sh.rect(cx - 2.0, R_top, 4.0, 8.0, "visible", fill="#aeb4bb")
    sh.rect(cx - 1.6, R_top + 0.4, 3.2, 7.2, "thin")
    sh.poly([(cx - 2.4, R_top), (cx - 1.0, R_top + 1.0), (cx + 1.0, R_top - 0.8),
             (cx + 2.4, R_top)], w="visible2")
    # kaki hollow
    sh.rect(cx - 2.0, R_top + 8.0, 4.0, 9.2, "visible", fill="#c9cdd2")
    sh.rect(cx - 1.6, R_top + 8.4, 3.2, 8.4, "thin")
    # plat besi 5 mm 100 x 100
    plate_y = R_top + 17.2
    sh.rect(cx - 10.0, plate_y, 20.0, 1.0, "visible", fill="#d8dbe0")
    # tumpuan (balok kaki / sloof) — potongan parsial 150 mm + garis putus
    sup_y = plate_y + 1.0
    pts = [(cx - 30.0, sup_y), (cx + 30.0, sup_y),
           (cx + 30.0, sup_y + 30.0), (cx - 30.0, sup_y + 30.0)]
    sh.poly(pts, w="frame", close=True, fill=support_fill)
    sh.hatch_poly(pts, spacing=1.3)
    sh.poly([(cx - 30.0, sup_y + 30.0), (cx - 10.0, sup_y + 31.2),
             (cx + 10.0, sup_y + 28.8), (cx + 30.0, sup_y + 30.0)], w="thin")
    # dynabolt 2 terlihat (embed 100 mm)
    for bxc in (-5.0, 5.0):
        sh.rect(cx + bxc - 0.6, plate_y, 1.2, 20.0, "visible", fill="#9aa1a9")
        sh.rect(cx + bxc - 0.9, plate_y - 0.9, 1.8, 0.9, "visible", fill="#7d848c")
    # dimensi
    sh.dim_h(cx - 30.0, cx + 30.0, sup_y + 35.5, "300", ext_from=(sup_y + 30.0, sup_y + 30.0))
    sh.dim_h(cx - 10.0, cx + 10.0, plate_y - 9.0, "100")
    sh.dim_v(R_top, R_top + 8.0, cx - 6.4, "40")
    # label kanan
    sh.leader(cx + 2.0, R_top + 3.0, [(cx + 32.0, y + 13.0)],
              "RAIL HOLLOW 40 x 20", size=2.0, anchor="start")
    sh.leader(cx + 2.0, R_top + 12.6, [(cx + 32.0, y + 25.0)],
              "KAKI HOLLOW 40 x 20", size=2.0, split="SAMBUNGAN DILAS",
              size2=1.8, anchor="start")
    sh.leader(cx + 6.0, plate_y + 0.5, [(cx + 32.0, y + 33.5)],
              "PLAT BESI 5 mm 100 x 100", size=2.0, anchor="start")
    sh.leader(cx + 5.0, plate_y + 9.0, [(cx + 32.0, y + 44.5)],
              "DYNABOLT M12", size=2.0, split="(4 BH/TITIK — EMBED 100)",
              size2=1.8, anchor="start")
    # label tumpuan (rotasi, kiri)
    sh.text(cx - 34.0, sup_y + 15.0, support_lbl, size=2.0, anchor="middle", rot=-90)
    # keterangan bawah
    sh.text(cx, sup_y + 43.0, caption, size=1.9, anchor="middle")


# ---------------------------------------------------------------- G-03
def g03():
    sh = Sheet("TAMPAK SAMPING (POTONGAN A-A)", "G-03", scale_txt="1 : 20", rev="2")
    kop_sheet(sh, "TAMPAK SAMPING — POTONGAN A-A (SUMBU 2)")

    XA = 100.0     # origin potongan (utara) di kertas
    YST = 118.0    # kertas y puncak sloof
    S2 = 0.05      # 1:20

    def sx(v):
        return XA + v * S2

    def sy(h):
        return YST - h * S2

    y_edge = sy(D.H_FRONT_EDGE)       # 67.5
    y_re = sy(D.H_REAR_EDGE)          # 41.75
    y_pad = sy(D.PAD_TOP)             # 115.5
    y_fl = sy(D.FLOOR_TOP)            # 130.5
    y_gr = sy(D.GROUND)               # 135.5
    y_fb = sy(D.STONE_BOT)            # 150.5
    xF, xR = sx(D.Y_FRONT), sx(D.Y_REAR)

    # --- lantai kerja (kiri & kanan, di sekeliling struktur) ---
    for (xa, xb) in [(D.Y_FRONT - 150 - 400, D.Y_FRONT - 300),
                     (D.Y_REAR + 300, D.Y_REAR + 150 + 400)]:
        sh.rect(sx(xa), y_fl, sx(xb) - sx(xa), y_gr - y_fl, "thin", fill="#f7f6f3")
        sh.hatch_poly([(sx(xa), y_fl), (sx(xb), y_fl), (sx(xb), y_gr), (sx(xa), y_gr)],
                      spacing=1.8, ang=-45)
    # --- tanah asli ---
    sh.earth_hatch(sx(-300), sx(2650), y_gr, depth=4.0)

    # --- proyeksi pondasi batu kali & balok kaki (sumbu 1 & 3, di belakang
    #     bidang potong — digambar putus-putus, isian putih menutup arsir tanah) ---
    for xc in (D.Y_FRONT, D.Y_REAR):
        pts = [(sx(xc - 150), y_fl), (sx(xc + 150), y_fl),
               (sx(xc + 300), y_fb), (sx(xc - 300), y_fb)]
        sh.poly(pts, w="hidden", close=True, fill="#ffffff", dash="2,1")
        sh.rect(sx(xc - 150), y_pad, 15.0, YST - y_pad, "hidden", fill="none", dash="2,1")

    # --- sloof (potongan, tinggi +0.25) ---
    for xc in (D.Y_FRONT, D.Y_REAR):
        pts = [(sx(xc - 150), YST), (sx(xc + 150), YST), (sx(xc + 150), y_fl), (sx(xc - 150), y_fl)]
        sh.poly(pts, w="frame", close=True)
        sh.hatch_poly(pts, spacing=1.7)
    # --- balok ikat (muka sisi, terpotong pada bidang sumbu 2) ---
    xT0, xT1 = sx(D.Y_FRONT + 150), sx(D.Y_REAR - 150)
    sh.rect(xT0, YST, xT1 - xT0, y_fl - YST, "visible2")
    sh.line(xT0, YST + 1.25, xT1, YST + 1.25, "thin")
    sh.line(xT0, y_fl - 1.25, xT1, y_fl - 1.25, "thin")

    # --- plat, kaki, rail (kaki tengah — alas LANGSUNG di atas sloof) ---
    for xc, hleg in ((D.Y_FRONT, D.H_FRONT_LEG), (D.Y_REAR, D.H_REAR_LEG)):
        sh.rect(sx(xc) - 2.5, YST - 0.15, 5.0, 0.3, "visible", fill="#1a1a1a")
        for db in (-25, 25):
            sh.line(sx(xc + db), YST, sx(xc + db), YST + 1.6, "thin")
        sh.line(sx(xc), YST, sx(xc), sy(hleg - 45), "visible")
        sh.rect(sx(xc) - 1.0, sy(hleg - 45), 2.0, 1.0, "visible", fill="#1a1a1a")

    # --- pengaku diagonal ---
    sh.line(sx(D.Y_FRONT), sy(D.BRACE_Y0), sx(D.Y_REAR), sy(D.BRACE_Y1), "visible2")

    # --- box panel control ---
    bx0 = sx(D.BOX_YC - 100)
    sh.rect(bx0, sy(D.BOX_BOTTOM + D.BOX_H), 10.0, 15.0, "visible", fill="#c9cdd2")
    sh.circle(bx0 + 2.5, sy(D.BOX_BOTTOM + D.BOX_H) + 3.0, 0.8, "thin", fill="#c0392b")
    sh.circle(bx0 + 7.5, sy(D.BOX_BOTTOM + D.BOX_H) + 3.0, 0.8, "thin", fill="#1e8449")
    sh.line(bx0, sy(D.BOX_BOTTOM), xF, sy(D.BOX_BOTTOM - 250), "thin")
    sh.line(bx0 + 10.0, sy(D.BOX_BOTTOM), xR, sy(D.BOX_BOTTOM + 180), "thin")

    # --- modul (garis miring 15 derajat, tebal 35 mm) ---
    th = D.MOD_T / math.cos(math.radians(D.TILT)) * S2    # 1.81 mm kertas
    sh.line(sx(0), y_edge, sx(D.PLAN_D), y_re, "visible", color="#3d4f60")
    sh.line(sx(0), y_edge - th, sx(D.PLAN_D), y_re - th, "visible", color="#1a1a1a")
    sh.line(sx(0), y_edge, sx(0), y_edge - th, "thin", color="#1a1a1a")
    sh.line(sx(D.PLAN_D), y_re, sx(D.PLAN_D), y_re - th, "thin", color="#1a1a1a")

    # --- level (kanan, digeser jauh ke kanan agar tidak menabrak label) ---
    sh.level_mark(255.0, y_pad, "+0,30")
    sh.level_mark(255.0, YST, "+0,25")
    sh.level_mark(255.0, y_fl, "\u00b10,00")
    sh.level_mark(255.0, y_fb, "-0,40")

    # --- dimensi kiri (tinggi, bertumpuk) ---
    sh.dim_v(YST, y_edge, sx(0) - 8.0, "1010", ext_from=(sx(0), sx(0)))
    sh.dim_v(YST, sy(D.H_FRONT_LEG), sx(0) - 13.0, "1135", ext_from=(sx(0), xF))
    sh.dim_v(YST, sy(D.H_REAR_LEG), sx(0) - 18.0, "1400", ext_from=(sx(0), xR))
    sh.dim_v(YST, y_re, sx(0) - 23.0, "1525", ext_from=(sx(D.PLAN_D), sx(D.PLAN_D)))

    # --- dimensi bawah (rantai -> pondasi -> total) ---
    yb = y_fb + 6.0
    sh.dim_h(sx(0), xF, yb, "466", ext_from=(y_fb, y_fl))
    sh.dim_h(xF, xR, yb, "990", ext_from=(y_fb, y_fb))
    sh.dim_h(xR, sx(D.PLAN_D), yb, "466", ext_from=(y_fb, y_fl))
    sh.dim_h(sx(D.Y_FRONT - 300), sx(D.Y_FRONT + 300), yb + 6.5, "600",
             ext_from=(y_fb, y_fb), flip_text=True)
    sh.dim_h(sx(0), sx(D.PLAN_D), yb + 13.0, "1922", ext_from=(yb, yb))
    # dimensi modul sejajar kemiringan
    sh.dim_aligned((sx(0), y_edge), (sx(D.PLAN_D), y_re), "1990 (MODUL)", offset=3.5)
    # sudut 15 derajat
    x0c, y0c = sx(0), y_edge
    r = 6.0
    p_arc = [(x0c + r * math.cos(math.radians(t)), y0c - r * math.sin(math.radians(t)))
             for t in range(0, 16)]
    sh.poly(p_arc, w="dim")
    sh.line(x0c, y0c, x0c + 9.0, y0c, "dim")
    sh.text(x0c + r + 0.8, y0c - r - 0.4, "15\u00b0", size=2.2)

    # --- dimensi sloof kiri, pondasi & lantai ---
    sh.dim_v(YST, y_fl, sx(D.Y_FRONT - 150) - 4.0, "250", text_left=True)
    sh.dim_h(sx(D.Y_FRONT - 150), sx(D.Y_FRONT + 150), y_fl + 4.0, "300",
             ext_from=(y_fl, y_fl), flip_text=True)
    sh.dim_v(y_gr, y_fb, sx(D.Y_FRONT - 300) - 5.0, "300", text_left=True,
             ext_from=(sx(D.Y_FRONT - 300),) * 2)
    sh.dim_v(y_fl, y_gr, sx(D.Y_FRONT - 550), "100", text_left=True,
             ext_from=(sx(D.Y_FRONT - 300),) * 2)

    # --- dimensi box (kiri box) ---
    sh.dim_v(YST, sy(D.BOX_BOTTOM), sx(D.BOX_YC - 140), "400")
    sh.dim_v(sy(D.BOX_BOTTOM), sy(D.BOX_BOTTOM + D.BOX_H), sx(D.BOX_YC - 140), "300")
    sh.dim_h(bx0, bx0 + 10.0, sy(D.BOX_BOTTOM + D.BOX_H) - 2.2, "200")

    # --- label kanan ---
    def rlab(px, py, pts, t1, t2=None, bold=False, sz=2.1):
        sh.leader(px, py, pts, t1, size=sz, split=t2, size2=sz - 0.2,
                  anchor="start", bold=bold)

    rlab(xR + 0.2, sy(1560), [(sx(D.PLAN_D) + 6.0, 45.0)],
         "KAKI & RAIL BAJA HOLLOW 40 x 20")
    rlab(sx(D.PLAN_D) - 0.5, y_re - 0.4, [(sx(D.PLAN_D) + 6.0, 52.0)],
         "MODUL SURYA 550 Wp", "1990 x 1130 x 35 — KEMIRINGAN 15\u00b0", bold=True, sz=2.3)
    rlab((xF + xR) / 2 + 1.0, sy(820), [(sx(D.PLAN_D) + 6.0, 58.0)],
         "PENGAKU HOLLOW 40 x 20 (3 BH)")
    rlab(bx0 + 10.0, sy(680), [(sx(D.PLAN_D) + 6.0, 64.0)],
         "BOX PANEL CONTROL")
    rlab(xR + 7.2, y_pad + 0.5, [(sx(D.PLAN_D) + 6.0, 132.0)],
         "BALOK KAKI RANGKA (PROYEKSI)", "TINGGI +0,30 — HANYA SUMBU 1 & 3")
    rlab(xR + 0.5, YST + 0.4, [(sx(D.PLAN_D) + 6.0, 140.0)],
         "PLAT BESI 5 mm + DYNABOLT M12 (4 BH/TITIK)", "KAKI TENGAH LANGSUNG DI ATAS SLOOF")
    rlab(sx(D.Y_REAR + 180), y_fb - 1.0, [(sx(D.PLAN_D) + 6.0, 152.0)],
         "PONDASI BATU KALI", "ATAS 30 / BAWAH 60 / DALAM 30 cm — 4 TITIK")
    sh.text(sx(D.PLAN_D) + 8.0, 175.0, "TANAH ASLI", size=2.0)

    # --- label kiri bawah ---
    sh.leader(sx(D.Y_FRONT - 100), y_fl - 0.3, [(115.0, 178.0), (68.0, 178.0)],
              "BALOK PONDASI RANGKA (SLOOF)", split="(BETON 30/25 — K-225 — TINGGI +0,25)",
              size=2.0, size2=2.0, anchor="end")
    sh.leader(sx(D.Y_FRONT - 450), y_fl + 0.3, [(100.0, 184.0), (68.0, 184.0)],
              "LANTAI KERJA BETON 10 CM", size=2.0, anchor="end")
    sh.leader((xT0 + xT1) / 2, y_fl - 0.2, [(115.0, 190.0), (68.0, 190.0)],
              "BALOK IKAT MELINTANG 30/25 (3 BH)", size=2.0, anchor="end")

    title_under(sh, (sx(0) + sx(D.PLAN_D)) / 2, 190.0, "TAMPAK SAMPING (POTONGAN A-A)",
                t2="SKALA 1 : 20")
    sh.text((sx(0) + sx(D.PLAN_D)) / 2, 198.2,
            "POTONGAN PADA SUMBU 2 — DIPANDANG DARI BARAT (KE TIMUR)", size=2.0,
            anchor="middle", color="#555555")
    sh.text((sx(0) + sx(D.PLAN_D)) / 2, 202.6,
            "KAKI TENGAH LANGSUNG DI ATAS SLOOF — PONDASI & BALOK KAKI (PUTUS-PUTUS) "
            "HANYA DI SUMBU 1 & 3", size=1.9, anchor="middle", color="#555555")

    notes_block(sh, 280.0, 16.0, 131.0)
    legend_block(sh, 280.0, 86.0)
    sheet_list_block(sh, 280.0, 124.0, 131.0)
    return sh
