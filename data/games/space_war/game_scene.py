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
from data.components.state_machine import _State, StateMachine
from data.components.labels import FlashingText, Label

from . import constants, states


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
        machine_states = {"GAME" : states.Game(self)}
        self.state_machine = StateMachine(True)
        self.state_machine.setup_states(machine_states)
        self.state_machine.start_state("GAME")

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

    def update(self, surface, keys, current_time, dt, scale):
        """
        Updates the game scene screen.
        """
        if self.state_machine.done:
            self.done = True
            self.next = "lobby"
        self.state_machine.update(surface, keys, current_time, dt, scale)

    def get_event(self, event, scale):
        if event.type == pg.QUIT:
            self.done = True
            self.quit = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                self.done  = True
                self.next = "lobby"
        self.state_machine.get_event(event, scale)
