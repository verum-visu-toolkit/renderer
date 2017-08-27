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


def render(shapes=None, frames=None, config=None):
    # shapes: [{'type':'circle', 'args': { radius: 'var1', xy: ['var2',
    # 'var3'], fill: [1,0,0}]}]

    video_w, video_h = int(config['width']), int(config['height'])

    def make_frame(t):
        surface = gizeh.Surface(video_w, video_h)

        for shape_def in shapes:
            shape_args = {
                arg: calc_shape_prop(arg, t)
                for arg in shape_def['args']
            }
            shape_method = shape_def['type']
            shape = gizeh[shape_method](**shape_args)
            shape.draw(surface)

        return surface.get_npimage()

    # frames: e.g. [[{ 'var1': 3.23, 'var2': '23423.33', 'var3': 323 }], ...]
    def calc_shape_prop(prop_name, t):
        if type(prop_name).__name__ == str.__name__:
            return frames[t][prop_name]
        else:  # if `prop_name` isn't a string, assume it's a constant value
            #  and return it instead of getting a value from the frame
            return prop_name

    video_duration = int(config['num_frames']) / float(config['speed'])
    video = VideoClip(make_frame=make_frame, duration=video_duration)
    video.set_fps(float(config['speed']))
    return video
