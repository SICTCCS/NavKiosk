import random
import argparse
from PIL import Image


def random_color():
    return tuple(random.randint(0, 255) for _ in range(3))


def generate_random_image(width, height, filename, block_size=10):
    """Generate an image where each logical pixel is drawn as a block_size x block_size square.

    Args:
        width (int): number of logical pixels horizontally (each becomes block_size pixels).
        height (int): number of logical pixels vertically (each becomes block_size pixels).
        filename (str): output filename (PNG).
        block_size (int): size of each "big pixel" in actual image pixels. Default 10.
    """
    img_w, img_h = width * block_size, height * block_size
    img = Image.new('RGB', (img_w, img_h))
    pixels = img.load()

    for bx in range(width):
        for by in range(height):
            color = random_color()
            x0, x1 = bx * block_size, (bx + 1) * block_size
            y0, y1 = by * block_size, (by + 1) * block_size
            for x in range(x0, x1):
                for y in range(y0, y1):
                    pixels[x, y] = color

    img.save(filename, 'PNG')


def _parse_args():
    p = argparse.ArgumentParser(description='Generate random image made of big pixel blocks')
    p.add_argument('--width', '-W', type=int, default=128,
                   help='number of logical pixels horizontally (default: 128)')
    p.add_argument('--height', '-H', type=int, default=128,
                   help='number of logical pixels vertically (default: 128)')
    p.add_argument('--block-size', '-b', type=int, default=10,
                   help='size of each block in actual pixels (default: 10)')
    p.add_argument('--count', '-c', type=int, default=10,
                   help='how many images to generate (default: 10)')
    p.add_argument('--out-prefix', '-o', type=str, default='random_image_',
                   help='output filename prefix (default: random_image_)')
    return p.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    for i in range(args.count):
        filename = f"{args.out_prefix}{i+1}.png"
        generate_random_image(args.width, args.height, filename, block_size=args.block_size)