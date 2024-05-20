import os
import sys

import pygame

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 997
TITLE = "LONGEST DRAGON"
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(TITLE)


def image(filename):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, 'images', filename)
