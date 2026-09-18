# -*- coding: utf-8 -*-
"""svgcad.py — Mini CAD library untuk gambar teknik SVG (koordinat kertas dalam mm, y ke bawah).
Digunakan untuk menghasilkan gambar kerja PLTS Ground Mount 2,75 kWp (A3, multi-skala)."""

import math

FONT = "Liberation Sans, Arial, sans-serif"

# ---------------- gaya garis (ketebalan mm kertas) ----------------
LW = {
    "visible":  0.50,   # garis benda terlihat (tebal)
    "visible2": 0.35,   # garis benda sekunder
    "hidden":   0.30,   # garis tersembunyi (putus-putus)
    "dim":      0.15,   # garis dimensi / leader
    "center":   0.15,   # garis sumbu (titik-garis)
    "thin":     0.22,   # garis tipis (tick, hatch)
    "frame":    0.70,   # border lembar / potongan beton
    "kop":      0.35,
}


class Sheet:
    """Lembar gambar A3 landscape (420x297 mm). origin kiri-atas."""

    def __init__(self, title, doc_no, scale_txt="1 : 25", date_txt="18-09-2026",
                 unit_txt="mm", rev="0", border_left=20.0, margin=8.0):
        self.W, self.H = 420.0, 297.0
        self.bl, self.m = border_left, margin
        self.el = []  # elemen svg (string)
        self.title = title
        self.doc_no = doc_no
        self.scale_txt = scale_txt
        self.date_txt = date_txt
        self.unit_txt = unit_txt
        self.rev = rev

    # ---------------- primitif ----------------
    def line(self, x1, y1, x2, y2, w="visible", color="#1a1a1a", dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.el.append(
            f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
            f'stroke="{color}" stroke-width="{LW[w]}" stroke-linecap="round"{d}/>')

    def poly(self, pts, w="visible", color="#1a1a1a", close=False, fill="none", dash=None):
        s = "M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in pts)
        if close:
            s += " Z"
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.el.append(
            f'<path d="{s}" fill="{fill}" stroke="{color}" stroke-width="{LW[w]}" '
            f'stroke-linejoin="round" stroke-linecap="round"{d}/>')

    def rect(self, x, y, w, h, st="visible", fill="none", color="#1a1a1a", rx=None, dash=None):
        dash_s = f' stroke-dasharray="{dash}"' if dash else ""
        r = f' rx="{rx}"' if rx else ""
        self.el.append(
            f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}"{r} '
            f'fill="{fill}" stroke="{color}" stroke-width="{LW[st]}"{dash_s}/>')

    def circle(self, cx, cy, r, st="visible", fill="none", color="#1a1a1a", dash=None):
        dash_s = ' stroke-dasharray="%s"' % dash if dash else ''
        self.el.append(
            f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" fill="{fill}" '
            f'stroke="{color}" stroke-width="{LW[st]}"{dash_s}/>')

    def text(self, x, y, s, size=2.5, anchor="start", color="#1a1a1a", bold=False,
             rot=None, spacing=None):
        """y = baseline. rot derajat searah jarum jam sekitar (x,y)."""
        b = ' font-weight="bold"' if bold else ""
        ls = f' letter-spacing="{spacing}"' if spacing else ""
        tr = f' transform="rotate({rot} {x:.2f} {y:.2f})"' if rot is not None else ""
        self.el.append(
            f'<text x="{x:.2f}" y="{y:.2f}" font-family="{FONT}" font-size="{size:.2f}" '
            f'fill="{color}" text-anchor="{anchor}"{b}{ls}{tr}>{_esc(s)}</text>')

    # ---------------- dimensi ----------------
    def _arrow(self, x, y, ang, size=1.6, color="#1a1a1a"):
        a1, a2 = ang + math.radians(160), ang - math.radians(160)
        p = [(x, y),
             (x + size * math.cos(a1), y + size * math.sin(a1)),
             (x + size * math.cos(a2), y + size * math.sin(a2))]
        s = "M" + " L".join(f"{px:.2f},{py:.2f}" for px, py in p) + " Z"
        self.el.append(f'<path d="{s}" fill="{color}" stroke="none"/>')

    def dim_h(self, x1, x2, y, label=None, ext_from=None, text_size=2.2, offset_text=0.75,
              ticks=None, color="#1a1a1a", flip_text=False):
        """Dimensi horizontal pada ketinggian y. ext_from: list 2 titik y awal garis bantu."""
        if x2 < x1:
            x1, x2 = x2, x1
        lbl = label if label is not None else f"{abs(x2-x1):g}"
        if ext_from:
            y0a, y0b = ext_from
            self.line(x1, y0a, x1, y - (0.9 if y > y0a else -0.9), "dim", color)
            self.line(x2, y0b, x2, y - (0.9 if y > y0b else -0.9), "dim", color)
        self.line(x1, y, x2, y, "dim", color)
        self._arrow(x1, y, 0 if x2 >= x1 else 180, color=color)
        self._arrow(x2, y, 180 if x2 >= x1 else 0, color=color)
        ty = y - offset_text if not flip_text else y + offset_text + text_size * 0.1
        self.text((x1 + x2) / 2, ty, lbl, size=text_size, anchor="middle", color=color)
        if ticks:
            for tx in ticks:
                self.line(tx, y - 0.8, tx, y + 0.8, "thin", color)

    def dim_v(self, y1, y2, x, label=None, ext_from=None, text_size=2.2, color="#1a1a1a",
              text_left=False, offset=1.4):
        if y2 < y1:
            y1, y2 = y2, y1
        lbl = label if label is not None else f"{abs(y2-y1):g}"
        if ext_from:
            x0a, x0b = ext_from
            self.line(x0a, y1, x - (0.9 if x > x0a else -0.9), y1, "dim", color)
            self.line(x0b, y2, x - (0.9 if x > x0b else -0.9), y2, "dim", color)
        self.line(x, y1, x, y2, "dim", color)
        self._arrow(x, y1, 90, color=color)
        self._arrow(x, y2, -90, color=color)
        tx = x - offset if not text_left else x + offset
        self.text(tx, (y1 + y2) / 2, lbl, size=text_size, anchor="middle", rot=-90, color=color)

    def dim_aligned(self, p1, p2, label, offset=2.5, text_size=2.2, color="#1a1a1a"):
        """Dimensi sejajar garis p1-p2. offset ke kiri arah normal."""
        x1, y1 = p1
        x2, y2 = p2
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy)
        ang = math.atan2(dy, dx)
        nx, ny = dy / L, -dx / L  # normal kiri
        a = (x1 + nx * offset, y1 + ny * offset)
        b = (x2 + nx * offset, y2 + ny * offset)
        self.line(x1 + nx * 0.8, y1 + ny * 0.8, a[0], a[1], "dim", color)
        self.line(x2 + nx * 0.8, y2 + ny * 0.8, b[0], b[1], "dim", color)
        self.line(a[0], a[1], b[0], b[1], "dim", color)
        self._arrow(a[0], a[1], ang, color=color)
        self._arrow(b[0], b[1], ang + math.pi, color=color)
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        deg = math.degrees(ang)
        if deg > 90 or deg < -90:
            deg += 180
        self.text(mx, my, label, size=text_size, anchor="middle", rot=deg, color=color)

    # ---------------- leader & callout ----------------
    def leader(self, px, py, pts, text, size=2.3, anchor="start", bold=False,
               color="#1a1a1a", arrow=True, dy_text=0.0, split=None, size2=None):
        """pts: titik-titik patahan leader setelah (px,py). text di ujung akhir."""
        path = [(px, py)] + list(pts)
        for i in range(len(path) - 1):
            self.line(path[i][0], path[i][1], path[i + 1][0], path[i + 1][1], "dim", color)
        if arrow:
            dx, dy = path[1][0] - px, path[1][1] - py
            self._arrow(px, py, math.atan2(dy, dx), 1.5, color)
        ex, ey = path[-1]
        if split:
            # dua baris, keduanya DI ATAS garis leader horizontal
            self.text(ex + (0.7 if anchor == "start" else -0.7), ey - 1.3, split,
                      size=size, anchor=anchor, bold=bold, color=color)
            self.text(ex + (0.7 if anchor == "start" else -0.7), ey - 1.3 - size * 1.3,
                      text, size=size2 or size, anchor=anchor, bold=bold, color=color)
        else:
            self.text(ex + (0.7 if anchor == "start" else -0.7), ey - 0.6 + dy_text, text,
                      size=size, anchor=anchor, bold=bold, color=color)

    # ---------------- hatch ----------------
    def hatch_poly(self, pts, spacing=1.4, ang=45, w="thin", color="#1a1a1a", phase=0.0):
        """Arsir poligon tertutup (pts list (x,y)) dengan garis miring."""
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        x0, y0, x1, y1 = min(xs), min(ys), max(xs), max(ys)
        key = (tuple(round(px, 1) for px, py in pts), round(phase, 2), spacing)
        idp = "h" + str(abs(hash(key)) & 0xffffff)
        s = "M" + " L".join(f"{px:.2f},{py:.2f}" for px, py in pts) + " Z"
        self.el.append(f'<defs><clipPath id="{idp}"><path d="{s}"/></clipPath></defs>')
        ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        diag = math.hypot(x1 - x0, y1 - y0)
        n = int(diag / spacing) + 2
        for i in range(-n, n + 1):
            o = i * spacing + phase
            px, py = cx - sa * o, cy + ca * o
            lines = (f'<line x1="{px - ca * diag:.2f}" y1="{py - sa * diag:.2f}" '
                     f'x2="{px + ca * diag:.2f}" y2="{py + sa * diag:.2f}" '
                     f'stroke="{color}" stroke-width="{LW[w]}" clip-path="url(#{idp})"/>')
            self.el.append(lines)

    def earth_hatch(self, x0, x1, y, depth=2.5, spacing=1.6, color="#1a1a1a"):
        """Arsir tanah di bawah garis tanah (pola miring pendek)."""
        self.line(x0, y, x1, y, "thin", color)
        x = x0
        while x < x1:
            self.line(x, y, x + 0.9, y + depth * 0.4, "thin", color)
            x += spacing

    # ---------------- simbol ----------------
    def north_arrow(self, cx, cy, r=7.0):
        self.circle(cx, cy, r, "dim")
        self.poly([(cx, cy - r + 0.8), (cx - r * 0.32, cy + r * 0.42), (cx, cy + r * 0.1),
                   (cx + r * 0.32, cy + r * 0.42)], w="visible", close=True, fill="#1a1a1a")
        self.text(cx, cy - r - 1.0, "U", size=3.6, anchor="middle", bold=True)
        self.text(cx, cy + r + 3.0, "UTARA", size=2.0, anchor="middle")

    def axis_bubble(self, x, y, label, r=3.2):
        self.circle(x, y, r, "thin")
        self.text(x, y + 1.1, label, size=2.6, anchor="middle", bold=True)

    def level_mark(self, x, y, label, side="left", color="#1a1a1a"):
        """Simbol elevasi segitiga pada garis level."""
        s = 1.6
        if side == "left":
            self.poly([(x - s, y), (x, y), (x, y + s * 0.8)], w="thin", close=True, color=color)
            self.line(x, y, x + 6, y, "dim", color)
            self.text(x + 6.4, y - 0.5, label, size=2.2, color=color)
        else:
            self.poly([(x + s, y), (x, y), (x, y + s * 0.8)], w="thin", close=True, color=color)
            self.line(x, y, x - 6, y, "dim", color)
            self.text(x - 6.4, y - 0.5, label, size=2.2, anchor="end", color=color)

    def section_mark(self, x1, y1, x2, y2, label):
        """Garis potongan dengan panah arah pandang (ke timur) dan huruf."""
        self.line(x1, y1, x2, y2, "visible", dash="3,1")
        ang = math.atan2(y2 - y1, x2 - x1)
        nx, ny = -math.sin(ang), math.cos(ang)
        for (px, py) in [(x1, y1), (x2, y2)]:
            ox, oy = px - nx * 3.5, py - ny * 3.5  # sisi timur (arah pandang)
            self.line(px, py, ox, oy, "visible")
            self._arrow(ox, oy, math.atan2(oy - py, ox - px), 1.3)
        for (px, py) in [(x1, y1), (x2, y2)]:
            self.axis_bubble(px, py, label, r=2.8)

    def view_dir(self, x, y, label, deg=90, size=2.0):
        """Simbol arah pandang (lingkaran + panah)."""
        r = 3.0
        self.circle(x, y, r, "thin")
        a = math.radians(deg)
        self._arrow(x + math.cos(a) * r * 0.15, y + math.sin(a) * r * 0.15, a, 2.4)
        self.text(x, y + r + 2.2, label, size=size, anchor="middle")

    # ---------------- kop gambar ----------------
    def title_block(self, x0, y0, w=185.0, h=34.0, judul=""):
        x1, y1 = x0 + w, y0 + h
        self.rect(x0, y0, w, h, "frame")
        # baris 1: nama proyek
        self.rect(x0, y0, w, 7.5, "kop")
        self.line(x0, y0 + 7.5, x1, y0 + 7.5, "kop")
        self.text(x0 + 2.5, y0 + 5.3, "PEMBANGUNAN PLTS GROUND MOUNT 2,75 kWp", size=3.4, bold=True)
        # baris 2: lokasi (blank)
        bh = 7.0
        self.line(x0, y0 + 7.5 + bh, x1, y0 + 7.5 + bh, "kop")
        self.text(x0 + 1.5, y0 + 7.5 + 3.0, "LOKASI / PEKERJAAN :", size=2.0)
        self.line(x0 + 26, y0 + 7.5 + 4.6, x1 - 1.5, y0 + 7.5 + 4.6, "dim")
        self.line(x0 + 26, y0 + 7.5 + 1.4, x1 - 1.5, y0 + 7.5 + 1.4, "dim")
        self.text(x0 + 26.5, y0 + 7.5 + 2.5, "( diisi sesuai lokasi proyek )", size=1.6, color="#666666")
        # baris 3: judul gambar
        bh2 = 6.5
        self.line(x0, y0 + 7.5 + bh + bh2, x1, y0 + 7.5 + bh + bh2, "kop")
        self.text(x0 + 1.5, y0 + 7.5 + bh + 4.4, "JUDUL GAMBAR :", size=2.0)
        self.text(x0 + 26.5, y0 + 7.5 + bh + 4.6, judul.upper(), size=2.8, bold=True)
        # baris 4: data grid
        gy = y0 + 7.5 + bh + bh2
        gh = h - (7.5 + bh + bh2)
        for cx in (47, 76, 100, 132, 160):
            self.line(x0 + cx, gy, x0 + cx, y1, "kop")
        self.line(x0, gy + 2.6, x1, gy + 2.6, "kop")
        heads = [("NO. GAMBAR", 1.2), ("SKALA", 48.2), ("SAT.", 77.2),
                 ("TANGGAL", 101.2), ("REVISI", 133.2), ("STATUS", 161.2)]
        for hd, dx in heads:
            self.text(x0 + dx, gy + 1.9, hd, size=1.5)
        vh = gh - 2.6
        self.text(x0 + 1.2, gy + 2.6 + vh * 0.62, self.doc_no, size=4.2, bold=True)
        self.text(x0 + 48.2, gy + 2.6 + vh * 0.62, self.scale_txt, size=3.4, bold=True)
        self.text(x0 + 77.2, gy + 2.6 + vh * 0.62, self.unit_txt, size=3.0, bold=True)
        self.text(x0 + 101.2, gy + 2.6 + vh * 0.62, self.date_txt, size=2.6)
        self.text(x0 + 133.2, gy + 2.6 + vh * 0.62, self.rev, size=3.0, bold=True)
        self.text(x0 + 161.2, gy + 2.6 + vh * 0.62, "KONSTRUKSI", size=2.2)

    def sign_block(self, x0, y0, w=185.0, h=9.0):
        """Blok DIGAMBAR / DIPERIKSA / DISAHKAN di atas kop."""
        self.rect(x0, y0, w, h, "frame")
        cw = w / 3.0
        for i in range(1, 3):
            self.line(x0 + cw * i, y0, x0 + cw * i, y0 + h, "kop")
        labels = ["DIGAMBAR", "DIPERIKSA", "DISAHKAN"]
        for i, lb in enumerate(labels):
            self.text(x0 + cw * i + cw / 2, y0 + 3.2, lb, size=2.0, anchor="middle", bold=True)
            self.line(x0 + cw * i + 3, y0 + 6.8, x0 + cw * (i + 1) - 3, y0 + 6.8, "dim")
            self.text(x0 + cw * i + cw / 2, y0 + 8.4, "NAMA / TGL :", size=1.5, anchor="middle",
                      color="#666666")

    def border(self):
        x0, y0 = self.bl, self.m
        x1, y1 = self.W - self.m, self.H - self.m
        self.rect(x0, y0, x1 - x0, y1 - y0, "frame")
        self.rect(x0 - 4, y0 - 4, 4, y1 - y0, "frame")  # bibir arsip kiri
        return x0, y0, x1, y1

    # ---------------- output ----------------
    def svg(self):
        body = "\n".join(self.el)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.W}mm" '
                f'height="{self.H}mm" viewBox="0 0 {self.W} {self.H}">'
                f'<rect width="{self.W}" height="{self.H}" fill="#ffffff"/>'
                f'{body}</svg>')


def _esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
