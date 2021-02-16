import os
import argparse

def main(args):
    print(args)

    input_path = os.path.abspath(args.input)
    print(input_path)
    prefix = os.path.split(input_path)[0]
    base_name, ext = os.path.splitext(args.input)

    template = 'gif-temporary-'

    cmd1 = 'convert {} {}/{}%05d.png'.format(input_path, prefix, template)
    print(cmd1)
    code = os.system(cmd1)
    cmd2 = 'ffmpeg -framerate 10 -i {}/{}%05d.png -r 25 -pix_fmt yuv420p {}.mp4'.format(prefix, template, base_name)
    print(cmd2)
    code = os.system(cmd2)
    cmd3 = 'rm {}/{}*.png'.format(prefix, template)
    print(cmd3)
    code = os.system(cmd3)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--input")

    args = parser.parse_args()

    main(args)
