"""
Welcome to the Python Arcade Collab project, please visit us at
https://www.reddit.com/r/PythonArcadeCollab/

All code is CC-0 unless otherwise explicitly stated.
No warranty expressed or implied.

This file serves as the entry point of the entire program.
"""

import sys
import pygame as pg

# import pygame._view # Sometimes required when building .exe files.

sys.dont_write_bytecode = True
from data.main import main


if __name__ == '__main__':
    main()
    pg.quit()
    sys.exit()
