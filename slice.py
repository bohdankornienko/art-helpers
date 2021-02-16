import os
import argparse

from PIL import Image

import numpy as np

def main(args):
    step = int(args.step)
    img = np.array(Image.open(args.file))
    print(img.shape)
    # h, w, c
    parts = img.shape[1] / step

    base_name, ext = os.path.splitext(args.file)

    results = list()
    prev_step = 0
    for s in range(1, int(parts)+1):
        lhs = prev_step
        rhs = s

        print(lhs * step, rhs * step)
        print(lhs, rhs)
        prev_step = s

        file_name = '{}-{:0>2}{}'.format(base_name, rhs, ext)
        print(file_name)
        roi = img[:, lhs*step:rhs*step, :]
        print('shape:', roi.shape)
        Image.fromarray(roi).save(file_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Slices image into pieces every --step piexel")
    parser.add_argument('--file', help='Path to file')
    parser.add_argument('--step', help='Step')

    args = parser.parse_args()

    main(args)
