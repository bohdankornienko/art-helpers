import os
import argparse

from PIL import Image
from math import ceil

import numpy as np


def apply_watermark(input_image, watermark):
    y_ratio = ceil(input_image.shape[0]/watermark.shape[0])
    x_ratio = ceil(input_image.shape[1]/watermark.shape[1])

    tiled_watermark = np.zeros((watermark.shape[0] * y_ratio, watermark.shape[1] * x_ratio, watermark.shape[2]), dtype=watermark.dtype)

    for y in range(y_ratio):
        for x in range(x_ratio):
            ylhs, yrhs = y*watermark.shape[0], y*watermark.shape[0]+watermark.shape[0]
            xlhs, xrhs = x*watermark.shape[1], x*watermark.shape[1]+watermark.shape[1]
            tiled_watermark[ylhs:yrhs, xlhs:xrhs, :] = watermark

    tiled_watermark = tiled_watermark[:input_image.shape[0], :input_image.shape[1], :]

    locations = np.stack([tiled_watermark[:, :, 3] > 0] * 4)
    locations = np.moveaxis(locations, [0, 1, 2], [2, 0, 1])

    alpha = tiled_watermark[:, :, 3] / 255
    alphas = np.stack([alpha] * 4)
    alphas = np.moveaxis(alphas, [0, 1, 2], [2, 0, 1])

    watermarked_image = input_image * (1 - alphas) + tiled_watermark * alphas
    watermarked_image = watermarked_image.astype(np.uint8)

    return watermarked_image

def main(args):
    input_path = os.path.abspath(args.input)
    file_dir = os.path.split(input_path)[0]
    base_name, ext = os.path.splitext(args.input)

    print('Applying watermark to: {}'.format(input_path))

    suffix = args.suffix
    output_file_name = os.path.join(file_dir, f'{base_name}-{suffix}.png')
    print(f'Result is written to: {output_file_name}')

    input_image = np.array(Image.open(input_path).convert('RGBA'))
    watermark = np.array(Image.open(args.watermark).convert('RGBA'))

    watermarked_image = apply_watermark(input_image, watermark)

    dst = Image.fromarray(watermarked_image)
    dst.save(output_file_name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--input", help="Input image path")
    parser.add_argument("--watermark", help="Input watermark image path")
    parser.add_argument("--suffix", default='watermark')

    args = parser.parse_args()

    main(args)
