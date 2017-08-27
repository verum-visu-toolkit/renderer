#!/usr/bin/env python
"""Verum Visu Toolkit: Renderer.

Usage:
  vv-renderer --fms=<framespath> --rnd=<renderpath> -o <destpath>

Options:
  -h --help           Show this screen.
  --version           Show version.
  --fms=<framespath>  Path to a JSON file with Interpreter output data
  --rnd=<renderpath>  Path to a JSON file with Director output data
  -o <destpath>       Path to write output mp4 file
"""

from docopt import docopt
import pkg_resources
import json
from renderer import render


def main():
    version = pkg_resources.require('vvrenderer')[0]
    input_args = docopt(__doc__, version=version)

    # test that the dest path is writeable
    with open(input_args['-o'], 'w'):
        pass

    with open(input_args['--fms']) as fms_file:
        fms_file_data = json.load(fms_file)  # (8.27.17) let's use json formats
        #  for now and implement binary formats later
        with open(input_args['--rnd']) as rnd_file:
            rnd_file_data = json.load(rnd_file)

            config = {
                'width': rnd_file_data['config']['width'],
                'height': rnd_file_data['config']['height'],
                'num_frames': fms_file_data['num_frames'],
                'speed': fms_file_data['speed']
            }
            video = render(shapes=rnd_file['shapes'], frames=fms_file,
                           config=config)
            video.write_videofile(input_args['-o'])


if __name__ == '__main__':
    main()
