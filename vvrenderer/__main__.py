#!/usr/bin/env python
"""Verum Visu Toolkit: Renderer.

Usage:
  vv-renderer --rnd=<renderpath> -o <destpath>
              [--audio=<audiosrcpath>]
              [--duration=<seconds>]


Options:
  -h --help               Show this screen.
  --version               Show version.
  --rnd=<renderpath>      Path to a file with Director output data
  --audio=<audiosrcpath>  Path to an audio file to composite to the output
  --duration=<seconds>    Optional, specify duration of video
  -o <destpath>           Path to write output mp4 file (should end in .mp4)
"""

from docopt import docopt
import pkg_resources
from vvbasicfile import RndFormatReader, load_basicfile_field
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

    rndpath = input_args['--rnd']
    audiopath = input_args['--audio']
    duration = input_args['--duration']
    outputpath = input_args['-o']

    # test that the dest path is writeable
    with open(outputpath, 'w'):
        pass

    rnd_file_config = load_basicfile_field(rndpath, 'config')
    render_config = {
        'width': int(rnd_file_config['width']),
        'height': int(rnd_file_config['height']),
        'num_frames': int(rnd_file_config['num_frames']),
        'speed': float(rnd_file_config['speed'])
    }

    with RndFormatReader(rndpath) as rnd_frames:
        video = render(command_frames=rnd_frames, config=render_config, audio_srcpath=audiopath,
                       duration=duration)
        video.write_videofile(outputpath)


if __name__ == '__main__':
    main()
