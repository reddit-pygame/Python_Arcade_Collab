import random
import collections
import pygame as pg

from data.core import prepare
from data.components.state_machine import _State, StateMachine

from . import constants, states


class Scene(_State):
    """
    This State is updated while our game is running.
    The game autodetection requires that the name of this class not be changed.
    """
    def __init__(self, controller):
        super(Scene, self).__init__(controller)
        self.screen_rect = pg.Rect((0, 0), prepare.RENDER_SIZE)
        machine_states = {"STARTUP" : states.AnyKey("Start!", self),
                          "GAME" : states.Game(self),
                          "DEAD" : states.YouDead("Dead.", self)}
        self.state_machine = StateMachine(True)
        self.state_machine.setup_states(machine_states)
        self.state_machine.start_state("STARTUP")

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
        self.state_machine.get_event(event, scale)
