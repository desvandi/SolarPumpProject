# -*- coding: utf-8 -*-
"""sheets_plan.py — Lembar G-01 (tampak atas), G-04 (rangka), G-05 (rangka+beton), G-06 (beton)."""
import math
import design as D
from svgcad import Sheet

S = 0.01  # 1:100
X0, Y0 = 48.0, 82.0  # origin rencana di kertas (tepi barat, tepi utara)


def mx(x):
    return X0 + x * S


def my(y):
    return Y0 + y * S


def ph(h):
    """tinggi model (di atas sloof) -> kertas (y makin kecil makin tinggi)."""
    return h * S


# ---------------------------------------------------------------- blok umum
def title_under(sh, cx, y, t1, t2="SKALA 1 : 100"):
    sh.text(cx, y, t1, size=4.0, anchor="middle", bold=True, spacing="0.5")
    sh.text(cx, y + 4.2, t2, size=2.4, anchor="middle")


def wrap(s, width_mm, size):
    maxc = max(10, int(width_mm / (0.50 * size)))
    words, lines, cur = s.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > maxc:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    return lines


def notes_block(sh, x, y, w, title="CATATAN :"):
    sh.text(x, y, title, size=2.6, bold=True)
    yy = y + 4.2
    for i, n in enumerate(D.NOTES, 1):
        first = True
        for ln in wrap(n, w - 7.0, 2.05):
            if first:
                sh.text(x, yy, f"{i}.", size=2.05, anchor="end")
                sh.text(x + 1.2, yy, ln, size=2.05)
                first = False
            else:
                sh.text(x + 1.2, yy, ln, size=2.05)
            yy += 2.9
        yy += 1.1
    return yy


def legend_block(sh, x, y, w=105.0):
    sh.text(x, y, "LEGENDA :", size=2.6, bold=True)
    yy = y + 4.6
    samples = [
        ("visible", None, "Tepi benda terlihat", False),
        ("hidden", "2,1", "Tepi benda tersembunyi", False),
        ("dim", None, "Garis dimensi / leader", False),
        ("center", "4,0.8,0.8", "Garis sumbu", False),
        ("thin", None, "Arsir beton / detail tipis", False),
        ("visible", None, "Kotak gelap : modul surya", True),
    ]
    for st, dash, lbl, dark in samples:
        if dark:
            sh.rect(x, yy - 1.4, 9, 1.8, "visible", fill="#3d4f60")
        else:
            sh.line(x, yy - 0.5, x + 9, yy - 0.5, st, dash=dash)
        sh.text(x + 11.5, yy, lbl, size=2.05)
        yy += 4.2
    # arsir tanah
    sh.earth_hatch(x, x + 9, yy - 1.2, depth=1.2)
    sh.text(x + 11.5, yy + 0.8, "Tanah asli", size=2.05)
    return yy + 4.5


def bom_table(sh, x, y, w=215.0):
    cols = [0.0, 8.0, 84.0, 152.0, 175.0, 197.0, 215.0]
    sh.text(x, y - 2.2, "DAFTAR KEBUTUHAN MATERIAL (BOM) :", size=2.6, bold=True)
    rh = 4.05
    # header
    sh.rect(x, y, w, 4.4, "visible", fill="#e8ecef")
    sh.text(x + 2.5, y + 3.0, "NO", size=1.9, bold=True)
    sh.text(x + 10.0, y + 3.0, "URAIAN MATERIAL", size=1.9, bold=True)
    sh.text(x + 86.0, y + 3.0, "SPESIFIKASI", size=1.9, bold=True)
    sh.text(x + 153.0, y + 3.0, "SAT.", size=1.9, bold=True, anchor="middle")
    sh.text(x + 176.0, y + 3.0, "QTY", size=1.9, bold=True, anchor="middle")
    yy = y + 4.4
    for i, r in enumerate(D.BOM):
        if i % 2 == 1:
            sh.rect(x, yy, w, rh, "thin", fill="#f4f6f8")
        sh.text(x + 2.5, yy + 2.8, r[0], size=1.95)
        sh.text(x + 10.0, yy + 2.8, r[1], size=1.95)
        sh.text(x + 86.0, yy + 2.8, r[2], size=1.95)
        sh.text(x + 153.0, yy + 2.8, r[3], size=1.95, anchor="middle")
        sh.text(x + 176.0, yy + 2.8, r[4], size=1.95, anchor="middle")
        sh.line(x, yy, x + w, yy, "thin")
        yy += rh
    sh.line(x, yy, x + w, yy, "visible")
    for cx in cols[1:-1]:
        sh.line(x + cx, y, x + cx, yy, "thin")
    sh.line(x, y, x, yy, "visible")
    sh.line(x + w, y, x + w, yy, "visible")
    return yy


