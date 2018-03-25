"""
Contained here are resource loading functions, command line argument processing,
Timer and simple Animation classes and various other useful tools.
"""

import os
import copy
import argparse

import pygame as pg


class _KwargMixin(object):
    """
    Useful for classes that require a lot of keyword arguments for
    customization.
    """
    def process_kwargs(self, name, defaults, kwargs):
        """
        Arguments are a name string (displayed in case of invalid keyword);
        a dictionary of default values for all valid keywords;
        and the kwarg dict.
        """
        settings = copy.deepcopy(defaults)
        for kwarg in kwargs:
            if kwarg in settings:
                if isinstance(kwargs[kwarg], dict):
                    settings[kwarg].update(kwargs[kwarg])
                else:
                    settings[kwarg] = kwargs[kwarg]
            else:
                message = "{} has no keyword: {}"
                raise AttributeError(message.format(name, kwarg))
        for setting in settings:
            setattr(self, setting, settings[setting])


### Mouse position functions
def scaled_mouse_pos(scale, pos=None):
    """
    Return the mouse position adjusted for screen size if no pos argument is
    passed and returns pos adjusted for screen size if pos is passed.
    """
    x,y = pg.mouse.get_pos() if pos is None else pos
    return (int(x*scale[0]), int(y*scale[1]))


### Resource loading functions.
def load_all_gfx(directory, colorkey=(255,0,255), accept=(".png",".jpg",".bmp")):
    """
    Load all graphics with extensions in the accept argument.  If alpha
    transparency is found in the image the image will be converted using
    convert_alpha().  If no alpha transparency is detected image will be
    converted using convert() and colorkey will be set to colorkey.
    """
    graphics = {}
    for pic in os.listdir(directory):
        name,ext = os.path.splitext(pic)
        if ext.lower() in accept:
            img = pg.image.load(os.path.join(directory, pic))
            if img.get_alpha():
                img = img.convert_alpha()
            else:
                img = img.convert()
                img.set_colorkey(colorkey)
            graphics[name]=img
    return graphics


def _generic_resoure_loader(directory, accept):
    """
    Loads resources from given directory skipping file extensions not in accept.
    """
    resources = {}
    for resource in os.listdir(directory):
        name, ext = os.path.splitext(resource)
        if ext.lower() in accept:
            resources[name] = os.path.join(directory, resource)
    return resources


def load_all_music(directory, accept=(".wav", ".mp3", ".ogg", ".mdi")):
    """
    Create a dictionary of paths to music files in given directory
    if their extensions are in accept.
    """
    return _generic_resoure_loader(directory, accept)


def load_all_fonts(directory, accept=(".ttf",)):
    """
    Create a dictionary of paths to font files in given directory
    if their extensions are in accept.
    """
    return _generic_resoure_loader(directory, accept)


def load_all_movies(directory, accept=(".mpg",)):
    """
    Create a dictionary of paths to movie files in given directory
    if their extensions are in accept.
    """
    return _generic_resoure_loader(directory, accept)


def load_all_sfx(directory, accept=(".wav", ".mp3", ".ogg", ".mdi")):
    """
    Load all sfx of extensions found in accept.  Unfortunately it is
    common to need to set sfx volume on a one-by-one basis.  This must be done
    manually if necessary in the calling module.
    """
    effects = {}
    for fx in os.listdir(directory):
        name,ext = os.path.splitext(fx)
        if ext.lower() in accept:
            effects[name] = pg.mixer.Sound(os.path.join(directory, fx))
    return effects


def strip_from_sheet(sheet, start, size, columns, rows=1):
    """
    Strips individual frames from a sprite sheet given a start location,
    sprite size, and number of columns and rows.
    """
    frames = []
    for j in range(rows):
        for i in range(columns):
            location = (start[0]+size[0]*i, start[1]+size[1]*j)
            frames.append(sheet.subsurface(pg.Rect(location, size)))
    return frames


def strip_coords_from_sheet(sheet, coords, size):
    """
    Strip specific coordinates from a sprite sheet.
    """
    frames = []
    for coord in coords:
        location = (coord[0]*size[0], coord[1]*size[1])
        frames.append(sheet.subsurface(pg.Rect(location, size)))
    return frames


