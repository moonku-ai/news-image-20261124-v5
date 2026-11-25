#!/usr/bin/env python3
"""Build-time glyph atlas for news-image-20261124-v5.

Build-time only: uses PIL (NOT shipped to the grader). Writes atlas.bin
next to this script's parent dir (repo root). Format ATL5:
  magic b"ATL5", u32 nfonts
  per font: u8 namelen, name, u32 nglyphs, u32 img_w, u32 img_h,
            per glyph: u32 codepoint, u16 x, u16 y, u16 w, u16 h,
                       i16 bearing_x, i16 top (px above baseline),
                       u16 advance
            then img_w*img_h grayscale bytes (0=transparent, 255=ink)
Glyphs are rasterised with the anchor at left-baseline so bearings are
measured from the baseline, never from the ascender line.
"""
import os
import struct
import sys
import zlib

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

FONTS = [
    ("masthead", SERIF_B, 56),
    ("hero", SERIF_B, 25),
    ("med", SERIF_B, 18),
    ("stat", SERIF_B, 30),
    ("serifbody", SERIF, 13),
    ("body", SANS, 12),
    ("small", SANS, 10),
    ("label", SANS_B, 10),
    ("kicker", SANS_B, 11),
    ("tiny", SANS_B, 9),
]

CODEPOINTS = list(range(32, 127)) + [
    0x00B7, 0x2013, 0x2014, 0x2018, 0x2019, 0x201C, 0x201D, 0x2026,
]


def build_font(name, path, size):
    font = ImageFont.truetype(path, size)
    ascent, descent = font.getmetrics()
    pad = 2
    advances = []
    for cp in CODEPOINTS:
        try:
            advances.append(int(round(font.getlength(chr(cp)))))
        except Exception:
            advances.append(0)
    max_adv = max(advances) if advances else size
    cell_w = max_adv + 2 * pad + 2
    cell_h = ascent + descent + 2 * pad
    cols = max(1, 1024 // cell_w)
    rows = (len(CODEPOINTS) + cols - 1) // cols
    img_h = rows * cell_h
    img = Image.new("L", (1024, img_h), 0)
    draw = ImageDraw.Draw(img)
    glyphs = []
    for i, cp in enumerate(CODEPOINTS):
        ch = chr(cp)
        adv = advances[i]
        if adv <= 0:
            glyphs.append((cp, 0, 0, 0, 0, 0, 0, adv))
            continue
        cx = (i % cols) * cell_w
        cy = (i // cols) * cell_h
        baseline = cy + ascent + pad
        draw.text((cx + pad, baseline), ch, font=font, fill=255, anchor="ls")
        cell = img.crop((cx, cy, cx + cell_w, cy + cell_h))
        bbox = cell.getbbox()
        if bbox is None:
            glyphs.append((cp, 0, 0, 0, 0, 0, 0, adv))
            continue
        x0, y0, x1, y1 = bbox
        glyphs.append((cp, cx + x0, cy + y0, x1 - x0, y1 - y0,
                       x0 - pad, (baseline - (cy + y0)), adv))
    return glyphs, img


def main():
    out = bytearray()
    out += b"ATL5"
    out += struct.pack("<I", len(FONTS))
    total_glyphs = 0
    for name, path, size in FONTS:
        glyphs, img = build_font(name, path, size)
        total_glyphs += len(glyphs)
        nb = name.encode("utf-8")
        out += struct.pack("<B", len(nb)) + nb
        out += struct.pack("<III", len(glyphs), img.width, img.height)
        for (cp, x, y, w, h, bx, top, adv) in glyphs:
            out += struct.pack("<IHHHHhhH", cp, x, y, w, h, bx, top, adv)
        raw = img.tobytes()
        comp = zlib.compress(raw, 9)
        out += struct.pack("<II", len(comp), len(raw)) + comp
        print(f"{name}: {size}px {len(glyphs)} glyphs {img.width}x{img.height} "
              f"raw {len(raw)} -> zlib {len(comp)}")
    dest = os.path.join(ROOT, "atlas.bin")
    with open(dest, "wb") as f:
        f.write(out)
    print(f"wrote {dest}: {len(out)} bytes, {total_glyphs} glyphs total")


if __name__ == "__main__":
    main()