def sheet_list_block(sh, x, y, w=120.0):
    sh.text(x, y, "DAFTAR LEMBAR GAMBAR :", size=2.6, bold=True)
    yy = y + 4.6
    for no, t in D.SHEETS:
        sh.text(x + 1.0, yy, no, size=2.1, bold=True)
        sh.text(x + 13.0, yy, t, size=2.1)
        sh.line(x, yy + 1.6, x + w, yy + 1.6, "thin")
        yy += 3.9
    return yy


def kop_sheet(sh, judul):
    sh.border()
    sh.sign_block(227.0, 246.0)
    sh.title_block(227.0, 255.0, judul=judul)
    sh.text(28.0, 285.5, f"{sh.doc_no} — {sh.title}", size=2.2, bold=True, color="#666666")
    sh.text(412.0 - 1.5, 285.5, "SEMUA UKURAN DALAM mm", size=2.0, anchor="end", color="#666666")


def plan_common(sh, show_modules="solid", show_ghost=False, show_frame=False,
                show_beton=False, show_beton_only=False, show_floor=False,
                show_box=False, show_braces=False, show_plates=False,
                plates_solid=False, legs_solid=False):
    """Gambar rencana bersama sesuai kombinasi layer."""
    xL, xR = mx(0), mx(D.ARR_L)
    yT, yB = my(0), my(D.PLAN_D)

    if show_floor:
        fx0, fx1 = mx(-500), mx(D.ARR_L + 500)
        fy0, fy1 = my(-450), my(D.PLAN_D + 450)
        sh.rect(fx0, fy0, fx1 - fx0, fy1 - fy0, "hidden", dash="2,1.2")
        sh.leader(fx0 + 3, fy0 + 1.5, [(fx0 - 4, fy0 - 3)], "LANTAI KERJA BETON 10 CM", size=2.0)

    # --- beton ---
    if show_beton or show_beton_only:
        for yc in (D.Y_FRONT, D.Y_REAR):
            yA, yB2 = my(yc - 150), my(yc + 150)
            sh.rect(xL, yA, xR - xL, yB2 - yA, "visible2", fill="#e9e9e6")
            sh.hatch_poly([(xL, yA), (xR, yA), (xR, yB2), (xL, yB2)], spacing=1.1)
        for ax in D.AXES:
            xA, xB2 = mx(ax - 150), mx(ax + 150)
            sh.rect(xA, my(D.Y_FRONT + 150), xB2 - xA,
                    my(D.Y_REAR - 150) - my(D.Y_FRONT + 150), "visible2", fill="#f4f4f2")
            sh.hatch_poly([(xA, my(D.Y_FRONT + 150)), (xB2, my(D.Y_FRONT + 150)),
                           (xB2, my(D.Y_REAR - 150)), (xA, my(D.Y_REAR - 150))],
                          spacing=1.1, phase=0.55)
        # pondasi (tersembunyi)
        for ax in D.AXES:
            for yc in (D.Y_FRONT, D.Y_REAR):
                sh.rect(mx(ax - 300), my(yc - 300), ph(600), ph(600), "hidden", dash="2,1")
    # --- rangka ---
    if show_frame:
        # rail
        for yc in (D.Y_FRONT, D.Y_REAR):
            yA, yB2 = my(yc - 10), my(yc + 10)
            sh.rect(xL, yA, xR - xL, yB2 - yA, "visible", fill="#1a1a1a")
        # kaki (di bawah rail -> putus2)
        for ax in D.AXES:
            for yc in (D.Y_FRONT, D.Y_REAR):
                st = "visible" if legs_solid else "hidden"
                dash = None if legs_solid else "2,1"
                sh.rect(mx(ax - 10), my(yc - 20), ph(D.LEG_EW), ph(D.LEG_NS), st,
                        fill="#777777", dash=dash)
        # plat besi
        for ax in D.AXES:
            for yc in (D.Y_FRONT, D.Y_REAR):
                st = "visible" if plates_solid else "hidden"
                dash = None if plates_solid else "2,1"
                sh.rect(mx(ax - 50), my(yc - 50), ph(D.PLATE), ph(D.PLATE), st, dash=dash)
        # pengaku (di bawah rail, terlihat)
        if show_braces:
            for ax in D.AXES:
                sh.line(mx(ax), my(D.Y_FRONT + 25), mx(ax), my(D.Y_REAR - 25), "visible2")
        # box panel control
        if show_box:
            bx0, by0 = mx(D.BOX_XC - D.BOX_EW / 2), my(D.BOX_YC - D.BOX_NS / 2)
            sh.rect(bx0, by0, ph(D.BOX_EW), ph(D.BOX_NS), "visible", fill="#c9cdd2")
            sh.line(bx0, by0 + ph(D.BOX_NS) / 2, bx0 + ph(D.BOX_EW), by0 + ph(D.BOX_NS) / 2,
                    "visible2", dash="1.5,1")
    # --- modul ---
    if show_ghost:
        sh.rect(xL, yT, xR - xL, yB - yT, "thin", fill="none", dash="2,1.2")
        sh.text(xL + 1.2, yT + 2.4, "PROYEKSI MODUL SURYA (disamarkan)", size=1.7,
                color="#888888")
    if show_modules == "solid":
        for i in range(D.N_MOD):
            xA = mx(i * D.MOD_W)
            w = D.MOD_W * S
            sh.rect(xA, yT, w, yB - yT, "visible", fill="#3d4f60")
            if w > 8:
                for k in range(1, 6):  # 6 jalur sel
                    yy = yT + (yB - yT) * k / 6.0
                    sh.line(xA, yy, xA + w, yy, "thin", color="#9fb2c4")
            if i > 0:
                sh.line(xA, yT, xA, yB, "thin", color="#e8eef4")
        # arah kemiringan
        xcc = (xL + xR) / 2
        sh.text(xcc, yT - 2.6, "ARAH KEMIRINGAN 15\u00b0 \u2192 SELATAN", size=1.9,
                anchor="middle", color="#555555")

    # sumbu
    for ax in D.AXES:
        sh.line(mx(ax), yT - 5.5, mx(ax), yB + 5.5, "center", dash="4,0.8,0.8")
    for yc in (D.Y_FRONT, D.Y_REAR):
        sh.line(xL - 5.5, my(yc), xR + 5.5, my(yc), "center", dash="4,0.8,0.8")


