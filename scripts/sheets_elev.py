# -*- coding: utf-8 -*-
"""sheets_elev.py — Lembar G-02 TAMPAK DEPAN & G-03 TAMPAK SAMPING (POTONGAN A-A)."""
import math
import design as D
from svgcad import Sheet
from sheets_plan import (kop_sheet, notes_block, legend_block, sheet_list_block,
                         title_under)

X0 = 50.0        # origin elevasi (tepi barat) di kertas
Y_ST = 138.0     # kertas y puncak sloof
S1 = 0.01


def ex(x):
    return X0 + x * S1


def ey(h):
    return Y_ST - h * S1


# ---------------------------------------------------------------- G-02
def g02():
    sh = Sheet("TAMPAK DEPAN", "G-02")
    kop_sheet(sh, "TAMPAK DEPAN — ELEVASI DARI ARAH UTARA")

    xL, xR = ex(0), ex(D.ARR_L)
    y_edge = ey(D.H_FRONT_EDGE)          # bawah band modul (973)
    y_top = ey(D.H_TOP_REAR)             # atas band (1599)

    # --- pondasi & tanah ---
    y_soil = ey(-250)
    y_fb = ey(-750)
    for ax in D.AXES:
        xA, xB = ex(ax - 300), ex(ax + 300)
        sh.rect(xA, y_soil, xB - xA, y_fb - y_soil, "visible2", fill="#efeeea")
        sh.hatch_poly([(xA, y_soil), (xB, y_soil), (xB, y_fb), (xA, y_fb)], spacing=1.2)
    sh.earth_hatch(xL - 7.0, xR + 7.0, y_soil, depth=3.0)

    # --- lantai kerja ---
    y_fl = ey(-150)
    sh.rect(xL - 7.0, y_fl, (xR - xL) + 14.0, y_soil - y_fl, "thin", fill="#f7f6f3")
    sh.hatch_poly([(xL - 7.0, y_fl), (xR + 7.0, y_fl), (xR + 7.0, y_soil), (xL - 7.0, y_soil)],
                  spacing=1.5, ang=-45)

    # --- sloof ---
    y_st = ey(0)
    sh.rect(xL, y_st, xR - xL, y_fl - y_st, "visible", fill="#e9e9e6")
    sh.hatch_poly([(xL, y_st), (xR, y_st), (xR, y_fl), (xL, y_fl)], spacing=1.0)
    sh.line(xL, y_st, xR, y_st, "visible")
    sh.line(xL, y_fl, xR, y_fl, "visible2")

    # --- band modul ---
    sh.rect(xL, y_top, xR - xL, y_edge - y_top, "visible", fill="#3d4f60")
    for i in range(1, D.N_MOD):
        xx = ex(i * D.MOD_W)
        sh.line(xx, y_top, xx, y_edge, "thin", color="#e8eef4")
    for k in (1, 2, 3):
        yy = y_top + (y_edge - y_top) * k / 4.0
        sh.line(xL, yy, xR, yy, "thin", color="#8ba0b4")

    # --- kaki depan + plat + dynabolt ---
    for ax in D.AXES:
        xx = ex(ax)
        sh.line(xx, y_st, xx, y_edge, "visible")
        sh.rect(xx - 0.5, y_st - 0.12, 1.0, 0.3, "visible", fill="#1a1a1a")
        for db in (-0.28, 0.28):
            sh.line(xx + db, y_st, xx + db, y_st + 0.55, "thin")

    # --- box panel control (rangka tengah) ---
    bx = ex(D.AXES[1])
    sh.rect(bx - 2.0, ey(D.BOX_BOTTOM + D.BOX_H), 4.0, 3.0, "visible", fill="#c9cdd2")
    sh.circle(bx - 1.0, ey(D.BOX_BOTTOM + D.BOX_H) + 1.0, 0.3, "thin", fill="#c0392b")
    sh.circle(bx + 1.0, ey(D.BOX_BOTTOM + D.BOX_H) + 1.0, 0.3, "thin", fill="#1e8449")
    sh.line(bx - 2.0, ey(D.BOX_BOTTOM), bx - 1.0, y_st, "thin")
    sh.line(bx + 2.0, ey(D.BOX_BOTTOM), bx + 1.0, y_st, "thin")

    # --- level (kanan) ---
    sh.level_mark(xR + 4.0, y_st, "+0.15")
    sh.level_mark(xR + 4.0, y_fl, "\u00b10.00")
    sh.level_mark(xR + 4.0, y_fb, "-0.60")

    # --- dimensi atas ---
    ticks = [ex(i * D.MOD_W) for i in range(D.N_MOD + 1)]
    sh.dim_h(xL, xR, y_top - 6.0, "5670", ext_from=(y_top, y_top))
    yy = y_top - 2.5
    sh.line(xL, yy, xR, yy, "dim")
    sh._arrow(xL, yy, 0)
    sh._arrow(xR, yy, 180)
    for tx in ticks[:-1]:
        sh._arrow(tx, yy, 0)
        sh._arrow(tx, yy, 180)
    for i in range(D.N_MOD):
        sh.text((ticks[i] + ticks[i + 1]) / 2, yy - 0.8, "1134", size=2.2, anchor="middle")
    for ax, lbl in zip(D.AXES, ["1", "2", "3"]):
        sh.axis_bubble(ex(ax), y_top - 14.0, lbl)

    # --- dimensi bawah ---
    yb1 = y_fb + 5.5
    for (xa, xb, lbl) in [(xL, ex(D.AXES[0]), "550"), (ex(D.AXES[0]), ex(D.AXES[1]), "2285"),
                           (ex(D.AXES[1]), ex(D.AXES[2]), "2285"), (ex(D.AXES[2]), xR, "550")]:
        sh.dim_h(xa, xb, yb1, lbl, ext_from=(y_fb, y_fb))
    sh.dim_h(ex(D.AXES[0] - 300), ex(D.AXES[0] + 300), yb1 + 6.5, "600", ext_from=(yb1, yb1))

    # --- dimensi kanan (tinggi band) ---
    xr1 = xR + 6.0
    sh.dim_v(y_st, y_edge, xr1, "973", ext_from=(xR, xR))
    sh.dim_v(y_edge, y_top, xr1, "626", ext_from=(xR, xR))

    # --- label kiri ---
    sh.leader(ex(D.AXES[0]), ey(700), [(48.0, 126.5), (21.5, 126.5)],
              "KAKI RANGKA HOLLOW 40 x 20", size=2.1, split="(kaki belakang: lihat G-03)",
              size2=1.9, anchor="start")
    sh.leader(51.5, ey(-60), [(46.0, 136.0), (21.5, 136.0)],
              "BALOK PONDASI RANGKA (SLOOF)", size=2.1, split="BETON 30/25 — K-225",
              size2=1.9, anchor="start")
    sh.leader(46.0, ey(-200), [(40.0, 143.5), (21.5, 143.5)],
              "LANTAI KERJA BETON 10 CM", size=2.1, anchor="start")
    sh.leader(ex(D.AXES[0]) - 2.5, ey(-450), [(46.0, 149.5), (21.5, 149.5)],
              "PONDASI BATU KALI 60 x 60", size=2.1, split="DALAM 50 CM (6 TITIK)",
              size2=1.9, anchor="start")

    # --- label kanan ---
    sh.leader(ex(D.ARR_L) - 1.8, y_top + 0.8, [(116.5, 127.5)],
              "MODUL SURYA 550 Wp", size=2.3, bold=True,
              split="5 UNIT — KEMIRINGAN 15\u00b0 KE SELATAN", size2=2.0, anchor="start")
    sh.leader(bx + 2.0, ey(D.BOX_BOTTOM - 60), [(96.0, 140.5), (116.5, 140.5)],
              "BOX PANEL CONTROL", size=2.1, split="(pada rangka tengah)",
              size2=1.9, anchor="start")

    # --- tanda detail A ---
    sh.circle(ex(D.AXES[1]), y_st - 2.2, 3.8, "visible", dash="1.5,1")
    sh.axis_bubble(ex(D.AXES[1]) + 5.6, y_st - 6.0, "A", r=2.4)
    sh.line(ex(D.AXES[1]) + 3.6, y_st - 3.6, ex(D.AXES[1]) + 4.6, y_st - 5.2, "dim")

    title_under(sh, (xL + xR) / 2, yb1 + 14.5, "TAMPAK DEPAN")
    sh.text((xL + xR) / 2, yb1 + 22.5, "DIPANDANG DARI ARAH UTARA (KE SELATAN)",
            size=2.0, anchor="middle", color="#555555")

    detail_a(sh, 105.0, 28.0)
    notes_block(sh, 195.0, 22.0, 215.0)
    legend_block(sh, 320.0, 120.0)
    sheet_list_block(sh, 195.0, 185.0)
    return sh


