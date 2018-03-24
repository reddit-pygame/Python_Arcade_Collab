from random import randint

import pygame as pg

from data.core import prepare
from data.components.state_machine import _State


class SnakeSplash(_State):
    """
    This State is updated while our game shows the splash screen.
    """    
    def __init__(self, controller):
        super(SnakeSplash, self).__init__(controller)
        self.next = "title_screen"
        self.screen_rect = pg.Rect((0, 0), prepare.RENDER_SIZE)
        self.timeout = 7
        self.alpha = 0
        self.alpha_speed  = 2  # Alpha change per frame.
        self.image = prepare.GFX["splash2"]
        self.image.set_alpha(self.alpha)
        self.rect = self.image.get_rect(center=self.screen_rect.center)

    def startup(self, current_time, persistent):
        """This method will be called each time the state resumes."""
        self.start_time = current_time
        self.persist = persistent

    def update(self, surface, keys, current_time, dt, scale):
        """Updates the splash screen."""
        self.now = current_time
        self.alpha = min(self.alpha + self.alpha_speed, 255)
        self.image.set_alpha(self.alpha)
        if self.now - self.start_time > 1000.0 * self.timeout:
            self.done = True
        self.draw(surface)

    def draw(self, surface):
        surface.fill(prepare.BACKGROUND_BASE)
        surface.blit(self.image, self.rect)

    def get_event(self, event, scale):
        if event.type == pg.QUIT:
            self.done = True
            self.quit = True
        elif event.type == pg.KEYUP:
            self.done  = True
            if event.key == pg.K_ESCAPE:
                self.quit = True
        elif event.type == pg.MOUSEBUTTONUP:
            self.done = True