def plan_dims(sh, overall_bottom=True):
    xL, xR = mx(0), mx(D.ARR_L)
    yT, yB = my(0), my(D.PLAN_D)
    # atas: rantai modul + total
    ticks = [mx(i * D.MOD_W) for i in range(D.N_MOD + 1)]
    sh.dim_h(xL, xR, yT - 14.0, "5670", ext_from=(yT - 5.5, yT - 5.5))
    yy = yT - 8.0
    sh.line(xL, yy, xR, yy, "dim")
    sh._arrow(xL, yy, 0)
    sh._arrow(xR, yy, 180)
    for tx in ticks[:-1]:
        sh._arrow(tx, yy, 0)
        sh._arrow(tx, yy, 180)
    for i in range(D.N_MOD):
        sh.text((ticks[i] + ticks[i + 1]) / 2, yy - 0.8, "1134", size=2.2, anchor="middle")
    # bawah: sumbu
    yb1 = yB + 8.0
    for (xa, xb, lbl) in [(mx(0), mx(D.AXES[0]), "550"),
                           (mx(D.AXES[0]), mx(D.AXES[1]), "2285"),
                           (mx(D.AXES[1]), mx(D.AXES[2]), "2285"),
                           (mx(D.AXES[2]), xR, "550")]:
        sh.dim_h(xa, xb, yb1, lbl, ext_from=(yB + 5.5, yB + 5.5))
    if overall_bottom:
        sh.dim_h(xL, xR, yb1 + 7.0, "5670", ext_from=(yb1, yb1))
    # kiri: kedalaman
    sh.dim_v(yT, yB, xL - 6.0, "2200", ext_from=(xL - 5.5, xL - 5.5))
    # kanan: baris kaki
    sh.dim_v(my(D.Y_FRONT), my(D.Y_REAR), xR + 6.0, "990", ext_from=(xR + 5.5, xR + 5.5))
    sh.dim_v(yT, my(D.Y_FRONT), xR + 12.5, "605", ext_from=(xR + 11.5, xR + 5.5))
    sh.dim_v(my(D.Y_REAR), yB, xR + 12.5, "605", ext_from=(xR + 5.5, xR + 11.5))


