import pygame
from Utility.CONSTANTS import IMAGE_DIR, TILE_SCALE
from Utility.display import Display
import os


class Level:
    def __init__(self, display: Display) -> None:
        self.window_info: tuple[int, int] = pygame.display.get_window_size()
        self.winw: int = self.window_info[0]
        self.winh: int = self.window_info[1]
        self.background: pygame.Surface = display.screen

        # TODO Use array to generate rooms and hold data in dicts
        # TODO support multi tileset generation

        self.dungeon_tiles: dict[str, pygame.Surface] = {}
        tile_path: str = os.path.join(IMAGE_DIR, "Dungeon_Tiles")

        for tile in os.listdir(tile_path):
            if tile.endswith(".png"):
                filename = os.path.splitext(tile)[0]
                self.dungeon_tiles[filename] = pygame.image.load(
                    os.path.join(tile_path, tile)
                ).convert()
                self.dungeon_tiles[filename] = pygame.transform.scale(
                    self.dungeon_tiles[filename], TILE_SCALE
                )
                print(tile)

    def generate_room(self) -> pygame.Surface:

        return pygame.Surface(
            (0, 0)
        )  # Placeholder return value until the function is implemented

        pass
