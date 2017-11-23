#!/usr/bin/env python
"""Verum Visu Toolkit: Renderer.

Usage:
  vv-renderer --rnd=<renderpath> [--json] -o <destpath>
              [--audio=<audiosrcpath>]
              [--duration=<seconds>]


Options:
  -h --help               Show this screen.
  --version               Show version.
  --rnd=<renderpath>      Path to a file with Director output data
  --json                  Specifies that the file contains uncompressed JSON
  --audio=<audiosrcpath>  Path to an audio file to composite to the output
  --duration=<seconds>    Optional, specify duration of video
  -o <destpath>           Path to write output mp4 file (should end in .mp4)
"""

from docopt import docopt
import pkg_resources
from vvbasicfile import RndFormat
from __init__ import render

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

    output_path = input_args['-o']

    # test that the dest path is writeable
    with open(output_path, 'w'):
        pass

    rnd_filename = input_args['--rnd']
    rndfile = RndFormat.load_from_json_file(rnd_filename) \
        if input_args['--json'] else RndFormat.load_from_file(rnd_filename)

    rnd_file_config = rndfile.get_config()

    render_config = {
        'width': int(rnd_file_config['width']),
        'height': int(rnd_file_config['height']),
        'num_frames': int(rnd_file_config['num_frames']),
        'speed': float(rnd_file_config['speed'])
    }
    duration = input_args['--duration']

    video = render(command_frames=rndfile.data(), config=render_config,
                   audio_srcpath=input_args['--audio'], duration=duration)
    video.write_videofile(output_path)


if __name__ == '__main__':
    main()