def axis_bubbles(sh, rows=True):
    for ax, lbl in zip(D.AXES, ["1", "2", "3"]):
        sh.axis_bubble(mx(ax), my(0) - 19.5, lbl)
    if rows:
        sh.axis_bubble(mx(0) - 12.5, my(D.Y_FRONT), "A")
        sh.axis_bubble(mx(0) - 12.5, my(D.Y_REAR), "B")


# ---------------------------------------------------------------- G-01
def g01():
    sh = Sheet("TAMPAK ATAS", "G-01")
    kop_sheet(sh, "TAMPAK ATAS — RENCANA SUSUNAN MODUL")
    plan_common(sh, show_modules="solid")
    plan_dims(sh)
    axis_bubbles(sh)

    # potongan A-A (vertikal di sumbu 2, arah pandang ke TIMUR)
    xs = mx(D.AXES[1])
    sh.section_mark(xs, my(0) - 4.0, xs, my(D.PLAN_D) + 4.0, "A")
    # arah pandang tampak depan (dari utara, melihat ke selatan)
    sh.view_dir(mx(0) - 17.0, my(D.PLAN_D) + 16.0, "TAMPAK DEPAN", deg=90, size=1.8)

    # panah utara
    sh.north_arrow(mx(D.ARR_L) + 38.0, my(0) - 14.0)
    sh.text(mx(D.ARR_L) + 38.0, my(0) + 0.5, "PANEL MENGHADAP UTARA", size=2.0, anchor="middle")
    sh.text(mx(D.ARR_L) + 38.0, my(0) + 3.2, "(azimuth 0\u00b0 — sesuaikan site)", size=1.8,
            anchor="middle", color="#666666")

    # label modul (menunjuk ke kanan, bebas dari dimensi)
    sh.leader(mx(4.7 * D.MOD_W), my(D.PLAN_D * 0.42), [(mx(D.ARR_L) + 7.5, my(D.PLAN_D * 0.42))],
              "MODUL SURYA 550 Wp", size=2.3, bold=True,
              split="2278 x 1134 x 35 mm — 5 UNIT (2,75 kWp)",
              size2=2.0, anchor="start")

    title_under(sh, (mx(0) + mx(D.ARR_L)) / 2, my(D.PLAN_D) + 30.0, "TAMPAK ATAS")

    # kolom kanan
    yend = bom_table(sh, 195.0, 16.0)
    notes_block(sh, 195.0, yend + 6.0, 215.0)
    legend_block(sh, 320.0, 132.0)
    sheet_list_block(sh, 195.0, 205.0)
    return sh


