from __future__ import print_function

import gizeh
from moviepy.editor import VideoClip

# W,H = 128,128  # width, height, in pixels
# duration = 2  # duration of the clip, in seconds

# def make_frame(t):
#     surface = gizeh.Surface(W,H)
#     radius = W * (1 + (t*(duration-t))**2) / 6
#     circle = gizeh.circle(radius, xy=(W/2, H/2), fill=(1, 0, 0))
#     circle.draw(surface)
#     return surface.get_npimage()
#
# clip = mpy.VideoClip(make_frame, duration=duration)
# clip.write_gif('circle.gif', fps=15, opt='OptimizePlus', fuzz=10)


def render(command_frames=None, config=None):
    # command_frames: [[{'type':'circle', 'args': { radius: '5', xy: ['32',
    # '33'], fill: [1,0,0] } }, ...commands], ...frames]

    video_w, video_h = config['width'], config['height']
    bg = gizeh.rectangle(lx=video_w, ly=video_h,
                         xy=(video_w / 2, video_h / 2),
                         fill=(1, 1, 1))

    named_shapes = dict()

    def make_frame(t):
        surface = gizeh.Surface(video_w, video_h)

        bg.draw(surface)

        # draw all shapes in named_shapes (they are removed when hidden via
        # hide command)
        for _, shape in named_shapes.items():
            shape.draw(surface)

        num_frame = int(config['speed'] * t)
        commands = command_frames[num_frame]
        for command in commands:
            # if there is a hide key, this command is a hide command
            if 'hide' in command:
                del named_shapes[command['hide']]

            # if there is not a hide key, this command is a draw command
            # (and a register command if it provides a name)
            else:
                # make args keys non-unicode-flagged strings for easy access
                shape_args = {
                    str(key): val
                    for key, val in command['args'].items()
                }
                shape_method = command['type']

                gizeh_fn = getattr(gizeh, shape_method)
                shape = gizeh_fn(**shape_args)

                if 'name' in command:
                    named_shapes[command['name']] = shape

                shape.draw(surface)

        return surface.get_npimage()

    video_duration = int(config['num_frames']) / float(config['speed'])
    video = VideoClip(make_frame=make_frame, duration=video_duration)
    video.fps = config['speed']
    return video
