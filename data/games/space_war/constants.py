import os
import pygame as pg

from data.core import tools


PATH = os.path.join(".", "data", "games", "space_war", "resources")

BACKGROUND_COLOR = (10, 20, 30)
SCALE_FACTOR = 0.3 # For scaleing down ship images.
ROTATE = {pg.K_RIGHT: 1, pg.K_LEFT : -1}
THRUST = pg.K_UP

GFX = None # Loaded and Unloaded on startup and cleanup.


def load():
    """
    Load resources. Called by the game scene on startup.
    """
    global GFX
    if GFX is None:
        GFX = tools.load_all_gfx(PATH)
        GFX["ships"] = tools.load_all_gfx(os.path.join(PATH, "ships"))
        GFX["big_stars"] = tools.tile_surface((2048,2048), GFX["stars"], True)


def unload():
    """
    Unload resources. Called by the game scene on cleanup.
    """
    global GFX
    if GFX:
        GFX["ships"].clear()
        GFX.clear()
    GFX = None