def detail_a(sh, x, y):
    """DETAIL A — sambungan kaki, plat angkur & sloof. Skala 1:5."""
    F = 0.2
    sh.text(x, y, "DETAIL A — SAMBUNGAN KAKI RANGKA", size=2.8, bold=True)
    sh.text(x, y + 3.8, "SKALA 1 : 5", size=2.2)
    cx = x + 26.0
    ytop = y + 24.0
    w_sloof, h_sloof = 300 * F, 250 * F
    pw, pt = 100 * F, 5 * F
    # sloof potongan
    pts = [(cx - w_sloof / 2, ytop), (cx + w_sloof / 2, ytop),
           (cx + w_sloof / 2, ytop + h_sloof), (cx - w_sloof / 2, ytop + h_sloof)]
    sh.poly(pts, w="frame", close=True)
    sh.hatch_poly(pts, spacing=1.3)
    # plat besi
    sh.rect(cx - pw / 2, ytop - pt, pw, pt, "visible", fill="#d8dbe0")
    # kaki hollow + rail di atasnya
    sh.rect(cx - 10 * F, ytop - pt - 46 * F, 20 * F, 46 * F, "visible", fill="#c9cdd2")
    sh.rect(cx - 10 * F, ytop - pt - 46 * F - 40 * F, 20 * F, 40 * F, "visible", fill="#aeb4bb")
    sh.rect(cx - 8 * F, ytop - pt - 44 * F, 16 * F, 42 * F, "thin")
    yb = ytop - pt - 46 * F - 40 * F
    sh.poly([(cx - 8.5 * F, yb), (cx - 4 * F, yb + 1.2), (cx + 4 * F, yb - 1.2), (cx + 8.5 * F, yb)],
            w="visible2")
    # dynabolt 2 terlihat
    for bx in (-25 * F, 25 * F):
        bw = 6 * F
        sh.rect(cx + bx - bw / 2, ytop - pt, bw, 100 * F, "visible", fill="#9aa1a9")
        sh.rect(cx + bx - 4.5 * F, ytop - pt - 5 * F, 9 * F, 4.5 * F, "visible", fill="#7d848c")
    # dimensi
    sh.dim_v(ytop, ytop + h_sloof, cx + w_sloof / 2 + 5.5, "250")
    sh.dim_h(cx - w_sloof / 2, cx + w_sloof / 2, ytop + h_sloof + 5.5, "300",
             ext_from=(ytop + h_sloof, ytop + h_sloof))
    sh.dim_h(cx - pw / 2, cx + pw / 2, ytop - pt - 9.0, "100")
    sh.dim_v(yb, ytop - pt - 46 * F, cx - 12 * F - 4.0, "40")
    # label
    sh.leader(cx - 25 * F, ytop - pt + 20 * F, [(cx - w_sloof / 2 - 8.0, ytop - pt + 8 * F)],
              "DYNABOLT M12", size=2.0, split="(4 BH / TITIK)", size2=1.8, anchor="end")
    sh.leader(cx + 25 * F, ytop - pt + 26 * F, [(cx + w_sloof / 2 + 8.0, ytop - pt + 30 * F)],
              "ANGKUR EKSPANSI", size=2.0, split="TANAM 100 MM", size2=1.8, anchor="start")
    sh.leader(cx - pw / 2 + 3 * F, ytop - pt / 2, [(cx - w_sloof / 2 - 8.0, ytop - pt - 5 * F)],
              "PLAT BESI 5 MM", size=2.0, split="100 x 100", size2=1.8, anchor="end")
    sh.leader(cx + 10 * F - 1 * F, ytop - pt - 46 * F - 20 * F,
              [(cx + w_sloof / 2 + 8.0, ytop - pt - 46 * F - 30 * F)],
              "KAKI HOLLOW 40 x 20", size=2.0, split="SAMBUNGAN DILAS", size2=1.8, anchor="start")
    sh.leader(cx + 9 * F, yb + 10 * F, [(cx + w_sloof / 2 + 8.0, yb + 4 * F)],
              "RAIL HOLLOW 40 x 20", size=2.0, anchor="start")
    sh.text(cx - w_sloof / 2 - 5.5, ytop + h_sloof / 2, "SLOOF BETON 30/25 (K-225)",
            size=2.0, anchor="end", rot=-90)
    sh.text(cx, ytop + h_sloof + 12.0, "SEMUA TITIK SAMBUNGAN KAKI SAMA (6 TITIK)", size=2.0,
            anchor="middle", color="#555555")


