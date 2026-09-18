# -*- coding: utf-8 -*-
"""validate_bounds.py — Cek teks SVG yang keluar dari border lembar A3.
Border: x 20..412 (kiri termasuk bibir arsip), y 8..289. Estimasi lebar teks Liberation Sans."""
import re
import sys
import os

BORDER = (20.5, 8.5, 411.5, 288.5)  # x0, y0, x1, y1
W_FACTOR = {False: 0.52, True: 0.56}  # reguler / bold, rata-rata per karakter

PAT = re.compile(
    r'<text x="([\d.-]+)" y="([\d.-]+)" font-family="[^"]+" font-size="([\d.]+)"[^>]*?'
    r'(font-weight="bold")?[^>]*?text-anchor="(\w+)"[^>]*?(transform="rotate\(([-\d.]+))?[^>]*>(.*?)</text>')


def check(path):
    with open(path, encoding='utf-8') as f:
        c = f.read()
    problems = []
    for m in re.finditer(r'<text ([^>]+)>(.*?)</text>', c):
        attrs, inner = m.group(1), m.group(2)
        xm = re.search(r'x="([\d.-]+)"', attrs)
        ym = re.search(r'y="([\d.-]+)"', attrs)
        sm = re.search(r'font-size="([\d.]+)"', attrs)
        am = re.search(r'text-anchor="(\w+)"', attrs)
        bm = 'font-weight="bold"' in attrs
        rm = re.search(r'transform="rotate\(([-\d.]+)', attrs)
        if not (xm and ym and sm):
            continue
        x, y, size = float(xm.group(1)), float(ym.group(1)), float(sm.group(1))
        anchor = am.group(1) if am else "start"
        txt = re.sub(r'<[^>]+>', '', inner)
        txt = txt.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
        if not txt.strip():
            continue
        w = len(txt) * W_FACTOR[bm] * size
        rot = float(rm.group(1)) if rm else None
        if rot is None:
            if anchor == "start":
                x0e, x1e = x, x + w
            elif anchor == "end":
                x0e, x1e = x - w, x
            else:
                x0e, x1e = x - w / 2, x + w / 2
            y0e, y1e = y - size * 0.78, y + size * 0.24
        else:
            # teks rotasi -90 (vertikal, ke atas): eksten sepanjang y
            if abs(abs(rot) - 90) < 1:
                if anchor == "start":
                    y0e, y1e = y - w, y
                elif anchor == "end":
                    y0e, y1e = y, y + w
                else:
                    y0e, y1e = y - w / 2, y + w / 2
                x0e, x1e = x - size * 0.24, x + size * 0.78
            else:
                x0e, x1e = x - w / 2, x + w / 2
                y0e, y1e = y - w / 2, y + w / 2
        if x0e < BORDER[0] - 0.3 or x1e > BORDER[2] + 0.3 or y0e < BORDER[1] - 0.3 or y1e > BORDER[3] + 0.3:
            problems.append((txt[:44], round(x0e, 1), round(x1e, 1), round(y0e, 1), round(y1e, 1)))
    return problems


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else "/home/z/my-project/download/GAMBAR PLTS GROUND MOUNT 2,75 kWp"
    total = 0
    for f in sorted(os.listdir(d)):
        if f.endswith(".svg"):
            p = os.path.join(d, f)
            pr = check(p)
            if pr:
                total += len(pr)
                print(f"== {f}: {len(pr)} teks keluar border")
                for t in pr:
                    print("   ", t)
            else:
                print(f"== {f}: OK")
    print("TOTAL MASALAH:", total)
