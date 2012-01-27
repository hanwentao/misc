#!/usr/bin/env python
# coding: utf-8
# Wentao Han (wentao.han@gmail.com)

import sys
import Image

def get_orientation(path):
    """Returns the orientation of the image file specified by path.

    Return values:
        'landscape' - if width is greater than height,
        'portrait'  - if width is less than height,
        'square'    - if width is equal to height.
    """
    try:
        image = Image.open(path)
    except IOError:
        return 'unknown'
    width, height = image.size
    # XXX: Deal with orientation in EXIF using internal API
    try:
        exif = image._getexif()
        if exif[274] >= 5:
            width, height = height, width
    except (IOError, KeyError):
        pass
    if width > height:
        return 'landscape'
    elif width < height:
        return 'portrait'
    else:
        return 'square'

def main(args):
    image_paths = args[1:]
    if len(image_paths) == 1:
        image_path = image_paths[0]
        orientation = get_orientation(image_path)
        sys.stdout.write('%s\n' % orientation)
    else:
        for image_path in image_paths:
            orientation = get_orientation(image_path)
            sys.stdout.write('%s: %s\n' % (image_path, orientation))

if __name__ == '__main__':
    sys.exit(main(sys.argv))
