"""
This module contains some useful classes for text rendering and GUI elements,
such as buttons and text input boxes.

TODO: needs some cleaning up, consolidation, and documentation.
"""

import os
import string

import pygame as pg
from data.core import prepare, tools


LOADED_FONTS = {}

BUTTON_DEFAULTS = {"call"               : None,
                   "args"               : None,
                   "call_on_up"         : True,
                   "font"               : None,
                   "font_size"          : 36,
                   "text"               : None,
                   "hover_text"         : None,
                   "disable_text"       : None,
                   "text_color"         : pg.Color("white"),
                   "hover_text_color"   : None,
                   "disable_text_color" : None,
                   "fill_color"         : None,
                   "hover_fill_color"   : None,
                   "disable_fill_color" : None,
                   "idle_image"         : None,
                   "hover_image"        : None,
                   "disable_image"      : None,
                   "hover_sound"        : None,
                   "click_sound"        : None,
                   "visible"            : True,
                   "active"             : True,
                   "bindings"           : ()}


# Helper function for MultiLineLabel class.
# Seems this can be removed in favor of the standard library textwrap module.
def wrap_text(text, char_limit, separator=" "):
    """Splits a string into a list of strings no longer than char_limit."""
    words = text.split(separator)
    lines = []
    current_line = []
    current_length = 0
    for word in words:
        if len(word) + current_length <= char_limit:
            current_length += len(word) + len(separator)
            current_line.append(word)
        else:
            lines.append(separator.join(current_line))
            current_line = [word]
            current_length = len(word) + len(separator)
    if current_line:
        lines.append(separator.join(current_line))
    return lines


def _parse_color(color):
    if color is not None:
        try:
            return pg.Color(color)
        except ValueError:
            return pg.Color(*color)
    return color


# Should probably inherit from sprites.
class Label(object):
    """
    Parent class all labels inherit from. Color arguments can use color names
    or an RGB tuple. rect_attr should be a dict with keys of pygame.Rect
    attribute names (strings) and the relevant position(s) as values.

    Creates a surface with text blitted to it (self.image) and an associated
    rectangle (self.rect). Label will have a transparent bg if
    bg is not passed to __init__.
    """
    def __init__(self, path, size, text, color, rect_attr, bg=None):
        self.path, self.size = path, size
        if (path, size) not in LOADED_FONTS:
            LOADED_FONTS[(path, size)] = pg.font.Font(path, size)
        self.font = LOADED_FONTS[(path, size)]
        self.bg = _parse_color(bg)
        self.color = _parse_color(color)
        self.rect_attr = rect_attr
        self.set_text(text)

    def set_text(self, text):
        """
        Set the text to display.
        """
        self.text = text
        self.update_text()

    def update_text(self):
        """
        Update the surface using the current properties and text.
        """
        if self.bg:
            render_args = (self.text, True, self.color, self.bg)
        else:
            render_args = (self.text, True, self.color)
        self.image = self.font.render(*render_args)
        self.rect = self.image.get_rect(**self.rect_attr)

    def draw(self, surface):
        """
        Blit self.image to target surface.
        """
        surface.blit(self.image, self.rect)


# Should probably be depracated with Labels turned into sprites so that
# They can use standard sprite groups.
class GroupLabel(Label):
    """
    Creates a Label object which is then appended to group.
    """
    def __init__(self, group, path, size, text, color, rect_attr, bg=None):
        super(GroupLabel,self).__init__(path, size, text, color, rect_attr, bg)
        group.append(self)


