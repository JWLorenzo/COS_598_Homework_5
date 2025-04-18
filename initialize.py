from display import Display
import pygame
from pygame.locals import *
import CONSTANTS


def initialize_game() -> Display:
    pygame.init()
    info = pygame.display.Info()
    screen = pygame.display.set_mode((info.current_w, info.current_h))
    clock = pygame.time.Clock()
    display = Display(screen, clock)
    return display
