import sys
import pygame as pg

# import pygame._view # Sometimes required when building .exe files.

sys.dont_write_bytecode = True
from data.main import main


if __name__ == '__main__':
    main()
    pg.quit()
    sys.exit()
