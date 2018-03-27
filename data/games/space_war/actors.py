"""
This module contains the Player class for the user controlled character.
"""

import math
import pygame as pg

import constants


class Player(pg.sprite.Sprite):
    """
    This class represents our user controlled character.
    """
    def __init__(self, pos, image, speed=420, *groups):
        super(Player, self).__init__(*groups)
        self.top_speed = speed
        self.acceleration = speed*2
        self.velocity = [0.0, 0.0]
        self.original = pg.transform.rotozoom(image, 0, constants.SCALE_FACTOR)
        self.angle = 270.0
        self.image = pg.transform.rotozoom(self.original, -self.angle, 1)
        self.rect = self.image.get_rect(center=pos)
        self.true_pos = list(self.rect.center)
        self.angular_speed = 200.0

    def update(self, keys, bounding, dt):
        """
        Updates the players position based on currently held keys.
        """
        self.check_keys(keys, dt)
        self.true_pos[0] += self.velocity[0]*dt
        self.true_pos[1] += self.velocity[1]*dt
        self.rect.center = self.true_pos
        if not bounding.contains(self.rect):
            self.on_boundary_collision(bounding)

    def on_boundary_collision(self, bounding):
        """
        If the ship hits the edge of the map, zero acceleration in that
        direction.
        """
        if self.rect.x < bounding.x or self.rect.right > bounding.right:
            self.velocity[0] = 0.0
        if self.rect.y < bounding.y or self.rect.bottom > bounding.bottom:
            self.velocity[1] = 0.0 
        self.rect.clamp_ip(bounding)
        self.true_pos = list(self.rect.center)

    def check_keys(self, keys, dt):
        """
        Call methods to check keys for both rotation and thrust.
        """
        self.rotate(keys, dt)
        self.thrust(keys, dt)

    def rotate(self, keys, dt):
        """
        If either rotation key is held adjust angle, image,
        and rect appropriately.
        """
        for key in constants.ROTATE:
            if keys[key]:
                self.angle += self.angular_speed*constants.ROTATE[key]*dt
                self.angle %= 360
                self.image = pg.transform.rotozoom(self.original,-self.angle,1)
                self.rect = self.image.get_rect(center=self.rect.center)

    def thrust(self, keys, dt):
        """
        Adjust velocity if the thrust key is held.
        """
        if keys[constants.THRUST]:
            rads = math.radians(self.angle)
            self.velocity[0] += self.acceleration*math.cos(rads)*dt
            self.velocity[1] += self.acceleration*math.sin(rads)*dt
            self.restrict_speed()

    def restrict_speed(self):
        """
        Restricts the velocity components so that the top speed is never
        exceeded.
        """
        adj, op = self.velocity
        if math.hypot(adj, op) > self.top_speed:
            angle = math.atan2(op, adj) # Angle of movement; not ship direction
            self.velocity[0] = self.top_speed*math.cos(angle)
            self.velocity[1] = self.top_speed*math.sin(angle)

    def draw(self, surface):
        """
        Basic draw function. (not  used if drawing via groups)
        """
        surface.blit(self.image, self.rect)
