import pygame
import pygame.freetype


class Display:
    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock) -> None:
        self.screen: pygame.Surface = screen
        self.clock: pygame.time.Clock = clock
        self.run: bool = True
        self.delta: int = 0
        self.font: pygame.freetype.Font = None
