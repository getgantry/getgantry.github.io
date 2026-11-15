#!/usr/bin/env python3
"""Fail when the site fonts miss a letter, mark or digit of a site language.

Needs fontTools with brotli. Symbols only get a note: they fall back to the system font.
"""
import json
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

try:
    from fontTools.ttLib import TTFont
except ImportError:
    sys.exit("check_fonts: install fontTools and brotli first (pip install fonttools brotli)")

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "assets" / "fonts"
TAG = re.compile(r"<[^>]+>")
CODE = re.compile(r"<code>(.*?)</code>", re.S)


def cmap_of(prefix):
    chars = set()
    for f in sorted(FONTS.glob(prefix + "-*.woff2")):
        chars |= set(TTFont(f).getBestCmap())
    return chars


def strings(node):
    if isinstance(node, str):
        yield node
    elif isinstance(node, dict):
        for v in node.values():
            yield from strings(v)
    elif isinstance(node, list):
        for v in node:
            yield from strings(v)


def missing(chars, cmap):
    return sorted(c for c in chars if not c.isspace() and ord(c) not in cmap)


def main():
    sans, mono = cmap_of("ibm-plex-sans"), cmap_of("jetbrains-mono")
    if not sans or not mono:
        sys.exit("check_fonts: no font files in assets/fonts")
    langs = sorted((ROOT / "i18n").glob("*.json"))
    errors, symbols = 0, defaultdict(int)
    for path in langs:
        all_strings = list(strings(json.loads(path.read_text(encoding="utf-8"))))
        text = set("".join(TAG.sub(" ", s) for s in all_strings))
        code = set("".join(c for s in all_strings for c in CODE.findall(s)))
        for font, chars, cmap in (("text", text, sans), ("mono", code, mono)):
            gaps = missing(chars, cmap)
            hard = [c for c in gaps if unicodedata.category(c)[0] in "LMN"]
            if hard:
                errors += 1
                print(f"{path.stem}: {font} font misses {''.join(hard)!r}")
            if font == "text":
                for c in gaps:
                    if c not in hard:
                        symbols[c] += 1
    for c, n in sorted(symbols.items()):
        print(f"note: {c!r} U+{ord(c):04X} uses the system font ({n} languages)")
    if errors:
        sys.exit(f"check_fonts: {errors} problem(s)")
    print(f"check_fonts: ok, {len(langs)} languages")


if __name__ == "__main__":
    main()
