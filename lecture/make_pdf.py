# -*- coding: utf-8 -*-
"""Render the complete slide deck to PDF and PNG previews."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "render"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import content_a, content_b, content_c, content_d
from deck import render
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
S = content_a.S + content_b.S + content_c.S + content_d.S
OUT = os.path.join(ROOT, "media", "IF701_Fire_Dynamics_Slides.pdf")


def main():
    pages = []
    for i, seg in enumerate(S):
        im = render(seg, i + 1, len(S), scale=1.25)
        im = im.convert("RGB")
        pages.append(im)
        print(f"  {i+1:02d}/{len(S)} {seg['id']}")
    pages[0].save(OUT, save_all=True, append_images=pages[1:], resolution=150.0,
                  quality=82, optimize=True)
    print("PDF:", OUT, os.path.getsize(OUT) / 1e6, "MB", len(pages), "pages")


if __name__ == "__main__":
    main()
