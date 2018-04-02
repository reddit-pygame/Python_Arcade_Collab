import pygame as pg

from data.core import tools, prepare
from data.components.labels import FlashingText
from data.components.state_machine import _State


class TitleScreen(_State):
    """
    Initial state of the game.
    """
    def __init__(self, controller):
        super(TitleScreen, self).__init__(controller)
        self.next = "lobby"
        self.screen_rect = pg.Rect((0, 0), prepare.RENDER_SIZE)
        self.title = prepare.GFX["collab_title"]
        cent_x = self.screen_rect.centerx
        self.title_rect = self.title.get_rect(centerx=cent_x, y=100)
        anykey_args = (prepare.FONTS["Fixedsys500c"], 30, "[Please Insert Coin]",
                       pg.Color("gold"), {"center" : (cent_x, 650)}, 350)
        self.anykey = FlashingText(*anykey_args)
        
    def get_event(self, event, scale):
        if event.type == pg.QUIT:
            self.done = True
            self.quit = True
        elif event.type == pg.KEYUP:
            self.done = True
            if event.key == pg.K_ESCAPE:
                self.quit = True

    def update(self, surface, keys, current_time, dt, scale):
        self.anykey.update(current_time)
        self.draw(surface)

    def draw(self, surface):
        surface.fill(prepare.BACKGROUND_BASE)
        surface.blit(self.title, self.title_rect)
        surface.blit(self.anykey.image, self.anykey.rect)
