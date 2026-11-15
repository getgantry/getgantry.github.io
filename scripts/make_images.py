#!/usr/bin/env python3
"""Write 800 px and 1600 px WebP copies next to each screenshot that the pages show. Needs cwebp."""
import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from build_pages import SHOTS, png_size  # noqa: E402

WIDTHS = (800, 1600)


def main():
    if not shutil.which("cwebp"):
        sys.exit("make_images: install cwebp first (brew install webp)")
    made = 0
    for _, rel_path in SHOTS.values():
        src = os.path.join(ROOT, rel_path)
        if not os.path.exists(src):
            continue
        width, _ = png_size(src)
        for w in WIDTHS:
            out = src[:-4] + f"-{w}.webp"
            if os.path.exists(out) and os.path.getmtime(out) >= os.path.getmtime(src):
                continue
            resize = ["-resize", str(w), "0"] if width > w else []
            subprocess.run(["cwebp", "-quiet", "-q", "82", "-m", "6", *resize, src, "-o", out], check=True)
            made += 1
    print(f"make_images: {made} file(s) written")


if __name__ == "__main__":
    main()
