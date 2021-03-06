import os
import sys

import pygame as pg

from app import App

CAPTION = "Moving Platforms"
SCREEN_SIZE = (700, 500)

if __name__ == "__main__":
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.init()
    pg.display.set_caption(CAPTION)
    pg.display.set_mode(SCREEN_SIZE)
    run_it = App()
    run_it.main_loop()
    pg.quit()
    sys.exit()
