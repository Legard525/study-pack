#!/usr/bin/env python3
"""Render a PDF's pages and tile them four per image for a fast visual check.

Usage: contact_sheet.py <file.pdf> <out_dir> [--dpi 70] [--per 4]
Prints the paths of the tiled sheets. Uses pdftoppm (poppler) if present, else PyMuPDF.
"""
import argparse, glob, os, shutil, subprocess, sys

from PIL import Image


def render(pdf, out_dir, dpi):
    prefix = os.path.join(out_dir, "page")
    if shutil.which("pdftoppm"):
        subprocess.run(["pdftoppm", "-r", str(dpi), "-png", pdf, prefix], check=True)
        return sorted(glob.glob(prefix + "-*.png"))
    try:
        import fitz  # PyMuPDF
    except ImportError:
        sys.exit("Need poppler (pdftoppm) or PyMuPDF (pip install pymupdf).")
    paths = []
    for i, page in enumerate(fitz.open(pdf), 1):
        p = f"{prefix}-{i:03d}.png"
        page.get_pixmap(dpi=dpi).save(p)
        paths.append(p)
    return paths


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("out_dir")
    ap.add_argument("--dpi", type=int, default=70)
    ap.add_argument("--per", type=int, default=4)
    a = ap.parse_args()
    os.makedirs(a.out_dir, exist_ok=True)
    for old in glob.glob(os.path.join(a.out_dir, "page-*.png")) + glob.glob(os.path.join(a.out_dir, "sheet-*.png")):
        os.remove(old)
    pages = render(a.pdf, a.out_dir, a.dpi)
    print(f"{len(pages)} pages")
    for k in range(0, len(pages), a.per):
        ims = [Image.open(p) for p in pages[k:k + a.per]]
        w = max(im.width for im in ims); h = max(im.height for im in ims)
        sheet = Image.new("RGB", (w * len(ims), h), "white")
        for i, im in enumerate(ims):
            sheet.paste(im, (i * w, 0))
        out = os.path.join(a.out_dir, f"sheet-{k // a.per + 1}.png")
        sheet.save(out)
        print(out, f"(pages {k + 1}-{k + len(ims)})")


if __name__ == "__main__":
    main()