class MultiLineLabel(object):
    """
    Creates a single surface with multiple labels blitted to it.
    """
    def __init__(self, path, size, text, color, rect_attr,
                 bg=None, char_limit=42, align="left", vert_space=0):
        attr = {"center": (0, 0)}
        lines = wrap_text(text, char_limit)
        labels = [Label(path, size, line, color, attr, bg) for line in lines]
        width = max([label.rect.width for label in labels])
        spacer = vert_space*(len(lines)-1)
        height = sum([label.rect.height for label in labels])+spacer
        self.image = pg.Surface((width, height)).convert()
        self.image.set_colorkey(pg.Color("black"))
        self.image.fill(pg.Color("black"))
        self.rect = self.image.get_rect(**rect_attr)
        aligns = {"left"  : {"left": 0},
                  "center": {"centerx": self.rect.width//2},
                  "right" : {"right": self.rect.width}}
        y = 0
        for label in labels:
            label.rect = label.image.get_rect(**aligns[align])
            label.rect.top = y
            label.draw(self.image)
            y += label.rect.height+vert_space

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class ButtonGroup(pg.sprite.Group):
    """
    A sprite group to hold multiple buttons.
    """
    def get_event(self, event, *args, **kwargs):
        """
        Only passes events along to Buttons that are both active and visible.
        """
        check = (s for s in self.sprites() if s.active and s.visible)
        for s in check:
            s.get_event(event, *args, **kwargs)


class Button(pg.sprite.Sprite, tools._KwargMixin):
    _invisible = pg.Surface((1,1)).convert_alpha()
    _invisible.fill((0,0,0,0))

    def __init__(self, rect_style, *groups, **kwargs):
        super(Button, self).__init__(*groups)
        self.process_kwargs("Button", BUTTON_DEFAULTS, kwargs)
        self.rect = pg.Rect(rect_style)
        rendered = self.render_text()
        self.idle_image = self.make_image(self.fill_color, self.idle_image,
                                          rendered["text"])
        self.hover_image = self.make_image(self.hover_fill_color,
                                           self.hover_image, rendered["hover"])
        self.disable_image = self.make_image(self.disable_fill_color,
                                             self.disable_image,
                                             rendered["disable"])
        self.image = self.idle_image
        self.clicked = False
        self.hover = False

    def render_text(self):
        font, size = self.font, self.font_size
        if (font, size) not in LOADED_FONTS:
            LOADED_FONTS[font, size] = pg.font.Font(font, size)
        self.font = LOADED_FONTS[font, size]
        text = self.text and self.font.render(self.text, 1, self.text_color)
        hover = self.hover_text and self.font.render(self.hover_text, 1,
                                                     self.hover_text_color)
        disable = self.disable_text and self.font.render(self.disable_text, 1,
                                                       self.disable_text_color)
        return {"text" : text, "hover" : hover, "disable": disable}

    def make_image(self, fill, image, text):
        if not any((fill, image, text)):
            return None
        final_image = pg.Surface(self.rect.size).convert_alpha()
        final_image.fill((0,0,0,0))
        rect = final_image.get_rect()
        fill and final_image.fill(fill, rect)
        image and final_image.blit(image, rect)
        text and final_image.blit(text, text.get_rect(center=rect.center))
        return final_image

    def get_event(self, event):
        if self.active and self.visible:
            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                self.on_up_event(event)
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                self.on_down_event(event)
            elif event.type == pg.KEYDOWN and event.key in self.bindings:
                self.on_down_event(event, True)
            elif event.type == pg.KEYUP and event.key in self.bindings:
                self.on_up_event(event, True)

    def on_up_event(self, event, onkey=False):
        if self.clicked and self.call_on_up:
            self.click_sound and self.click_sound.play()
            self.call and self.call(self.args or self.text)
        self.clicked = False

    def on_down_event(self, event, onkey=False):
        if self.hover or onkey:
            self.clicked = True
            if not self.call_on_up:
                self.click_sound and self.click_sound.play()
                self.call and self.call(self.args or self.text)

    def update(self, prescaled_mouse_pos):
        hover = self.rect.collidepoint(prescaled_mouse_pos)
        pressed = pg.key.get_pressed()
        if any(pressed[key] for key in self.bindings):
            hover = True
        if not self.visible:
            self.image = Button._invisible
        elif self.active:
            self.image = (hover and self.hover_image) or self.idle_image
            if not self.hover and hover:
                self.hover_sound and self.hover_sound.play()
            self.hover = hover
        else:
            self.image = self.disable_image or self.idle_image

    def draw(self, surface):
        surface.blit(self.image, self.rect)


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


class FlashingText(pg.sprite.Sprite):
    def __init__(self, center, text, font, color, size, delay, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.raw_image = render_font(font, size, text, color)
        self.null_image = pg.Surface((1,1)).convert_alpha()
        self.null_image.fill((0,0,0,0))
        self.image = self.raw_image
        self.rect = self.image.get_rect(center=center)
        self.blink = False
        self.timer = tools.Timer(delay)

    def update(self, now, *args):
        if self.timer.check_tick(now):
            self.blink = not self.blink
        self.image = self.raw_image if self.blink else self.null_image


def render_font(font, size, msg, color=pg.Color("white")):
    """
    Takes the name of a loaded font, the size, and the color and returns
    a rendered surface of the msg given.
    """
    selected_font = pg.font.Font(prepare.FONTS[font], size)
    return selected_font.render(msg, 1, color)
    
        
class TextBox(object):
    def __init__(self, rect, **kwargs):
        self.rect = pg.Rect(rect)
        self.buffer = []
        self.final = None
        self.rendered = None
        self.render_rect = None
        self.render_area = None
        self.blink = True
        self.blink_timer = 0.0
        self.accepted = string.ascii_letters+string.digits+string.punctuation+" "
        self.process_kwargs(kwargs)

    def process_kwargs(self,kwargs):
        defaults = {"id" : None,
                    "command" : None,
                    "active" : True,
                    "color" : pg.Color("white"),
                    "font_color" : pg.Color("black"),
                    "outline_color" : pg.Color("black"),
                    "outline_width" : 2,
                    "active_color" : pg.Color("blue"),
                    "font" : pg.font.Font(None, self.rect.height+4),
                    "clear_on_enter" : False,
                    "inactive_on_enter" : True}
        for kwarg in kwargs:
            if kwarg in defaults:
                defaults[kwarg] = kwargs[kwarg]
            else:
                raise KeyError("InputBox accepts no keyword {}.".format(kwarg))
        self.__dict__.update(defaults)

    def get_event(self,event, mouse_pos):
        if event.type == pg.KEYDOWN and self.active:
            if event.key in (pg.K_RETURN,pg.K_KP_ENTER):
                self.execute()
            elif event.key == pg.K_BACKSPACE:
                if self.buffer:
                    self.buffer.pop()
            elif event.unicode in self.accepted:
                self.buffer.append(event.unicode)
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.active = self.rect.collidepoint(mouse_pos)

    def execute(self):
        if self.command:
            self.command(self.id,self.final)
        self.active = not self.inactive_on_enter
        if self.clear_on_enter:
            self.buffer = []

    def update(self):
        new = "".join(self.buffer)
        if new != self.final:
            self.final = new
            self.rendered = self.font.render(self.final, True, self.font_color)
            self.render_rect = self.rendered.get_rect(x=self.rect.x+2,
                                                      centery=self.rect.centery)
            if self.render_rect.width > self.rect.width-6:
                offset = self.render_rect.width-(self.rect.width-6)
                self.render_area = pg.Rect(offset,0,self.rect.width-6,
                                           self.render_rect.height)
            else:
                self.render_area = self.rendered.get_rect(topleft=(0,0))
        if pg.time.get_ticks()-self.blink_timer > 200:
            self.blink = not self.blink
            self.blink_timer = pg.time.get_ticks()

    def draw(self,surface):
        outline_color = self.active_color if self.active else self.outline_color
        outline = self.rect.inflate(self.outline_width*2,self.outline_width*2)
        surface.fill(outline_color,outline)
        surface.fill(self.color,self.rect)
        if self.rendered:
            surface.blit(self.rendered,self.render_rect,self.render_area)
        if self.blink and self.active:
            curse = self.render_area.copy()
            curse.topleft = self.render_rect.topleft
            surface.fill(self.font_color,(curse.right+1,curse.y,2,curse.h))
