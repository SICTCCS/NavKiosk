"""
Generate solid-color desktop tiles from a source image.

Usage:
    python generate_tiles.py --source path/to/image.jpg --cols 8 --rows 5 --tile-size 256

This script will:
 - load the source image
 - divide it into a grid (cols x rows)
 - compute the average color for each cell
 - create a solid-color PNG tile per cell and save on the user's Desktop in a folder named "image_tiles_<timestamp>"
 - optionally output a small contact-sheet preview named preview.png in the same folder

Requirements:
 - Pillow

"""
import os
import sys
from datetime import datetime
from math import ceil
from argparse import ArgumentParser

try:
    from PIL import Image, ImageDraw
except Exception:
    print("Pillow is required. Install with: pip install pillow")
    raise


def average_color(image):
    """Return the average color (R, G, B) of a PIL Image."""
    # Resize to 1x1 to get the average quickly
    small = image.resize((1, 1), resample=Image.BILINEAR)
    return small.getpixel((0, 0))[:3]


def ensure_desktop_folder(folder_name):
    """Return a path to a new folder on the user's Desktop, creating it if necessary."""
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    out_dir = os.path.join(desktop, folder_name)
    os.makedirs(out_dir, exist_ok=True)
    return out_dir


def make_solid_tile(color, size):
    """Create a new PIL Image of given size filled with color."""
    img = Image.new("RGB", size, color)
    return img


def build_preview(tiles, cols, tile_size, padding=2, bg=(30, 30, 30)):
    """Create a contact-sheet preview image from a list of tile images."""
    rows = ceil(len(tiles) / cols)
    w = cols * tile_size + (cols + 1) * padding
    h = rows * tile_size + (rows + 1) * padding
    preview = Image.new("RGB", (w, h), bg)
    x = padding
    y = padding
    for i, t in enumerate(tiles):
        preview.paste(t, (x, y))
        x += tile_size + padding
        if (i + 1) % cols == 0:
            x = padding
            y += tile_size + padding
    return preview


def main():
    p = ArgumentParser(description="Generate solid-color desktop tiles from a source image")
    p.add_argument("--source", required=True, help="Path to the source image")
    p.add_argument("--cols", type=int, default=8, help="Number of columns in grid")
    p.add_argument("--rows", type=int, default=5, help="Number of rows in grid")
    p.add_argument("--tile-size", type=int, default=256, help="Pixel size (square) of each tile to save")
    p.add_argument("--preview-cols", type=int, default=8, help="Columns in the preview contact sheet")
    args = p.parse_args()

    src_path = args.source
    if not os.path.isfile(src_path):
        print(f"Source image not found: {src_path}")
        sys.exit(1)

    try:
        img = Image.open(src_path).convert("RGB")
    except Exception as e:
        print(f"Failed to open image: {e}")
        sys.exit(1)

    cols = max(1, args.cols)
    rows = max(1, args.rows)

    w, h = img.size
    cell_w = w / cols
    cell_h = h / rows

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_name = f"image_tiles_{timestamp}"
    out_dir = ensure_desktop_folder(folder_name)

    tiles = []
    print(f"Source image: {src_path} ({w}x{h}), grid: {cols}x{rows}, output: {out_dir}")

    for r in range(rows):
        for c in range(cols):
            left = int(round(c * cell_w))
            upper = int(round(r * cell_h))
            right = int(round((c + 1) * cell_w))
            lower = int(round((r + 1) * cell_h))
            # Clamp
            right = min(right, w)
            lower = min(lower, h)
            if right <= left or lower <= upper:
                print(f"Skipping empty cell at r={r}, c={c}")
                continue
            cell = img.crop((left, upper, right, lower))
            col = average_color(cell)
            tile = make_solid_tile(col, (args.tile_size, args.tile_size))
            fname = f"tile_r{r}_c{c}.png"
            tile_path = os.path.join(out_dir, fname)
            tile.save(tile_path)
            tiles.append(tile)

    # Build and save preview
    try:
        preview = build_preview(tiles, args.preview_cols, args.tile_size)
        preview_path = os.path.join(out_dir, "preview.png")
        preview.save(preview_path)
        print(f"Saved preview: {preview_path}")
    except Exception as e:
        print(f"Failed to build preview: {e}")

    print("Done.")


if __name__ == '__main__':
    main()
