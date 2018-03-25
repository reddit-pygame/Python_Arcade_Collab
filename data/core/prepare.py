"""
This module performs various tasks related to starting up the program.
These include initializing the display, processing command line arguments,
creating dictionaries of resources, and starting the music.

Many useful constants are also defined here so you will often find this file
imported across the entire program.
"""

import os
import pygame as pg

from data.core import tools


CAPTION = "Python Arcade Collab"
TITLE_TRACK = "Nils_505_Feske_-_03_-_Balibulu"
START_SIZE = (800, 600)
RENDER_SIZE = (928, 696)
RESOLUTIONS = [(600, 400), (800, 600), (928, 696), (1280, 960), (1400, 1050)]
WIN_POS = (0, 0)

# Some commonly used colors.
BACKGROUND_BASE = (5, 5, 15) # Pure Black is often too severe.
LOW_LIGHT_GREEN = (0, 166, 8)
HIGH_LIGHT_GREEN = (0, 232, 37)

# Process command line arguments.
ARGS = tools.get_cli_args(CAPTION, WIN_POS, START_SIZE)
# Adjust settings based on args
START_SIZE = int(ARGS['size'][0]), int(ARGS['size'][1])
DEBUG = bool(ARGS['debug'])


# Pre-initialize the mixer for less delay before a sound plays.
pg.mixer.pre_init(44100, -16, 1, 512)

# Initialization of display.
pg.init()
if ARGS['center']:
    os.environ['SDL_VIDEO_CENTERED'] = "True"
else:
    os.environ['SDL_VIDEO_WINDOW_POS'] = '{},{}'.format(*ARGS['winpos'])
pg.display.set_caption(CAPTION)
if ARGS['fullscreen']:
    pg.display.set_mode(START_SIZE, pg.FULLSCREEN)
elif ARGS["resizable"]:
    pg.display.set_mode(START_SIZE, pg.RESIZABLE)
    pg.event.clear(pg.VIDEORESIZE)
else:
    pg.display.set_mode(START_SIZE)


# Resource loading (Fonts and music just contain path names).
FONTS = tools.load_all_fonts(os.path.join("resources", "fonts"))
MUSIC = tools.load_all_music(os.path.join("resources", "music"))
SFX   = tools.load_all_sfx(os.path.join("resources", "sound"))
GFX   = tools.load_all_gfx(os.path.join("resources", "graphics"))


# It's time to start the music, it's time to light the lights.
pg.mixer.music.load(MUSIC[TITLE_TRACK])
pg.mixer.music.set_volume(.2)
if not ARGS["music_off"]:
    pg.mixer.music.play(-1)
