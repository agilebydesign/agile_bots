#!/usr/bin/env python3
"""
Add black background to PNG images. Replaces transparent areas and white/near-white
background pixels with black. Saves in place.
"""
from pathlib import Path
from PIL import Image

IMG_DIR = Path(__file__).resolve().parent.parent / "src" / "panel" / "img"

# Pixels with R,G,B all >= this are treated as background and replaced with black
WHITE_THRESHOLD = 240


def process_image(path: Path) -> bool:
    """Replace transparent and white/near-white pixels with black. Returns True if modified."""
    try:
        img = Image.open(path).convert("RGBA")
    except Exception as e:
        print(f"  Skip {path.name}: {e}")
        return False

    w, h = img.size
    pixels = img.load()
    black = (0, 0, 0, 255)

    for y in range(h):
        for x in range(w):
            r, g, b, a = pixels[x, y]
            # Transparent: replace with black
            if a < 10:
                pixels[x, y] = black
            # Opaque white/near-white background: replace with black
            elif r >= WHITE_THRESHOLD and g >= WHITE_THRESHOLD and b >= WHITE_THRESHOLD:
                pixels[x, y] = black

    # Flatten onto black (handles any remaining semi-transparent pixels)
    bg = Image.new("RGB", (w, h), (0, 0, 0))
    bg.paste(img, (0, 0), img)
    bg.save(path, "PNG")
    return True


def main():
    if not IMG_DIR.exists():
        print(f"Directory not found: {IMG_DIR}")
        return 1

    # Only process files directly in img/ (default ABD brand), not subdirs
    count = 0
    for path in sorted(IMG_DIR.iterdir()):
        if path.is_file() and path.suffix.lower() == ".png":
            if process_image(path):
                count += 1
                print(f"  Processed: {path.name}")

    print(f"Done. Processed {count} images.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
