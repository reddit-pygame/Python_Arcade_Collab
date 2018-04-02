import random
import pygame as pg

from data.core import constants as prog_consts
from data.components.state_machine import _State
from data.components.labels import FlashingText, Label

from . import actors, constants, tools


class AnyKey(_State):
    """
    A state for the start and death scene.
    """
    def __init__(self, title, controller):
        super(AnyKey, self).__init__(controller)
        self.next = None
        self.screen_rect = pg.Rect((0, 0), prog_consts.RENDER_SIZE)
        cent_x = self.screen_rect.centerx
        anykey_args = (prog_consts.FONTS["Fixedsys500c"], 50, "[Press Any Key]",
                       pg.Color("white"), {"center" : (cent_x, 625)}, 350)
        self.anykey = FlashingText(*anykey_args)
        self.title = Label(prog_consts.FONTS["Fixedsys500c"], 100, title,
                         pg.Color("white"), {"centerx": cent_x, "y" : 50})
        self.screen_copy = None

    def draw(self, surface):
        if self.screen_copy:
            surface.blit(self.screen_copy, (0,0))
        else:
            surface.fill(prog_consts.BACKGROUND_BASE)
        self.title.draw(surface)
        surface.blit(self.anykey.image, self.anykey.rect)

    def update(self, surface, keys, current_time, dt, scale):
        self.anykey.update(current_time)
        self.draw(surface)

    def get_event(self, event, scale):
        """
        Switch to game on keydown.
        """
        if event.type == pg.KEYDOWN:
            self.done = True
            self.next = "GAME"


class Game(_State):
    """This scene is active during the gameplay phase."""
    def __init__(self, controller):
        super(Game, self).__init__(controller)
        self.levels = tools.make_levels()
        self.reset()

    def reset(self):
        """Prepare for next run."""
        self.snake = actors.Snake()
        self.walls = self.make_walls()
        self.apple = actors.Apple(self.walls, self.snake)

    def make_walls(self):
        """Make the borders, and load a random level."""
        walls = set()
        for i in range(-1, constants.BOARD_SIZE[0]+1):
            walls.add((i, -1))
            walls.add((i, constants.BOARD_SIZE[1]))
        for j in range(-1, constants.BOARD_SIZE[1]+1):
            walls.add((-1, j))
            walls.add((constants.BOARD_SIZE[0], j))
        walls |= random.choice(self.levels)
        return walls

    def get_event(self, event, scale):
        """Pass any key presses on to the snake."""
        if event.type == pg.KEYDOWN:
            self.snake.get_key_press(event.key)

    def update(self, surface, keys, current_time, dt, scale):
        """Update the snake and check if it has died."""
        self.snake.update(current_time)
        self.snake.check_collisions(self.apple, self.walls)
        if self.snake.dead:
            self.done = True
            self.next = "DEAD"
        else:
            self.draw(surface)

    def cleanup(self):
        self.reset()
        return super(Game, self).cleanup()
        
    def draw(self, surface):
        """Draw the food, snake, and walls."""
        surface.fill(constants.COLORS["background"])
        tools.draw_cell(surface, self.apple.position,
                        self.apple.color, constants.PLAY_RECT.topleft)
        offset = constants.PLAY_RECT.topleft
        for wall in self.walls:
            tools.draw_cell(surface, wall, constants.COLORS["walls"], offset)
        self.snake.draw(surface, offset=offset)


class YouDead(AnyKey):
    def startup(self, persistant):
        super(YouDead, self).startup(persistant)
        surf = pg.Surface(prog_consts.RENDER_SIZE).convert()
        screen_copy = pg.display.get_surface().copy()
        scale_args = (screen_copy, prog_consts.RENDER_SIZE, surf)
        pg.transform.smoothscale(*scale_args)
        self.screen_copy = surf

    def get_event(self, event, scale):
        """Switch to lobby on keydown."""
        if event.type == pg.KEYDOWN:
            self.quit = True
