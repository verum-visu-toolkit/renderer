#!/usr/bin/env python
"""Verum Visu Toolkit: Renderer.

Usage:
  vv-renderer --rnd=<renderpath> -o <destpath>

Options:
  -h --help           Show this screen.
  --version           Show version.
  --rnd=<renderpath>  Path to a JSON file with Director output data
  -o <destpath>       Path to write output mp4 file
"""

from docopt import docopt
import pkg_resources
import json
from renderer import render

# rnd JSON file format:
# {config, data}
#   config: {width: Number, height: Number, num_frames: Number, speed: Number}
#   data: [frame, ...]
#       frame: [command, ...]
#           command: {type: String, args, name?: String} | {"hide": name}
#               args: {param_name: param_val, ...}


def main():
    version = pkg_resources.require('vvrenderer')[0]
    input_args = docopt(__doc__, version=version)

    # test that the dest path is writeable
    with open(input_args['-o'], 'w'):
        pass

    with open(input_args['--rnd']) as rnd_file:
        rnd_file_data = json.load(rnd_file)
        # impl binary format for rnd files later... json.load => fndfile.load

        rnd_file_config = rnd_file_data['config']
        config = {
            'width': int(rnd_file_config['width']),
            'height': int(rnd_file_config['height']),
            'num_frames': int(rnd_file_config['num_frames']),
            'speed': float(rnd_file_config['speed'])
        }
        video = render(command_frames=rnd_file_data['data'], config=config)
        video.write_videofile(input_args['-o'])


if __name__ == '__main__':
    main()