# ---------------------------------------------------------------- G-04
def g04():
    sh = Sheet("TAMPAK ATAS — PANEL SURYA DISAMARKAN (RANGKA)", "G-04")
    kop_sheet(sh, "TAMPAK ATAS — RANGKA PANEL (PANEL DISAMARKAN)")
    plan_common(sh, show_ghost=True, show_frame=True, show_braces=True, show_box=True)
    plan_dims(sh, overall_bottom=False)
    axis_bubbles(sh)
    sh.dim_h(mx(D.AXES[0] - 50), mx(D.AXES[0] + 50), my(D.Y_FRONT) + 8.0, "100",
              ext_from=(my(D.Y_FRONT) + 5.5, my(D.Y_FRONT) + 5.5))

    xR = mx(D.ARR_L)
    # callout rangka (posisi bebas-tabrakan)
    sh.leader(mx(D.AXES[0]), my(D.Y_FRONT) - 0.4, [(42.0, 79.0), (21.5, 79.0)],
              "RAIL MEMANJANG BAJA HOLLOW", size=2.2, split="GALVANIS 40 x 20 mm (2 BH x 5,67 m)",
              size2=2.0, anchor="start")
    sh.leader(mx(D.AXES[2]), my(D.Y_FRONT) - 0.6, [(108.0, 80.5), (117.5, 80.5)],
              "KAKI RANGKA HOLLOW 40 x 20", size=2.2, split="6 TITIK (sumbu 1-2-3, baris A-B)",
              size2=2.0, anchor="start")
    sh.leader(mx(D.AXES[2]), my(D.Y_REAR - 45), [(112.0, 99.5), (117.5, 99.5)],
              "PENGAKU DIAGONAL 40 x 20", size=2.2, split="3 BH (satu per rangka)",
              size2=2.0, anchor="start")
    bx0 = mx(D.BOX_XC - D.BOX_EW / 2)
    sh.leader(bx0 + ph(D.BOX_EW) - 0.5, my(D.BOX_YC) + 1.0, [(100.0, 107.0), (101.2, 107.0)],
              "BOX PANEL CONTROL", size=2.2, split="(dipasang pada rangka tengah)",
              size2=2.0, anchor="start")
    sh.leader(mx(D.AXES[1]), my(D.Y_FRONT) + 0.8, [(76.0, 105.5)],
              "SAMBUNGAN RANGKA DILAS", size=2.2, bold=True,
              split="(lihat DETAIL A — G-02)", size2=2.0, anchor="end")

    title_under(sh, (mx(0) + xR) / 2, my(D.PLAN_D) + 30.0, "TAMPAK ATAS — RANGKA PANEL")

    # tabel batang
    sh.text(195.0, 22.0, "DAFTAR BATANG RANGKA :", size=2.6, bold=True)
    rows = [
        ("K-1", "Kaki depan (baris A)", "Hollow 40 x 20", "3", "1.090 m"),
        ("K-2", "Kaki belakang (baris B)", "Hollow 40 x 20", "3", "1.355 m"),
        ("R-1", "Rail memanjang", "Hollow 40 x 20", "2", "5.670 m"),
        ("P-1", "Pengaku diagonal", "Hollow 40 x 20", "3", "1.340 m"),
        ("P-2", "Braket dudukan box", "Hollow 40 x 20", "2", "0.350 m"),
        ("PL-1", "Plat besi alas kaki", "Plat 5 mm, 100 x 100", "6", "—"),
    ]
    cols = [0.0, 14.0, 78.0, 132.0, 158.0, 180.0, 198.0]
    x, y = 195.0, 26.0
    sh.rect(x, y, 198.0, 4.2, "visible", fill="#e8ecef")
    for cx, hd, anc in [(2.0, "KODE", "start"), (16.0, "URAIAN", "start"),
                        (79.5, "PENAMPANG", "start"), (140.0, "JML", "middle"),
                        (169.0, "PANJANG", "middle")]:
        sh.text(x + cx, y + 2.9, hd, size=1.9, bold=True, anchor=anc)
    yy = y + 4.2
    for r in rows:
        sh.text(x + 2.0, yy + 2.7, r[0], size=1.95, bold=True)
        sh.text(x + 16.0, yy + 2.7, r[1], size=1.95)
        sh.text(x + 79.5, yy + 2.7, r[2], size=1.95)
        sh.text(x + 140.0, yy + 2.7, r[3], size=1.95, anchor="middle")
        sh.text(x + 169.0, yy + 2.7, r[4], size=1.95, anchor="middle")
        sh.line(x, yy, x + 198.0, yy, "thin")
        yy += 3.9
    for cx in cols[1:-1]:
        sh.line(x + cx, y, x + cx, yy, "thin")
    sh.line(x, yy, x + 198.0, yy, "visible")
    sh.rect(x, y, 198.0, yy - y, "visible")

    notes_block(sh, 195.0, yy + 8.0, 215.0)
    legend_block(sh, 320.0, 168.0)
    return sh


