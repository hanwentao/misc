#!/usr/bin/env python
# coding: utf-8
# Wentao Han (wentao.han@gmail.com)

import argparse
import os
import os.path
import re
import sys
import Image

def adapt(source_path, target_path, target_size, args=None):
    """Adapts the source image to the target size."""

    source_image = Image.open(source_path)

    # Rotate the image
    # XXX: Deal with EXIF rotation tag
    try:
        exif = source_image._getexif()
        if exif[274] == 6:
            source_image = source_image.rotate(-90)
        elif exif[274] == 8:
            source_image = source_image.rotate(90)
    except (AttributeError, IOError, KeyError):
        pass
    source_width, source_height = source_image.size
    target_width, target_height = target_size

    # Resize the image
    #  resize_width      source_width
    # --------------- = ---------------
    #  resize_height     source_height
    resize_width = int(float(target_height) * source_width / source_height)
    if resize_width >= target_width:
        resize_height = target_height
    else:
        resize_height = int(float(target_width) * source_height / source_width)
        resize_width = target_width
    resized_image = source_image.resize((resize_width, resize_height), Image.ANTIALIAS)

    # Crop the image
    if resize_width > target_width:
        crop_x0 = (resize_width - target_width) / 2
        crop_y0 = 0
    else:
        crop_x0 = 0
        crop_y0 = (resize_height - target_height) / 2
    crop_box = (crop_x0, crop_y0, crop_x0 + target_width, crop_y0 + target_height)
    cropped_image = resized_image.crop(crop_box)

    # Convert to grayscale if specified
    if args and args.grayscale:
        cropped_image = cropped_image.convert("L")

    # Save the image
    cropped_image.save(target_path)

def main(argv=None):
    parser = argparse.ArgumentParser(description='Adapt pictures to target size.')
    parser.add_argument('image_paths',
                        nargs='+',
                        metavar='IMAGE',
                        help='images to adapt')
    parser.add_argument('-O', '--output',
                        dest='output_dir',
                        metavar='DIRECTORY',
                        default='output/',
                        help='specify the output directory')
    parser.add_argument('-s', '--size',
                        dest='target_size',
                        metavar='SIZE',
                        default='800x600',
                        help='specify the target size')
    parser.add_argument('-g', '--grayscale',
                        dest='grayscale',
                        action='store_true',
                        help='convert to grayscale')
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='verbose output')
    args = parser.parse_args(argv)

    # Parse target size
    match = re.match(r'(\d+)[Xx](\d+)', args.target_size)
    if match is None or match.group(0) != args.target_size:
        parser.error('invalid target size')
    args.target_size = (int(match.group(1)), int(match.group(2)))

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    for image_path in args.image_paths:
        output_path = os.path.join(args.output_dir, os.path.basename(image_path))
        if args.verbose:
            sys.stdout.write('%s => %s\n' % (image_path, output_path))
        adapt(image_path, output_path, args.target_size, args)

if __name__ == '__main__':
    sys.exit(main())
