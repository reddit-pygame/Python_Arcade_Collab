import pygame as pg

from . import constants


def draw_cell(surface, cell, color, offset=(0,0)):
    """
    Draw a single cell at the desired size with an offset.
    """
    pos = [cell[i]*constants.CELL.size[i] for i in (0,1)]
    rect = pg.Rect(pos, constants.CELL.size)
    rect.move_ip(*offset)
    surface.fill(color, rect)


def make_levels():
    """
    Make a few levels.  Hardcoded and ugly.  Don't do this.
    """
    w, h = constants.BOARD_SIZE
    r = range
    levels = [
        ({(w//2,i) for i in r(h//2-3)}|{(w//2,i) for i in r(h//2+3,h)}),
        ({(w//4,i) for i in r(3*h//5)}|{(3*w//4,i) for i in r(2*h//5,h)}),
        ({(w//2,i) for i in r(5,h-5)}|{(i,h//2) for i in r(3,w//2-3)}|
            {(i+w//2+3, h//2) for i in r(3,w//2-3)})]
    return levels
