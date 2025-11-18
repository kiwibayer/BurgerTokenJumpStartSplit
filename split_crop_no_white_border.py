#!/usr/bin/env python3
"""
Split side-by-side theme images into FRONT (left) and BACK (right),
and crop each half to its fixed, white-border-free box.
"""

from PIL import Image
from pathlib import Path
import argparse

FRONT_BOX = (50, 50, 800, 1100)
BACK_BOX  = (25, 50, 775, 1098)

def process_theme(path, out_dir, dry_run=False):
    im = Image.open(path)
    W, H = im.size
    mid = W // 2

    front = im.crop((0, 0, mid, H)).crop(FRONT_BOX)
    back  = im.crop((mid, 0, W, H)).crop(BACK_BOX)

    out_dir.mkdir(parents=True, exist_ok=True)
    stem = path.stem
    if not dry_run:
        front.save(out_dir / f"{stem}_front.png")
        back.save(out_dir / f"{stem}_back.png")
        print(f"[OK] {stem} -> front {front.size}, back {back.size}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="input_dir", required=True, help="Folder with *-theme.png")
    ap.add_argument("--out", dest="output_dir", required=True, help="Output folder")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    in_dir = Path(args.input_dir)
    out_dir = Path(args.output_dir)

    for p in sorted(in_dir.glob("*.png")):
        process_theme(p, out_dir, dry_run=args.dry_run)

if __name__ == "__main__":
    main()
