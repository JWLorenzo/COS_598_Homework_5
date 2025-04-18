import pygame
import os
from typing import Any
from CONSTANTS import IMAGE_DIR, ALPHA, ANIMATION_CYCLE, PLAYER_SIZE


class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.images: list[pygame.Surface] = []
        self.movex: int = 0
        self.movey: int = 0
        self.frame: int = 0
        self.steps: int = 10
        # TODO loop this to do multiple images for a walking texture
        ###
        img: pygame.Surface = (
            pygame.image.load(os.path.join(IMAGE_DIR, "player.png"))
            .convert()
            .convert_alpha()
        )
        img = pygame.transform.scale(img, PLAYER_SIZE)
        img.set_colorkey(ALPHA)
        self.images.append(img)
        self.image: pygame.Surface = self.images[0]
        self.rect: pygame.Rect = self.image.get_rect()
        ###

    def control(self, x: int, y: int) -> None:
        self.movex += x
        self.movey += y

    def update(self) -> None:
        self.rect.x = self.rect.x + self.movex
        self.rect.y = self.rect.y + self.movey

        if len(self.images) > 1:
            if self.movex < 0:
                self.frame += 1
                if self.frame > 3 * ANIMATION_CYCLE:
                    self.frame = 0
                self.image = self.images[self.frame // ANIMATION_CYCLE]

            if self.movex > 0:
                self.frame += 1
                if self.frame > 3 * ANIMATION_CYCLE:
                    self.frame = 0
                self.image = self.images[self.frame // ANIMATION_CYCLE]
