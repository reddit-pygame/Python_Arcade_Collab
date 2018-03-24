import pygame as pg

from data.core import prepare


##SCREEN_SIZE = (544, 544)
##PLAY_RECT = pg.Rect(16, 16, 512, 512)

CELL = pg.Rect(0, 0, 29, 29)
SCREEN_SIZE = prepare.RENDER_SIZE
PLAY_RECT = pg.Rect(CELL.w, CELL.h,
                    SCREEN_SIZE[0] - 2*CELL.w, SCREEN_SIZE[1] - 2*CELL.h)



##CELL = pg.Rect(0, 0, 16, 16)
BOARD_SIZE = (PLAY_RECT.w//CELL.w, PLAY_RECT.h//CELL.h)
GROWTH_PER_APPLE = 3


COLORS = {"background" : (30, 40, 50), "walls" : pg.Color("lightslategrey"),
          "snake" : pg.Color("limegreen"), "head" : pg.Color("darkgreen"),
          "apple" : pg.Color("tomato")}

DIRECT_DICT = {"left" : (-1, 0), "right" : ( 1, 0),
               "up" : ( 0,-1), "down" : ( 0, 1)}

OPPOSITES = {"left" : "right", "right" : "left",
             "up" : "down", "down" : "up"}

KEY_MAPPING = {(pg.K_LEFT, pg.K_a) : "left", (pg.K_RIGHT, pg.K_d) : "right",
               (pg.K_UP, pg.K_w) : "up", (pg.K_DOWN, pg.K_s) : "down"}