# ---------------------------------------------------------------- G-05
def g05():
    sh = Sheet("TAMPAK ATAS — PANEL DIHILANGKAN (RANGKA & BETON)", "G-05")
    kop_sheet(sh, "TAMPAK ATAS — RANGKA PANEL & STRUKTUR BETON")
    plan_common(sh, show_ghost=True, show_frame=True, show_braces=True, show_box=True,
                show_beton=True, show_floor=True)
    plan_dims(sh, overall_bottom=False)
    axis_bubbles(sh)
    sh.dim_h(mx(D.AXES[1] - 150), mx(D.AXES[1] + 150), my(D.Y_FRONT) + 8.0, "300",
              ext_from=(my(D.Y_FRONT) + 5.5, my(D.Y_FRONT) + 5.5))
    sh.dim_v(my(D.Y_FRONT - 150), my(D.Y_FRONT + 150), mx(0) - 12.0, "300",
             ext_from=(mx(0) - 5.5, mx(0) - 5.5))

    xR = mx(D.ARR_L)
    sh.leader(mx(600), my(D.Y_FRONT - 150), [(42.0, 80.0), (21.5, 80.0)],
              "BALOK PONDASI RANGKA (SLOOF)", size=2.2, split="BETON 30/25 — K-225 — 2 BH x 5,67 m",
              size2=2.0, anchor="start")
    sh.leader(mx(3200), my(D.Y_FRONT - 150) - 0.2, [(112.0, 72.5), (117.0, 72.5)],
              "BESI TULANGAN \u00d88 mm, SENGKANG \u00d88 JARAK 15 cm", size=2.2, bold=True,
              split="SEMUA STRUKTUR BETON DISATUKAN (MONOLIT)", size2=2.0, anchor="start")
    sh.leader(mx(D.AXES[1] + 60), my((D.Y_FRONT + D.Y_REAR) / 2),
              [(110.0, 96.5), (117.0, 96.5)],
              "BALOK IKAT MELINTANG 30/25", size=2.2, split="3 BH — MONOLIT DENGAN SLOOF",
              size2=2.0, anchor="start")
    sh.leader(mx(D.AXES[2]), my(D.Y_REAR) - 0.5, [(112.0, 102.5), (117.0, 102.5)],
              "KAKI DI ATAS PLAT BESI 5 mm", size=2.2, split="+ DYNABOLT M12 (4 BH/TITIK)",
              size2=2.0, anchor="start")
    sh.leader(mx(D.AXES[2] + 300) - 0.3, my(D.Y_REAR + 300) - 0.4,
              [(112.0, 106.5), (117.0, 106.5)],
              "PONDASI BATU KALI 60 x 60", size=2.2, split="DALAM 50 cm (6 TITIK)",
              size2=2.0, anchor="start")

    title_under(sh, (mx(0) + xR) / 2, my(D.PLAN_D) + 42.0, "TAMPAK ATAS — RANGKA & BETON")

    yend = notes_block(sh, 195.0, 22.0, 215.0)
    legend_block(sh, 320.0, 120.0)
    sheet_list_block(sh, 195.0, 185.0)
    return sh


