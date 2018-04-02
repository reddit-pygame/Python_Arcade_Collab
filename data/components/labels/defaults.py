import pygame as pg


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


TEXTBOX_DEFAULTS = {"id"                : None,
                    "command"           : None,
                    "active"            : True,
                    "color"             : pg.Color("white"),
                    "font_color"        : pg.Color("black"),
                    "outline_color"     : pg.Color("black"),
                    "outline_width"     : 2,
                    "active_color"      : pg.Color("blue"),
                    "font"              : None,
                    "clear_on_enter"    : False,
                    "inactive_on_enter" : True}
