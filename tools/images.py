#!/usr/bin/env python3
"""Regenerates assets/img/ from source-images/.

Drop high-resolution originals into source-images/ using these exact filenames:

  guardian-gallery.jpg   Guardian shown in a gallery (landscape)
  bison.jpg              Bison
  ride.jpg               Ride
  madonna.jpg            Madonna
  bear-gallery.jpg       The Bear shown in a gallery (landscape)
  horses-gallery.jpg     The Horses shown in a gallery (landscape)

then run:  pip install pillow && python3 tools/images.py

Each source becomes <name>.webp/.jpg plus -960 and -640 variants when the
source is wider than those sizes. Images are never upscaled. Update the
`w`/`h`/`sizes` values in tools/build.py to match the printed dimensions,
then run python3 tools/build.py.
"""
import os, sys
from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "source-images")
OUT = os.path.join(ROOT, "assets", "img")
VARIANTS = [1600, 960, 640]

def save(im, name):
    im.save(os.path.join(OUT, name + ".webp"), quality=82, method=6)
    im.save(os.path.join(OUT, name + ".jpg"), quality=84, optimize=True, progressive=True)

def main():
    if not os.path.isdir(SRC):
        sys.exit("Create source-images/ and add files first (see docstring).")
    for fn in sorted(os.listdir(SRC)):
        base, ext = os.path.splitext(fn)
        if ext.lower() not in (".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp"):
            continue
        im = ImageOps.exif_transpose(Image.open(os.path.join(SRC, fn))).convert("RGB")
        w, h = im.size
        # full size, capped at 1600 wide
        full = im if w <= VARIANTS[0] else im.resize((VARIANTS[0], round(h * VARIANTS[0] / w)), Image.LANCZOS)
        save(full, base)
        sizes = [full.width]
        for tw in VARIANTS[1:]:
            if full.width > tw:
                r = im.resize((tw, round(h * tw / w)), Image.LANCZOS)
                save(r, f"{base}-{tw}")
                sizes.append(tw)
        print(f"{base}: w={full.width}, h={full.height}, sizes={sizes}")
    # Open Graph image from the guardian gallery shot if present
    g = os.path.join(OUT, "guardian-gallery.jpg")
    if os.path.exists(g):
        og = ImageOps.fit(Image.open(g).convert("RGB"), (1200, 630), Image.LANCZOS, centering=(0.5, 0.45))
        og.save(os.path.join(OUT, "og-image.jpg"), quality=85, optimize=True, progressive=True)
        print("og-image.jpg: 1200x630")

if __name__ == "__main__":
    main()
