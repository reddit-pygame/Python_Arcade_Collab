import random
import pygame as pg

from data.core import prepare
from data.components.state_machine import _State
from . import constants, level, actors


class Game(_State):
    """This scene is active during the gameplay phase."""
    def __init__(self, controller):
        super(Game, self).__init__(controller)
        self.screen_rect = pg.Rect((0, 0), prepare.RENDER_SIZE)
        ship = random.choice(list(constants.GFX["ships"].values()))
        self.player = actors.Player((0,0), ship)
        self.level = level.Level(self.screen_rect.copy(), self.player)

    def update(self, surface, keys, current_time, dt, scale):
        dt /= 1000.0
        self.level.update(keys, dt)
        self.draw(surface)
        
    def draw(self, surface):
        surface.fill(constants.BACKGROUND_COLOR)
        self.level.draw(surface)
