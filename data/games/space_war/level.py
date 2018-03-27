"""
This module contains the Level class.
Drawing and updating of actors should occur here.
"""

import pygame as pg

from data.core import tools
from . import constants


class Level(object):
    """
    This class represents the whole starscape.  The starscape consists of
    three star layers.  The player is drawn and updated by this class.
    The player is contained in a pg.sprite.GroupSingle group.
    """
    def __init__(self, viewport, player):
        self.image = constants.GFX["big_stars"].copy()
        self.rect = self.image.get_rect()
        player.rect.midbottom = self.rect.centerx, self.rect.bottom-50
        player.true_pos = list(player.rect.center)
        self.player_singleton = pg.sprite.GroupSingle(player)
        self.make_layers()
        self.viewport = viewport
        self.update_viewport(True)
        self.mid_viewport = self.viewport.copy()
        self.mid_true = list(self.mid_viewport.topleft)
        self.base_viewport = self.viewport.copy()
        self.base_true = list(self.base_viewport.topleft)

    def make_layers(self):
        """
        Create the middle and base image of the stars.
        self.image scrolls with the player, self.mid_image scrolls at
        half the speed, and self.base always stays fixed. 
        """
        w, h = self.image.get_size()
        shrink = pg.transform.smoothscale(self.image, (w//2, h//2))
        self.mid_image = tools.tile_surface((w,h), shrink, True)
        shrink = pg.transform.smoothscale(self.image, (w//4, h//4))
        self.base = tools.tile_surface((w,h), shrink, True)

    def update(self, keys, dt):
        """
        Updates the player and then adjusts the viewport with respect to the
        player's new position.
        """
        self.player_singleton.update(keys, self.rect, dt)
        self.update_viewport()

    def update_viewport(self, start=False):
        """
        The viewport will stay centered on the player unless the player
        approaches the edge of the map.
        """
        old_center = self.viewport.center
        self.viewport.center = self.player_singleton.sprite.rect.center
        self.viewport.clamp_ip(self.rect)
        change = (self.viewport.centerx-old_center[0],
                  self.viewport.centery-old_center[1])
        if not start:
            self.mid_true[0] += change[0]*0.5
            self.mid_true[1] += change[1]*0.5
            self.mid_viewport.topleft = self.mid_true
            self.base_true[0] += change[0]*0.1
            self.base_true[1] += change[1]*0.1
            self.base_viewport.topleft = self.base_true

    def draw(self, surface):
        """
        Blit and clear actors on the self.image layer.
        Then blit appropriate viewports of all layers.
        """
        self.player_singleton.clear(self.image, clear_callback)
        self.player_singleton.draw(self.image)
        surface.blit(self.base, (0,0), self.base_viewport)
        surface.blit(self.mid_image, (0,0), self.mid_viewport)
        surface.blit(self.image, (0,0), self.viewport)


def clear_callback(surface, rect):
    """
    We need this callback because the clearing background contains
    transparency.  We need to fill the rect with transparency first.
    """
    surface.fill((0,0,0,0), rect)
    surface.blit(constants.GFX["big_stars"], rect, rect)
