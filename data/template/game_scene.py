"""
This is the template for the games accessible from the lobby.
To add your own game to the lobby, copy this folder into games,
and change the folder name to the name of your game.
Then get to work.
"""

import pygame as pg

from data.core import prepare
from data.components.state_machine import _State
from data.components.labels import FlashingText, Label


class Scene(_State):
    """
    This State is updated while our game is running.
    The game autodetection requires that the name of this class not be changed.
    """
    def __init__(self, controller):
        super(Scene, self).__init__(controller)
        self.next = None
        self.screen_rect = pg.Rect((0, 0), prepare.RENDER_SIZE)
        cent_x = self.screen_rect.centerx
        self.anykey = FlashingText((cent_x, 650), "[Press Any Key]",
                                   "Fixedsys500c", pg.Color("gold"), 30, 350)
        self.title = Label(prepare.FONTS["Fixedsys500c"], 72, "Your game here!",
                         pg.Color("white"), {"center": self.screen_rect.center})

    def startup(self, persistent):
        """
        This method will be called each time the state resumes.
        """
        self.start_time = pg.time.get_ticks()
        self.persist = persistent

    def cleanup(self):
        """
        Add variables that should persist to the self.persist dictionary.
        Then reset State.done to False.
        """
        self.done = False
        return self.persist

    def update(self, surface, keys, current_time, dt, scale):
        """
        Updates the game scene and then draws the screen.
        """
        self.anykey.update(current_time)
        self.draw(surface)

    def draw(self, surface):
        """
        Put all drawing logic here. Called at the end of the update method.
        """
        surface.fill(prepare.BACKGROUND_BASE)
        self.title.draw(surface)
        surface.blit(self.anykey.image, self.anykey.rect)

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
            self.done  = True
            self.next = "lobby"
