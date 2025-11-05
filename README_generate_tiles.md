Generate solid-color tiles from a source image

Usage example (powershell):

    python .\generate_tiles.py --source C:\path\to\image.jpg --cols 8 --rows 5 --tile-size 256

The script will create a folder on your Desktop named `image_tiles_<timestamp>` and save PNG tiles and a `preview.png` contact sheet there.

Dependencies:
 - Pillow (install with `pip install pillow`)

Notes:
 - Columns and rows control how the source image is divided.
 - Tile size controls the pixel size of each produced PNG (square).