# ---------------------------------------------------------------- G-03
def g03():
    sh = Sheet("TAMPAK SAMPING (POTONGAN A-A)", "G-03")
    kop_sheet(sh, "TAMPAK SAMPING — POTONGAN A-A (SUMBU 2)")

    XA = 85.0
    YST = 165.0

    def sx(v):
        return XA + v * S1

    def sy(h):
        return YST - h * S1

    y_edge = sy(D.H_FRONT_EDGE)
    y_re = sy(D.H_REAR_EDGE)
    y_fl = sy(-150)
    y_sb = sy(-250)
    y_fb = sy(-750)
    xF, xR = sx(D.Y_FRONT), sx(D.Y_REAR)

    # --- tanah & pondasi ---
    for xc in (D.Y_FRONT, D.Y_REAR):
        pts = [(sx(xc - 150), y_sb), (sx(xc + 150), y_sb),
               (sx(xc + 300), y_fb), (sx(xc - 300), y_fb)]
        sh.poly(pts, w="visible2", close=True, fill="#efeeea")
        sh.hatch_poly(pts, spacing=1.2)
    sh.earth_hatch(sx(-300), sx(2650), y_sb, depth=4.0)

    # --- lantai kerja (kiri & kanan) ---
    for (xa, xb) in [(D.Y_FRONT - 150 - 400, D.Y_FRONT - 300),
                     (D.Y_REAR + 300, D.Y_REAR + 150 + 400)]:
        sh.rect(sx(xa), y_fl, sx(xb) - sx(xa), y_sb - y_fl, "thin", fill="#f7f6f3")
        sh.hatch_poly([(sx(xa), y_fl), (sx(xb), y_fl), (sx(xb), y_sb), (sx(xa), y_sb)],
                      spacing=1.5, ang=-45)

    # --- sloof (potongan) ---
    for xc in (D.Y_FRONT, D.Y_REAR):
        pts = [(sx(xc - 150), YST), (sx(xc + 150), YST), (sx(xc + 150), y_sb), (sx(xc - 150), y_sb)]
        sh.poly(pts, w="frame", close=True)
        sh.hatch_poly(pts, spacing=1.15)
    # --- balok ikat (muka sisi) ---
    xT0, xT1 = sx(D.Y_FRONT + 150), sx(D.Y_REAR - 150)
    sh.rect(xT0, YST, xT1 - xT0, y_sb - YST, "visible2")
    sh.line(xT0, YST + 1.25, xT1, YST + 1.25, "thin")
    sh.line(xT0, y_sb - 1.25, xT1, y_sb - 1.25, "thin")

    # --- plat, kaki, rail ---
    for xc, hleg in ((D.Y_FRONT, D.H_FRONT_LEG), (D.Y_REAR, D.H_REAR_LEG)):
        sh.rect(sx(xc) - 0.5, YST - 0.05, 1.0, 0.25, "visible", fill="#1a1a1a")
        for db in (-25, 25):
            sh.line(sx(xc + db), YST, sx(xc + db), YST + 0.8, "thin")
        sh.line(sx(xc), YST, sx(xc), sy(hleg - 40 - 5), "visible")
        sh.rect(sx(xc) - 0.15, sy(hleg - 40 - 5), 0.3, 0.4, "visible", fill="#1a1a1a")

    # --- pengaku diagonal ---
    sh.line(sx(D.Y_FRONT), sy(D.BRACE_Y0), sx(D.Y_REAR), sy(D.BRACE_Y1), "visible2")

    # --- box panel control ---
    bx0 = sx(D.BOX_YC - 100)
    sh.rect(bx0, sy(D.BOX_BOTTOM + D.BOX_H), 2.0, 3.0, "visible", fill="#c9cdd2")
    sh.circle(bx0 + 0.5, sy(D.BOX_BOTTOM + D.BOX_H) + 1.0, 0.25, "thin", fill="#c0392b")
    sh.circle(bx0 + 1.5, sy(D.BOX_BOTTOM + D.BOX_H) + 1.0, 0.25, "thin", fill="#1e8449")
    sh.line(bx0, sy(D.BOX_BOTTOM), xF, sy(D.BOX_BOTTOM - 250), "thin")
    sh.line(bx0 + 2.0, sy(D.BOX_BOTTOM), xR, sy(D.BOX_BOTTOM + 180), "thin")

    # --- modul (garis tebal miring 15°) ---
    sh.line(sx(0), y_edge, sx(D.PLAN_D), y_re, "visible", color="#3d4f60")
    sh.line(sx(0), y_edge, sx(D.PLAN_D), y_re, "visible", color="#1a1a1a")

    # --- level (kanan) ---
    sh.level_mark(sx(2350) + 1.0, YST, "+0.15")
    sh.level_mark(sx(2350) + 1.0, y_fl, "\u00b10.00")
    sh.level_mark(sx(2350) + 1.0, y_fb, "-0.60")

    # --- dimensi kiri (tinggi, bertumpuk) ---
    sh.dim_v(YST, y_edge, sx(0) - 8.0, "973", ext_from=(sx(0), sx(0)))
    sh.dim_v(YST, sy(D.H_FRONT_LEG), sx(0) - 13.0, "1135", ext_from=(sx(0), xF))
    sh.dim_v(YST, sy(D.H_REAR_LEG), sx(0) - 18.0, "1400", ext_from=(sx(0), xR))
    sh.dim_v(YST, y_re, sx(0) - 23.0, "1563", ext_from=(sx(D.PLAN_D), sx(D.PLAN_D)))

    # --- dimensi bawah ---
    yb = y_fb + 6.0
    sh.dim_h(sx(0), xF, yb, "605", ext_from=(y_fb, y_sb))
    sh.dim_h(xF, xR, yb, "990", ext_from=(y_fb, y_fb))
    sh.dim_h(xR, sx(D.PLAN_D), yb, "605", ext_from=(y_fb, y_sb))
    sh.dim_h(sx(0), sx(D.PLAN_D), yb + 6.5, "2200", ext_from=(yb, yb))
    # dimensi modul sejajar kemiringan
    sh.dim_aligned((sx(0), y_edge), (sx(D.PLAN_D), y_re), "2278 (MODUL)", offset=2.8)
    # sudut 15 derajat
    x0c, y0c = sx(0), y_edge
    r = 3.2
    p_arc = [(x0c + r * math.cos(math.radians(t)), y0c - r * math.sin(math.radians(t)))
             for t in range(0, 16)]
    sh.poly(p_arc, w="dim")
    sh.line(x0c, y0c, x0c + 5.0, y0c, "dim")
    sh.text(x0c + r + 0.8, y0c - r - 0.4, "15\u00b0", size=2.2)

    # --- dimensi sloof kiri & pondasi kiri ---
    sh.dim_v(YST, y_sb, sx(D.Y_FRONT - 150) - 4.0, "250", text_left=True)
    sh.dim_v(y_sb, y_fb, sx(D.Y_FRONT - 300) - 6.5, "500", text_left=True)
    sh.dim_h(sx(D.Y_FRONT - 150), sx(D.Y_FRONT + 150), y_sb + 4.0, "300",
             ext_from=(y_sb, y_sb), flip_text=True)
    sh.dim_h(sx(D.Y_FRONT - 300), sx(D.Y_FRONT + 300), y_fb + 13.0, "600",
             ext_from=(y_fb, y_fb), flip_text=True)
    sh.dim_v(y_fl, y_sb, sx(D.Y_FRONT - 400), "100", text_left=True,
             ext_from=(sx(D.Y_FRONT - 300), sx(D.Y_FRONT - 300)))

    # --- dimensi box (kiri box) ---
    sh.dim_v(YST, sy(D.BOX_BOTTOM), sx(D.BOX_YC - 140), "400")
    sh.dim_v(sy(D.BOX_BOTTOM), sy(D.BOX_BOTTOM + D.BOX_H), sx(D.BOX_YC - 140), "300")
    sh.dim_h(bx0, bx0 + 2.0, sy(D.BOX_BOTTOM + D.BOX_H) - 2.2, "200")

    # --- label kanan (kolom x=112) ---
    def rlab(px, py, pts, t1, t2=None, bold=False, sz=2.1):
        sh.leader(px, py, pts, t1, size=sz, split=t2, size2=sz - 0.2,
                  anchor="start", bold=bold)

    rlab(xR + 0.2, sy(1560), [(sx(D.PLAN_D) + 5.0, 140.0)],
         "KAKI & RAIL BAJA HOLLOW 40 x 20")
    rlab(sx(D.PLAN_D) - 0.5, y_re - 0.4, [(sx(D.PLAN_D) + 5.0, 145.0)],
         "MODUL SURYA 550 Wp", "2278 x 1134 x 35 — KEMIRINGAN 15\u00b0", bold=True, sz=2.3)
    rlab((xF + xR) / 2 + 1.0, sy(820), [(sx(D.PLAN_D) + 5.0, 150.0)],
         "PENGAKU HOLLOW 40 x 20 (3 BH)")
    rlab(bx0 + 2.0, sy(680), [(sx(D.PLAN_D) + 5.0, 155.0)],
         "BOX PANEL CONTROL")
    rlab(sx(D.Y_REAR + 180), y_fb - 1.0, [(sx(D.PLAN_D) + 5.0, 160.0)],
         "PONDASI BATU KALI", "ATAS 30 / BAWAH 60 / DALAM 50 CM (6 TITIK)")
    rlab(xR + 0.5, YST + 0.4, [(sx(D.PLAN_D) + 5.0, 166.0)],
         "PLAT BESI 5 mm 100 x 100 + DYNABOLT M12", "(4 BH / TITIK — 6 TITIK)")
    sh.text(sx(D.PLAN_D) + 8.0, 175.0, "TANAH ASLI", size=2.0)

    # --- label kiri bawah ---
    sh.leader(sx(D.Y_FRONT - 100), y_sb - 0.3, [(83.0, 176.0), (61.5, 176.0)],
              "BALOK PONDASI RANGKA (SLOOF)", split="(BETON 30/25 — K-225)",
              size=2.0, size2=2.0, anchor="end")
    sh.leader(sx(D.Y_FRONT - 250), y_fl + 0.3, [(78.0, 182.0), (61.5, 182.0)],
              "LANTAI KERJA BETON 10 CM", size=2.0, anchor="end")
    sh.leader((xT0 + xT1) / 2, y_sb - 0.2, [(86.0, 188.0), (61.5, 188.0)],
              "BALOK IKAT MELINTANG 30/25", size=2.0, anchor="end")

    title_under(sh, (sx(0) + sx(D.PLAN_D)) / 2, yb + 26.0, "TAMPAK SAMPING (POTONGAN A-A)")
    sh.text((sx(0) + sx(D.PLAN_D)) / 2, yb + 34.0,
            "POTONGAN PADA SUMBU 2 — DIPANDANG DARI BARAT (KE TIMUR)", size=2.0,
            anchor="middle", color="#555555")

    notes_block(sh, 195.0, 22.0, 215.0)
    legend_block(sh, 320.0, 120.0)
    sheet_list_block(sh, 195.0, 185.0)
    return sh