# ---------------------------------------------------------------- G-06
def g06():
    sh = Sheet("TAMPAK ATAS — PANEL & RANGKA DISAMARKAN (BETON)", "G-06")
    kop_sheet(sh, "TAMPAK ATAS — STRUKTUR BETON (PANEL & RANGKA DISAMARKAN)")
    plan_common(sh, show_beton_only=True, show_plates=True, plates_solid=True, show_floor=True)
    plan_dims(sh, overall_bottom=False)
    axis_bubbles(sh)
    sh.dim_v(my(D.Y_FRONT - 300), my(D.Y_FRONT + 300), mx(D.AXES[0] - 300) - 4.0, "600",
             text_left=True, ext_from=(mx(D.AXES[0] - 300), mx(D.AXES[0] - 300)))

    # plat & dynabolt
    for ax in D.AXES:
        for yc in (D.Y_FRONT, D.Y_REAR):
            sh.rect(mx(ax - 50), my(yc - 50), ph(100), ph(100), "visible", fill="#ffffff")
            for dx in (-25, 25):
                for dy in (-25, 25):
                    sh.circle(mx(ax + dx), my(yc + dy), 0.35, "thin", fill="#1a1a1a")

    xR = mx(D.ARR_L)
    sh.leader(mx(600), my(D.Y_FRONT - 150), [(42.0, 80.0), (21.5, 80.0)],
              "BALOK PONDASI RANGKA (SLOOF BETON)", size=2.2, split="30 x 25 cm — 2 BH x 5,67 m — K-225",
              size2=2.0, anchor="start")
    sh.leader(mx(D.AXES[1] + 60), my((D.Y_FRONT + D.Y_REAR) / 2),
              [(110.0, 96.5), (117.0, 96.5)],
              "BALOK IKAT MELINTANG 30 x 25 cm", size=2.2, split="3 BH (sumbu 1-2-3) — MONOLIT",
              size2=2.0, anchor="start")
    sh.leader(mx(D.AXES[2] + 30), my(D.Y_REAR) - 0.5, [(112.0, 102.0), (117.0, 102.0)],
              "PLAT BESI 5 mm 100 x 100 + DYNABOLT M12", size=2.2, split="alas pijakan rangka (6 titik)",
              size2=2.0, anchor="start")
    sh.leader(mx(D.AXES[2] + 300) - 0.3, my(D.Y_REAR + 300) - 0.4,
              [(112.0, 106.5), (117.0, 106.5)],
              "PONDASI BATU KALI 60 x 60, DALAM 50 cm", size=2.2, split="6 TITIK (putus-putus = tersembunyi)",
              size2=2.0, anchor="start")

    title_under(sh, (mx(0) + mx(D.ARR_L)) / 2, my(D.PLAN_D) + 42.0, "TAMPAK ATAS — STRUKTUR BETON")

    # referensi detail
    sh.text(195.0, 24.0, "PLAT ANGKUR & SAMBUNGAN KAKI:", size=2.6, bold=True)
    sh.text(195.0, 28.6, "LIHAT DETAIL A PADA LEMBAR G-02 (SKALA 1 : 5)", size=2.2, bold=True,
            color="#a04000")
    sh.text(195.0, 33.6, "Plat besi 5 mm 100 x 100 mm diangkur dengan 4 dynabolt M12 ke sloof "
            "pada 6 titik kaki rangka (sumbu 1-2-3, baris A-B).", size=2.05)
    yend = notes_block(sh, 195.0, 44.0, 215.0)
    legend_block(sh, 320.0, 170.0)
    return sh


