"""
Includes many useful constants used across the program.
"""

import os
import pygame as pg

from data.core import tools
from data.core.prepare import ARGS, CAPTION


DEBUG = bool(ARGS['debug'])

RENDER_SIZE = (928, 696)
RESOLUTIONS = [(600, 400), (800, 600), (928, 696), (1280, 960), (1400, 1050)]

# Some commonly used colors.
BACKGROUND_BASE = (5, 5, 15) # Pure Black is often too severe.
LOW_LIGHT_GREEN = (0, 166, 8)
HIGH_LIGHT_GREEN = (0, 232, 37)

# Resource loading (Fonts and music just contain path names).
FONTS = tools.load_all_fonts(os.path.join("resources", "fonts"))
MUSIC = tools.load_all_music(os.path.join("resources", "music"))
SFX   = tools.load_all_sfx(os.path.join("resources", "sound"))
GFX   = tools.load_all_gfx(os.path.join("resources", "graphics"))

# Music played on program start.
TITLE_TRACK = MUSIC["Nils_505_Feske_-_03_-_Balibulu"]
