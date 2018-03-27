"""
This is the template for the games accessible from the lobby.
To add your own game to the lobby, copy this folder into games,
and change the folder name to the name of your game.
Then get to work.
"""

import os
import random
import pygame as pg

from data.core import prepare, tools
from data.components.state_machine import _State
from data.components.labels import FlashingText, Label

from . import constants, level, actors


class Scene(_State):
    """
    This State is updated while our game is running.
    The game autodetection requires that the name of this class not be changed.
    """
    def __init__(self, controller):
        super(Scene, self).__init__(controller)
        constants.load()
        self.next = None
        self.screen_rect = pg.Rect((0, 0), prepare.RENDER_SIZE)
        cent_x = self.screen_rect.centerx
        ship = random.choice(list(constants.GFX["ships"].values()))
        self.player = actors.Player((0,0), ship)
        self.level = level.Level(self.screen_rect.copy(), self.player)

    def update(self, surface, keys, current_time, dt, scale):
        """
        Updates the game scene and then draws the screen.
        """
        dt /= 1000.0
        self.level.update(keys, dt)
        self.draw(surface)

    def startup(self, persistent):
        """
        Load game specific resources into constants.
        """
        constants.load()
        super(Scene, self).startup(persistent)

    def cleanup(self):
        """
        Unload game specific resources from constants to reclaim memory.
        """
        constants.unload()
        return super(Scene, self).cleanup()

    def draw(self, surface):
        """
        Put all drawing logic here. Called at the end of the update method.
        """
        surface.fill(constants.BACKGROUND_COLOR)
        self.level.draw(surface)

    def get_event(self, event, scale):
        """
        Process all events here. States must not have their own embedded
        event loops as this cuts the rest of the program off from events.
        If you would like to use mouse position events you will need to scale it
        with scaled_mouse_pos found in data.core.tools.py.
        """
        if event.type == pg.QUIT:
            self.done = True
            self.quit = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                self.done  = True
                self.next = "lobby"
