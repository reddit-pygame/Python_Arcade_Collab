"""
This module initializes the display and processes command line arguments.
It must be imported before any resource loading occurs.
"""

import os
import pygame as pg

from data.core import tools


CAPTION = "Python Arcade Collab"
START_SIZE = (800, 600)
WIN_POS = (0, 0)


# Process command line arguments.
ARGS = tools.get_cli_args(CAPTION, WIN_POS, START_SIZE)
# Adjust settings based on args
START_SIZE = int(ARGS['size'][0]), int(ARGS['size'][1])


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
