# -*- coding: utf-8 -*-
"""sheets_plan.py — Lembar G-01 (tampak atas), G-04 (rangka), G-05 (rangka+beton), G-06 (beton).
Skala tampak atas 1 : 25 (S = 0.04) — gambar diperbesar agar dominan terhadap anotasi.
Tata letak: gambar besar kiri-atas, kolom catatan kanan, tabel di band bawah (di atas kop)."""
import math
import design as D
from svgcad import Sheet

S = 0.04  # 1:25
X0, Y0 = 40.0, 34.0  # origin rencana di kertas (tepi barat, tepi utara)

# kolom kanan (catatan/legenda) dan band bawah (tabel)
COLX = 292.0
COLW = 119.0


def mx(x):
    return X0 + x * S


def my(y):
    return Y0 + y * S


def ph(h):
    """tinggi model (di atas sloof) -> kertas (y makin kecil makin tinggi)."""
    return h * S


# ---------------------------------------------------------------- blok umum
def title_under(sh, cx, y, t1, t2="SKALA 1 : 25"):
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
        fm = 120.0  # margin lantai kerja (mm model) agar dimensi tetap di luar garis
        fx0, fx1 = mx(-fm), mx(D.ARR_L + fm)
        fy0, fy1 = my(-fm), my(D.PLAN_D + fm)
        sh.rect(fx0, fy0, fx1 - fx0, fy1 - fy0, "hidden", dash="2,1.2")
        sh.text(fx0 + 2.0, fy1 - 1.6, "LANTAI KERJA BETON 10 cm (meluas di sekeliling struktur)",
                size=1.9, color="#666666")

    # --- beton ---
    if show_beton or show_beton_only:
        for yc in (D.Y_FRONT, D.Y_REAR):
            yA, yB2 = my(yc - 150), my(yc + 150)
            sh.rect(xL, yA, xR - xL, yB2 - yA, "visible2", fill="#e9e9e6")
            sh.hatch_poly([(xL, yA), (xR, yA), (xR, yB2), (xL, yB2)], spacing=1.6)
        for ax in D.AXES:
            xA, xB2 = mx(ax - 150), mx(ax + 150)
            sh.rect(xA, my(D.Y_FRONT + 150), xB2 - xA,
                    my(D.Y_REAR - 150) - my(D.Y_FRONT + 150), "visible2", fill="#f4f4f2")
            sh.hatch_poly([(xA, my(D.Y_FRONT + 150)), (xB2, my(D.Y_FRONT + 150)),
                           (xB2, my(D.Y_REAR - 150)), (xA, my(D.Y_REAR - 150))],
                          spacing=1.6, phase=0.55)
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
        sh.text(xL + 2.0, yT + 3.4, "PROYEKSI MODUL SURYA (disamarkan)", size=2.0,
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
        # arah kemiringan (digeser dari sumbu 2 agar tidak menabrak garis potongan A-A)
        xcc = (xL + xR) / 2 - 45.0
        sh.text(xcc, yT - 2.6, "ARAH KEMIRINGAN 15\u00b0 \u2192 SELATAN", size=2.0,
                anchor="middle", color="#555555")

    # sumbu (garis sumbu masuk ke dalam balon sumbu)
    for ax in D.AXES:
        sh.line(mx(ax), yT - 16.0, mx(ax), yB + 6.0, "center", dash="4,0.8,0.8")
    for yc in (D.Y_FRONT, D.Y_REAR):
        sh.line(xL - 9.0, my(yc), xR + 7.0, my(yc), "center", dash="4,0.8,0.8")


def plan_dims(sh, overall_bottom=True):
    xL, xR = mx(0), mx(D.ARR_L)
    yT, yB = my(0), my(D.PLAN_D)
    # atas: rantai modul (dalam) + total (luar)
    ticks = [mx(i * D.MOD_W) for i in range(D.N_MOD + 1)]
    sh.dim_h(xL, xR, yT - 13.0, "5670", ext_from=(yT - 3.0, yT - 3.0))
    yy = yT - 7.0
    sh.line(xL, yy, xR, yy, "dim")
    sh._arrow(xL, yy, 0)
    sh._arrow(xR, yy, 180)
    for tx in ticks[:-1]:
        sh._arrow(tx, yy, 0)
        sh._arrow(tx, yy, 180)
    for i in range(D.N_MOD):
        sh.text((ticks[i] + ticks[i + 1]) / 2, yy - 0.8, "1134", size=2.2, anchor="middle")
    # bawah: sumbu
    yb1 = yB + 9.0
    for (xa, xb, lbl) in [(mx(0), mx(D.AXES[0]), "550"),
                           (mx(D.AXES[0]), mx(D.AXES[1]), "2285"),
                           (mx(D.AXES[1]), mx(D.AXES[2]), "2285"),
                           (mx(D.AXES[2]), xR, "550")]:
        sh.dim_h(xa, xb, yb1, lbl, ext_from=(yB + 5.0, yB + 5.0))
    if overall_bottom:
        sh.dim_h(xL, xR, yb1 + 7.0, "5670", ext_from=(yb1, yb1))
    # kiri: kedalaman
    sh.dim_v(yT, yB, xL - 6.0, "2200", ext_from=(xL - 4.0, xL - 4.0))
    # kanan: baris kaki
    sh.dim_v(my(D.Y_FRONT), my(D.Y_REAR), xR + 6.0, "990", ext_from=(xR + 4.0, xR + 4.0))
    sh.dim_v(yT, my(D.Y_FRONT), xR + 12.5, "605", ext_from=(xR + 11.5, xR + 4.0))
    sh.dim_v(my(D.Y_REAR), yB, xR + 12.5, "605", ext_from=(xR + 4.0, xR + 11.5))


def axis_bubbles(sh, rows=True):
    for ax, lbl in zip(D.AXES, ["1", "2", "3"]):
        sh.axis_bubble(mx(ax), my(0) - 20.0, lbl)
    if rows:
        sh.axis_bubble(mx(0) - 12.5, my(D.Y_FRONT), "A")
        sh.axis_bubble(mx(0) - 12.5, my(D.Y_REAR), "B")


# ---------------------------------------------------------------- G-01
def g01():
    sh = Sheet("TAMPAK ATAS", "G-01", scale_txt="1 : 25")
    kop_sheet(sh, "TAMPAK ATAS — RENCANA SUSUNAN MODUL")
    plan_common(sh, show_modules="solid")
    plan_dims(sh)
    axis_bubbles(sh)

    # potongan A-A (vertikal di sumbu 2, arah pandang ke TIMUR)
    xs = mx(D.AXES[1])
    sh.section_mark(xs, my(0) - 4.0, xs, my(D.PLAN_D) + 4.0, "A")
    # arah pandang tampak depan (dari utara, melihat ke selatan)
    sh.view_dir(mx(0) - 8.0, my(D.PLAN_D) + 20.0, "TAMPAK DEPAN", deg=90, size=1.8)

    # label modul sebagai "chip" putih di dalam array (tidak mengganggu dimensi)
    cx, cy = (mx(0) + mx(D.ARR_L)) / 2, (my(0) + my(D.PLAN_D)) / 2
    sh.rect(cx - 29.0, cy - 4.6, 58.0, 9.2, "thin", fill="#ffffff")
    sh.text(cx, cy - 0.9, "MODUL SURYA 550 Wp — 5 UNIT (2,75 kWp)", size=2.3,
            anchor="middle", bold=True)
    sh.text(cx, cy + 2.7, "2278 x 1134 x 35 mm — ORIENTASI PORTRAIT", size=2.0,
            anchor="middle")

    # panah utara (pojok kanan atas lembar)
    sh.north_arrow(388.0, 24.0)
    sh.text(388.0, 41.0, "PANEL MENGHADAP UTARA", size=2.0, anchor="middle")
    sh.text(388.0, 44.2, "(azimuth 0\u00b0 — sesuaikan site)", size=1.8,
            anchor="middle", color="#666666")

    title_under(sh, (mx(0) + mx(D.ARR_L)) / 2, 155.0, "TAMPAK ATAS")

    # band bawah: BOM
    bom_table(sh, 24.0, 188.5)
    # kolom kanan: catatan, legenda, daftar lembar
    notes_block(sh, COLX, 50.0, COLW)
    legend_block(sh, COLX, 118.0)
    sheet_list_block(sh, COLX, 154.0, COLW)
    return sh


# ---------------------------------------------------------------- G-04
def g04():
    sh = Sheet("TAMPAK ATAS — PANEL SURYA DISAMARKAN (RANGKA)", "G-04", scale_txt="1 : 25")
    kop_sheet(sh, "TAMPAK ATAS — RANGKA PANEL (PANEL DISAMARKAN)")
    plan_common(sh, show_ghost=True, show_frame=True, show_braces=True, show_box=True)
    plan_dims(sh, overall_bottom=False)
    axis_bubbles(sh)
    # dimensi lebar kaki (interior, bebas objek)
    sh.dim_h(mx(D.AXES[0] - 50), mx(D.AXES[0] + 50), my(D.Y_FRONT) + 6.5, "100",
             ext_from=(my(D.Y_FRONT) + 2.0, my(D.Y_FRONT) + 2.0))

    # callout rangka — ditempatkan di area interior rencana yang kosong
    sh.leader(mx(2500), my(D.Y_FRONT), [(110.0, 70.0)],
              "RAIL MEMANJANG BAJA HOLLOW", size=2.2,
              split="GALVANIS 40 x 20 mm (2 BH x 5,67 m)", size2=2.0, anchor="start")
    sh.leader(mx(D.AXES[2]), my(D.Y_FRONT) + 0.8, [(238.0, 72.0)],
              "KAKI RANGKA HOLLOW 40 x 20", size=2.2,
              split="6 TITIK (sumbu 1-2-3, baris A-B)", size2=2.0, anchor="end")
    sh.leader(mx(D.AXES[0]), my(1100), [(75.0, 86.0)],
              "PENGAKU DIAGONAL 40 x 20", size=2.2,
              split="3 BH (satu per rangka)", size2=2.0, anchor="start")
    bx0 = mx(D.BOX_XC - D.BOX_EW / 2)
    sh.leader(bx0 + ph(D.BOX_EW), my(D.BOX_YC), [(170.0, 90.0)],
              "BOX PANEL CONTROL", size=2.2,
              split="(dipasang pada rangka tengah)", size2=2.0, anchor="start")
    sh.leader(mx(D.AXES[1]), my(D.Y_FRONT) + 1.5, [(160.0, 64.0)],
              "SAMBUNGAN RANGKA DILAS", size=2.2, bold=True,
              split="(lihat DETAIL A — G-02)", size2=2.0, anchor="start")

    title_under(sh, (mx(0) + mx(D.ARR_L)) / 2, 155.0, "TAMPAK ATAS — RANGKA PANEL")

    # band bawah: tabel batang
    sh.text(24.0, 165.5, "DAFTAR BATANG RANGKA :", size=2.6, bold=True)
    rows = [
        ("K-1", "Kaki depan (baris A)", "Hollow 40 x 20", "3", "1.090 m"),
        ("K-2", "Kaki belakang (baris B)", "Hollow 40 x 20", "3", "1.355 m"),
        ("R-1", "Rail memanjang", "Hollow 40 x 20", "2", "5.670 m"),
        ("P-1", "Pengaku diagonal", "Hollow 40 x 20", "3", "1.340 m"),
        ("P-2", "Braket dudukan box", "Hollow 40 x 20", "2", "0.350 m"),
        ("PL-1", "Plat besi alas kaki", "Plat 5 mm, 100 x 100", "6", "—"),
    ]
    cols = [0.0, 14.0, 78.0, 132.0, 158.0, 180.0, 198.0]
    x, y = 24.0, 168.0
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

    notes_block(sh, COLX, 44.0, COLW)
    legend_block(sh, COLX, 114.0)
    return sh


# ---------------------------------------------------------------- G-05
def g05():
    sh = Sheet("TAMPAK ATAS — PANEL DIHILANGKAN (RANGKA & BETON)", "G-05", scale_txt="1 : 25")
    kop_sheet(sh, "TAMPAK ATAS — RANGKA PANEL & STRUKTUR BETON")
    plan_common(sh, show_ghost=True, show_frame=True, show_braces=True, show_box=True,
                show_beton=True, show_floor=True)
    plan_dims(sh, overall_bottom=False)
    axis_bubbles(sh)
    # dimensi balok ikat (interior, di atas balok ikat sumbu 2)
    sh.dim_h(mx(D.AXES[1] - 150), mx(D.AXES[1] + 150), my(D.Y_FRONT + 150) + 4.0, "300",
             ext_from=(my(D.Y_FRONT + 150) + 1.0, my(D.Y_FRONT + 150) + 1.0))

    # callout di area interior yang kosong (atas: zona bebas pondasi; bawah: bawah sloof B)
    sh.leader(100.0, my(D.Y_FRONT - 150), [(105.0, 45.0)],
              "BALOK PONDASI RANGKA (SLOOF)", size=2.2,
              split="BETON 30/25 — K-225 — 2 BH x 5,67 m", size2=2.0, anchor="start")
    sh.leader(mx(D.AXES[1]), 88.0, [(175.0, 113.0)],
              "BESI TULANGAN \u00d88 mm, SENGKANG \u00d88 JARAK 15 cm", size=2.2, bold=True,
              split="SEMUA STRUKTUR BETON DISATUKAN (MONOLIT)", size2=2.0, anchor="start")
    sh.leader(mx(D.AXES[1]), 66.0, [(170.0, 47.0)],
              "BALOK IKAT MELINTANG 30/25", size=2.2,
              split="3 BH — MONOLIT DENGAN SLOOF", size2=2.0, anchor="start")
    sh.leader(mx(D.AXES[2]), my(D.Y_REAR) + 0.8, [(226.0, 110.0)],
              "KAKI DI ATAS PLAT BESI 5 mm", size=2.2,
              split="+ DYNABOLT M12 (4 BH/TITIK)", size2=2.0, anchor="end")
    sh.leader(mx(D.AXES[2] + 300), my(D.Y_REAR + 300) - 0.5, [(262.0, 116.0)],
              "PONDASI BATU KALI 60 x 60", size=2.2,
              split="DALAM 50 cm (6 TITIK)", size2=2.0, anchor="start")

    title_under(sh, (mx(0) + mx(D.ARR_L)) / 2, 155.0, "TAMPAK ATAS — RANGKA & BETON")

    notes_block(sh, COLX, 44.0, COLW)
    legend_block(sh, COLX, 114.0)
    sheet_list_block(sh, COLX, 152.0, COLW)
    return sh


# ---------------------------------------------------------------- G-06
def g06():
    sh = Sheet("TAMPAK ATAS — PANEL & RANGKA DISAMARKAN (BETON)", "G-06", scale_txt="1 : 25")
    kop_sheet(sh, "TAMPAK ATAS — STRUKTUR BETON (PANEL & RANGKA DISAMARKAN)")
    plan_common(sh, show_beton_only=True, show_plates=True, plates_solid=True, show_floor=True)
    plan_dims(sh, overall_bottom=False)
    axis_bubbles(sh)

    # plat & dynabolt (4 titik angkur per plat, proporsional skala 1:25)
    for ax in D.AXES:
        for yc in (D.Y_FRONT, D.Y_REAR):
            sh.rect(mx(ax - 50), my(yc - 50), ph(100), ph(100), "visible", fill="#ffffff")
            for dx in (-25, 25):
                for dy in (-25, 25):
                    sh.circle(mx(ax + dx), my(yc + dy), 0.4, "thin", fill="#1a1a1a")

    sh.leader(100.0, my(D.Y_FRONT - 150), [(105.0, 45.0)],
              "BALOK PONDASI RANGKA (SLOOF BETON)", size=2.2,
              split="30 x 25 cm — 2 BH x 5,67 m — K-225", size2=2.0, anchor="start")
    sh.leader(mx(D.AXES[1]), 66.0, [(170.0, 47.0)],
              "BALOK IKAT MELINTANG 30 x 25 cm", size=2.2,
              split="3 BH (sumbu 1-2-3) — MONOLIT", size2=2.0, anchor="start")
    sh.leader(245.0, 99.0, [(250.0, 116.0)],
              "PLAT BESI 5 mm 100 x 100", size=2.2,
              split="+ DYNABOLT M12 (6 TITIK)", size2=2.0, anchor="start")
    sh.leader(mx(D.AXES[2] + 300) - 0.5, my(D.Y_FRONT - 300) + 0.5, [(262.0, 38.0)],
              "PONDASI BATU KALI 60 x 60", size=2.2,
              split="DALAM 50 cm (6 TITIK)", size2=2.0, anchor="start")

    title_under(sh, (mx(0) + mx(D.ARR_L)) / 2, 155.0, "TAMPAK ATAS — STRUKTUR BETON")

    # band bawah: referensi detail + catatan (lebar penuh -> lebih ringkas)
    sh.text(24.0, 168.0, "PLAT ANGKUR & SAMBUNGAN KAKI:", size=2.6, bold=True)
    sh.text(24.0, 172.6, "LIHAT DETAIL A PADA LEMBAR G-02 (SKALA 1 : 5)", size=2.2, bold=True,
            color="#a04000")
    sh.text(24.0, 177.6, "Plat besi 5 mm 100 x 100 mm diangkur dengan 4 dynabolt M12 ke sloof "
            "pada 6 titik kaki rangka (sumbu 1-2-3, baris A-B).", size=2.05)
    notes_block(sh, 24.0, 184.0, 215.0)
    legend_block(sh, COLX, 44.0)
    sheet_list_block(sh, COLX, 82.0, COLW)
    return sh