def xR_extra():
    return mx(D.ARR_L)


def detail_plat(sh, x, y):
    """Detail plat angkur — potongan, skala 1:5 (F = 0.2)."""
    F = 0.2
    sh.text(x, y, "DETAIL B — PLAT ANGKUR KAKI RANGKA", size=2.6, bold=True)
    sh.text(x, y + 3.6, "SKALA 1 : 5", size=2.2)
    # koordinat lokal: 0 = tengah plat di puncak sloof, ke bawah positif
    cx = x + 32.0
    ytop = y + 12.0
    w_sloof, h_sloof = 300 * F, 250 * F
    # sloof (potongan, arsir)
    pts = [(cx - w_sloof / 2, ytop), (cx + w_sloof / 2, ytop),
           (cx + w_sloof / 2, ytop + h_sloof), (cx - w_sloof / 2, ytop + h_sloof)]
    sh.poly(pts, w="visible", close=True)
    sh.hatch_poly(pts, spacing=1.3)
    # plat
    pw, pt = 100 * F, 5 * F
    sh.rect(cx - pw / 2, ytop - pt, pw, pt, "visible", fill="#d8dbe0")
    # kaki
    lw, lh = 40 * F, 46 * F
    sh.rect(cx - lw / 2, ytop - pt - lh, lw, lh, "visible", fill="#c9cdd2")
    sh.line(cx - lw / 2 + 2 * F, ytop - pt - lh + 2 * F, cx + lw / 2 - 2 * F,
            ytop - pt - lh + 2 * F, "visible2")
    # dynabolt kiri & kanan (2 terlihat)
    for bx in (-25 * F, 25 * F):
        bxw = 6 * F  # ringgit
        sh.rect(cx + bx - bxw / 2, ytop - pt, bxw, 100 * F, "visible", fill="#9aa1a9")
        # mur + ring
        sh.rect(cx + bx - 4.5 * F, ytop - pt - 5 * F, 9 * F, 4.5 * F, "visible", fill="#9aa1a9")
    # garis putus kaki
    yb = ytop - pt - lh
    sh.poly([(cx - lw / 2 - 2, yb), (cx - lw / 2 + 3, yb - 3)], w="visible2")
    # dimensi & label
    sh.dim_v(ytop, ytop + h_sloof, cx + w_sloof / 2 + 6.0, "250")
    sh.dim_h(cx - w_sloof / 2, cx + w_sloof / 2, ytop + h_sloof + 6.0, "300",
             ext_from=(ytop + h_sloof, ytop + h_sloof))
    sh.dim_h(cx - pw / 2, cx + pw / 2, ytop - pt - 9.0, "100")
    sh.leader(cx - 25 * F, ytop - pt + 30 * F, [(cx - 44 * F - 6, ytop - pt + 10 * F)],
              "DYNABOLT M12", size=2.0, split="(4 bh / titik)", size2=1.8, anchor="end")
    sh.leader(cx + 25 * F, ytop - pt + 55 * F, [(cx + 46 * F + 6, ytop - pt + 40 * F)],
              "DYNABOLT M12", size=2.0, anchor="start")
    sh.leader(cx - lw / 2 + 4 * F, ytop - pt - lh + 12 * F, [(cx - 10 * F - 14, ytop - pt - lh - 6)],
              "KAKI HOLLOW 40 x 20", size=2.0, anchor="end")
    sh.leader(cx + pw / 2 - 3 * F, ytop - pt / 2, [(cx + pw / 2 + 12, ytop - pt - 4)],
              "PLAT BESI 5 mm", size=2.0, split="100 x 100", size2=1.8, anchor="start")
    sh.text(cx + w_sloof / 2 + 6.0, ytop + h_sloof / 2 + 12, "SLOOF BETON 30/25 (K-225)",
            size=2.0, anchor="start", rot=-90)
    # tanda detail B pada gambar utama
    return None
