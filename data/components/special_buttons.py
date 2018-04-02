import os
import pygame as pg

from data.core import prepare
from data.components.labels import Button, Label


class NeonButton(Button):
    """
    Neon sign style button that glows on mouseover.
    """
    width = 182
    height = 58
    
    def __init__(self, pos, text, font_size=32,
                 call=None, args=None, *groups, **kwargs):
        text = text.replace("_", " ")
        blank = prepare.GFX["neon_button_blank"].copy()
        on_label = Label(prepare.FONTS["Fixedsys500c"], font_size, text,
                         prepare.HIGH_LIGHT_GREEN, {"center": (91, 29)})
        off_label = Label(prepare.FONTS["Fixedsys500c"], font_size, text,
                          prepare.LOW_LIGHT_GREEN, {"center": (91, 29)})
        on_image = blank.subsurface((self.width, 0, self.width, self.height))
        off_image = blank.subsurface((0, 0, self.width, self.height))
        on_label.draw(on_image)
        off_label.draw(off_image)
        rect = on_image.get_rect(topleft=pos)
        settings = {"hover_image" : on_image,
                    "idle_image"  : off_image,
                    "call"        : call,
                    "args"        : args}
        settings.update(kwargs)
        super(NeonButton, self).__init__(rect, *groups, **settings)


class GameButton(Button):
    ss_size = (160, 120)
    width = ss_size[0] + 12
    height = ss_size[1] + 12
    font = prepare.FONTS["Fixedsys500c"]

    def __init__(self, pos, game, thumb, call, *groups, **kwargs):
        path = os.path.join(".", "data", "states", game)
        idle, highlight = self.make_images(game, thumb)
        rect = idle.get_rect(topleft=pos)
        settings = {"hover_image" : highlight,
                    "idle_image"  : idle,
                    "call"        : call,
                    "args"        : game}
        settings.update(kwargs)
        super(GameButton, self).__init__(rect, *groups, **settings)

    def make_images(self, game, icon):
        icon = pg.transform.scale(icon, self.ss_size).convert_alpha()
        icon_rect = icon.get_rect()
        label_text = game.replace("_", " ").capitalize()
        label = Label(self.font, 28, label_text, prepare.LOW_LIGHT_GREEN,
                      {"center": (0, 0)})
        rect = pg.Rect(0, 0, self.width, self.height+label.rect.h)
        icon_rect.midtop = (rect.centerx, 10)
        label.rect.midtop = icon_rect.midbottom
        frame = label.image.get_rect()
        frame.w = icon_rect.w
        frame.midtop=icon_rect.midbottom
        image = pg.Surface(rect.size).convert_alpha()
        image.fill((0,0,0,0))
        image.blit(icon, icon_rect)
        image.fill(pg.Color("gray10"), frame)
        highlight = image.copy()
        pg.draw.rect(image, prepare.LOW_LIGHT_GREEN, icon_rect, 4)
        pg.draw.rect(image, prepare.LOW_LIGHT_GREEN, frame, 4)
        highlight.blit(prepare.GFX["game_highlight"], (0, 3))
        for surface in (image, highlight):
            label.draw(surface)
        return (image, highlight)
