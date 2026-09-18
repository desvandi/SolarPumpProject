# -*- coding: utf-8 -*-
"""build.py — Rakit 6 lembar gambar -> SVG + PNG + PDF (A3, 1:100)."""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

import design as D
import sheets_plan as SP
import sheets_elev as SE

# Direktori output — portabel. Override dengan env var: PLTS_OUT=/path python3 build.py
# Default: folder "gambar-kerja" satu level di atas folder skrip ini.
OUT = os.environ.get("PLTS_OUT", os.path.join(_HERE, "..", "gambar-kerja"))

FILES = [
    "G-01 TAMPAK ATAS.svg",
    "G-02 TAMPAK DEPAN.svg",
    "G-03 TAMPAK SAMPING (POTONGAN A-A).svg",
    "G-04 TAMPAK ATAS - PANEL SURYA DISAMARKAN (RANGKA).svg",
    "G-05 TAMPAK ATAS - PANEL DIHILANGKAN (RANGKA & BETON).svg",
    "G-06 TAMPAK ATAS - PANEL & RANGKA DISAMARKAN (BETON).svg",
]


def main():
    os.makedirs(OUT, exist_ok=True)
    sheets = [SP.g01(), SE.g02(), SE.g03(), SP.g04(), SP.g05(), SP.g06()]
    svgs = []
    for sh, nm in zip(sheets, FILES):
        svg = sh.svg()
        path = os.path.join(OUT, nm)
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg)
        svgs.append(path)
        print("SVG OK:", nm)

    # --- PNG (220 dpi) ---
    import cairosvg
    pngs = []
    for p in svgs:
        q = p[:-4] + ".png"
        cairosvg.svg2png(url=p, write_to=q, dpi=220, background_color="white")
        pngs.append(q)
        print("PNG OK:", os.path.basename(q))

    # --- PDF per lembar lalu gabung ---
    import cairosvg as cs
    import io
    from pypdf import PdfWriter, PdfReader
    writer = PdfWriter()
    for p in svgs:
        pdf_bytes = cs.svg2pdf(url=p)
        reader = PdfReader(io.BytesIO(pdf_bytes))
        for pg in reader.pages:
            writer.add_page(pg)
    writer.add_metadata({
        "/Title": "Gambar Kerja PLTS Ground Mount 2,75 kWp (5 x 550 Wp)",
        "/Author": "Z.ai",
        "/Creator": "Z.ai — penyempurnaan draft SVG pengguna",
        "/Subject": "Tampak atas, depan, samping, rangka & struktur beton — skala 1:100 (A3)",
    })
    pdf_path = os.path.join(OUT, "Gambar Kerja PLTS Ground Mount 2,75 kWp.pdf")
    with open(pdf_path, "wb") as f:
        writer.write(f)
    print("PDF OK:", pdf_path)
    print("\nSelesai. Output:", OUT)


if __name__ == "__main__":
    main()