def get_cell_coordinates(rect, point, size):
    """
    Find the cell of size, within rect, that point occupies.
    """
    cell = [None, None]
    point = (point[0]-rect.x, point[1]-rect.y)
    cell[0] = (point[0]//size[0])*size[0]
    cell[1] = (point[1]//size[1])*size[1]
    return tuple(cell)


def cursor_from_image(image):
    """
    Take a valid cursor image and create a mouse cursor.
    """
    colors = {(0,0,0,255) : "X",
              (255,255,255,255) : "."}
    rect = image.get_rect()
    icon_string = []
    for j in range(rect.height):
        this_row = []
        for i in range(rect.width):
            pixel = tuple(image.get_at((i,j)))
            this_row.append(colors.get(pixel, " "))
        icon_string.append("".join(this_row))
    return icon_string


def get_cli_args(caption, win_pos, start_size):
    """
    Modify prepare module globals based on command line arguments,
    quickly force settings for debugging.
    """
    parser = argparse.ArgumentParser(description='{} Arguments'.format(caption))
    parser.add_argument('-c','--center', action='store_false',
        help='position starting window at (0,0), sets SDL_VIDEO_CENTERED to false')
    parser.add_argument('-w','--winpos', nargs=2, default=win_pos, metavar=('X', 'Y'),
        help='position starting window at (X,Y), default is (0,0)')
    parser.add_argument('-s' , '--size', nargs=2, default=start_size, metavar=('WIDTH', 'HEIGHT'),
        help='set window size to WIDTH HEIGHT, default is {}'.format(start_size))
    parser.add_argument('-f' , '--fullscreen', action='store_true',
        help='start in fullscreen')
    parser.add_argument('-m' , '--music_off', action='store_true',
        help='start with no music')
    parser.add_argument('-S', '--straight', action='store', type=str,
        help='go straight to the named scene')
    parser.add_argument('-d', '--debug', action='store_true',
        help='run game in debug mode')
    parser.add_argument('-F', '--FPS', action='store_true',
        help='show FPS in title bar')
    parser.add_argument('-p', '--profile', action='store_true',
        help='run game with profiling')
    args = vars(parser.parse_args())
    # Check each condition.
    if not args['center'] or (args['winpos'] != win_pos): # If -c or -w options
        args['center'] = False
    if args['size'] != start_size: # If screen size is different
        args['resizable'] = False
    if args['fullscreen']:
        args['center'] = False
        args['resizable'] = False
    return args


class Anim(object):
    """
    A class to simplify the act of adding animations to sprites.
    """
    def __init__(self, frames, fps, loops=-1):
        """
        The argument frames is a list of frames in the correct order;
        fps is the frames per second of the animation;
        loops is the number of times the animation will loop (a value of -1
        will loop indefinitely).
        """
        self.frames = frames
        self.fps = fps
        self.frame = 0
        self.timer = None
        self.loops = loops
        self.loop_count = 0
        self.done = False

    def get_next_frame(self, now):
        """
        Advance the frame if enough time has elapsed and the animation has
        not finished looping.
        """
        if not self.timer:
            self.timer = now
        if not self.done and now-self.timer > 1000.0/self.fps:
            self.frame = (self.frame+1)%len(self.frames)
            if not self.frame:
                self.loop_count += 1
                if self.loops != -1 and self.loop_count >= self.loops:
                    self.done = True
                    self.frame -= 1
            self.timer = now
        return self.frames[self.frame]

    def reset(self):
        """
        Set frame, timer, and loop status back to the initialized state.
        """
        self.frame = 0
        self.timer = None
        self.loop_count = 0
        self.done = False


class Timer(object):
    """
    A very simple timer for events that are not directly tied to animation.
    """
    def __init__(self, delay, ticks=-1):
        """
        The delay is given in milliseconds; ticks is the number of ticks the
        timer will make before flipping self.done to True.  Pass a value
        of -1 to bypass this.
        """
        self.delay = delay
        self.ticks = ticks
        self.tick_count = 0
        self.timer = None
        self.done = False

    def check_tick(self, now):
        """
        Returns true if a tick worth of time has passed.
        """
        if not self.timer:
            self.timer = now
            return True
        elif not self.done and now-self.timer > self.delay:
            self.tick_count += 1
            self.timer = now
            if self.ticks != -1 and self.tick_count >= self.ticks:
                self.done = True
            return True
