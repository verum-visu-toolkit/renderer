from __future__ import print_function

import utils
import gizeh
from moviepy.editor import VideoClip, AudioFileClip

# TODO: figure out why make_frame is taking so long...
# (it's doing about ~3 frames/second rendering the 100 bars, 30fps multi spectra video!)


def render(command_frames, config=None, audio_srcpath=None, duration=None):
    # command_frames: [[{'type':'circle', 'args': { radius: '5', xy: ['32',
    # '33'], fill: [1,0,0] } }, ...commands], ...frames]

    if (hasattr(command_frames, 'next')
            and callable(getattr(command_frames, 'next', None))) or\
        (hasattr(command_frames, '__next__')
            and callable(getattr(command_frames, '__next__', None))):
        frame_is_gen = True
    elif type(command_frames) is list:
        frame_is_gen = False
    else:
        raise TypeError('command_frames must be a list or have __next__ function')

    video_w, video_h = config['width'], config['height']
    video_fps = config['speed']

    named_shapes = dict()

    def make_frame(t):
        surface = gizeh.Surface(video_w, video_h, bg_color=(1, 1, 1))

        # draw all shapes in named_shapes (they are removed when hidden via
        # hide command)
        for _, shape in named_shapes.items():
            shape.draw(surface)

        commands = []
        try:
            if frame_is_gen:
                commands = next(command_frames)  # each video frame is 1-to-1 with a rnd frame
            else:
                num_frame = int(video_fps * t)
                commands = command_frames[num_frame]
        except (StopIteration, IndexError):
            pass

        for command in commands:
            # if there is a hide key, this command is a hide command
            if 'hide' in command:
                del named_shapes[command['hide']]

            # if there is not a hide key, this command is a draw command
            # (and a register command if it provides a name)
            else:
                # make args keys non-unicode-flagged strings for easy access
                shape_args = {
                    str(key): utils.simplify_type_for_gizeh(val)
                    for key, val in command['args'].items()
                }
                shape_method = command['type']

                gizeh_fn = getattr(gizeh, shape_method)
                shape = gizeh_fn(**shape_args)

                if 'name' in command:
                    named_shapes[command['name']] = shape

                shape.draw(surface)

        return surface.get_npimage()

    if duration is None:
        duration = int(config['num_frames']) / float(config['speed'])
    else:
        duration = int(duration)

    video = VideoClip(make_frame=make_frame, duration=duration)
    video.fps = video_fps

    if audio_srcpath is not None:
        video.audio = AudioFileClip(audio_srcpath)

    return video
