import random
import collections
import pygame as pg

try:
    import Queue as queue
except ImportError:
    import queue

from . import constants, tools


class Apple(object):
    """Something edible.  Causes unrestricted growth in some animals."""
    def __init__(self, walls, snake):
        self.position = self.respawn(snake.body_set|walls)
        self.walls = walls
        self.color = constants.COLORS["apple"]

    def collide_with(self, snake):
        """If eaten find a new home."""
        self.position = self.respawn(snake.body_set|self.walls)

    def respawn(self, obstacles):
        """Don't land in a wall or inside the snake."""
        position = tuple(random.randrange(constants.BOARD_SIZE[i]) for i in (0,1))
        while position in obstacles:
            position = tuple(random.randrange(constants.BOARD_SIZE[i]) for i in (0,1))
        return position


class Snake(object):
    """Green and snakey."""
    def __init__(self):
        self.color = constants.COLORS["snake"]
        self.speed = 8 # Cells per second
        self.direction = "up"
        self.vector = constants.DIRECT_DICT[self.direction]
        self.body = [(10, 18), (10,17)]
        self.body_set = set(self.body)
        self.growing = False
        self.grow_number = 0
        self.timer = 0
        self.dead = False
        self.direction_queue = queue.Queue(5)

    def update(self, now):
        """Add new cell for the head.  If not growing, delete the tail."""
        if not self.dead and now-self.timer >= 1000.0/self.speed:
            self.timer = now
            self.change_direction()
            next_cell = [self.body[-1][i]+self.vector[i] for i in (0,1)]
            self.body.append(tuple(next_cell))
            if not self.growing:
                del self.body[0]
            else:
                self.grow()
            self.body_set = set(self.body)

    def change_direction(self):
        """
        Check direction queue for a new direction.  Directions parallel
        to the snakes current movement are ignored.
        """
        try:
            new = self.direction_queue.get(block=False)
        except queue.Empty:
            new = self.direction
        if new not in (self.direction, constants.OPPOSITES[self.direction]):
            self.vector = constants.DIRECT_DICT[new]
            self.direction = new

    def grow(self):
        """Increment grow number and reset if done."""
        self.grow_number += 1
        if self.grow_number == constants.GROWTH_PER_APPLE:
            self.grow_number = 0
            self.growing = False

    def check_collisions(self, apple, walls):
        """Get apples and collide with body and walls."""
        if self.body[-1] == apple.position:
            apple.collide_with(self)
            self.growing = True
        elif self.body[-1] in walls:
            self.dead = True
        elif any(val > 1 for val in collections.Counter(self.body).values()):
            self.dead = True

    def get_key_press(self, key):
        """
        Add directions to the direction queue if key in KEY_MAPPING is pressed.
        """
        for keys in constants.KEY_MAPPING:
            if key in keys:
                try:
                    self.direction_queue.put(constants.KEY_MAPPING[keys], block=False)
                    break
                except queue.Full:
                    pass

    def draw(self, surface, offset=(0,0)):
        """Draw the whole body, then the head."""
        for cell in self.body:
            tools.draw_cell(surface, cell, self.color, offset)
        tools.draw_cell(surface, self.body[-1], constants.COLORS["head"], offset)
