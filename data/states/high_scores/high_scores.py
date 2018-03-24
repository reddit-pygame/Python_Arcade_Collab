import pygame as pg

from data.core import prepare
from data.components.labels import FlashingText, Label
from data.components.state_machine import _State


class HighScores(_State):
    """
    Shown by clicking the high scores button in the lobby page.
    """
    def __init__(self, controller):
        super(HighScores, self).__init__(controller)
        self.next = None
        self.screen_rect = pg.Rect((0, 0), prepare.RENDER_SIZE)
        cent_x = self.screen_rect.centerx
        self.anykey = FlashingText((cent_x, 650), "[Press Any Key]",
                                   "Fixedsys500c", pg.Color("gold"), 30, 350)
        text= "Under Construction"
        self.title = Label(prepare.FONTS["Fixedsys500c"], 72, text,
                         pg.Color("white"), {"center": self.screen_rect.center})

    def update(self, surface, keys, current_time, dt, scale):
        """
        Updates the highcore screen.
        """
        self.anykey.update(current_time)
        self.draw(surface)

    def draw(self, surface):
        surface.fill(prepare.BACKGROUND_BASE)
        self.title.draw(surface)
        surface.blit(self.anykey.image, self.anykey.rect)

    def get_event(self, event, scale):
        if event.type == pg.QUIT:
            self.done = True
            self.quit = True
        elif event.type == pg.KEYUP:
            self.done  = True
            self.next = "lobby"
