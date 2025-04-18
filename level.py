import pygame
from CONSTANTS import IMAGE_DIR, TILE_SIZE, TILE_SCALE
from display import Display
import os
import copy


class Level:
    def __init__(self, display: Display) -> None:
        self.window_info: tuple[int, int] = pygame.display.get_window_size()
        self.winw: int = self.window_info[0]
        self.winh: int = self.window_info[1]
        self.background: pygame.Surface = pygame.Surface((self.winw, self.winh))

        # TODO Use array to generate rooms and hold data in dicts
        # TODO support multi tileset generation
        dungeon_tiles_names: list[str] = [
            "floor",
            "wall_vertical",
            "wall_horizontal",
            "corner_bottom",
        ]
        dungeon_tiles: dict[str, dict[str, pygame.Surface]] = {}
        tile_path: str = os.path.join(IMAGE_DIR, "Dungeon_Tiles")

        for tileset in os.listdir(tile_path):
            if os.path.isdir(os.path.join(tile_path, tileset)):
                dungeon_tiles[tileset] = {}
                for name in dungeon_tiles_names:
                    dungeon_tiles[tileset][name] = pygame.image.load(
                        os.path.join(tile_path, tileset, name + ".png")
                    ).convert()
                    dungeon_tiles[tileset][name] = pygame.transform.scale(
                        dungeon_tiles[tileset][name], TILE_SCALE
                    )

        ## DELETE THIS, IT IS TEMPORARY
        print(dungeon_tiles)
        for tile_h in range(self.winh // TILE_SIZE):
            for tile_w in range(self.winw // TILE_SIZE):
                pass
                # self.background.blit(tile, rect)
        # self.backgroundbox: pygame.Rect = display.screen.get_rect()

    # background: pygame.Surface = pygame.image.load(
    #     os.path.join(IMAGE_DIR, "background.png")
    # ).convert()

    def generate_room(self) -> list[list[str]]:
        # Let's create a semantic dictionary

        tile_dict: dict[str, list[list[str]]] = {
            "1": [["wvl", "wh"], ["wvl", "f"]],
            "2": [["wh", "wh"], ["f", "f"]],
            "3": [["wh", "wvr"], ["f", "wvr"]],
            "4": [["wvl", "f"], ["wvl", "f"]],
            "5": [["f", "wvr"], ["f", "wvr"]],
            "6": [["f", "f"], ["f", "f"]],
            "7": [["wvl", "f"], ["wvl", "wh"]],
            "8": [["f", "f"], ["wh", "wh"]],
            "9": [["f", "wvr"], ["wh", "wvr"]],
            "10": [["wvl", "wvr"], ["wh", "wh"]],
        }
        tile_connections: dict[str, list[tuple[int, str]]] = {
            "1": [(2, "E"), (4, "S")],
            "2": [(1, "W"), (3, "E"), (6, "S")],
            "3": [(2, "W"), (5, "S")],
            "4": [(1, "N"), (6, "E"), (7, "S")],
            "5": [(6, "W"), (3, "N"), (9, "S")],
            "6": [(2, "N"), (4, "W"), (5, "E"), (8, "S")],
            "7": [(4, "N"), (8, "E")],
            "8": [(6, "N"), (7, "W"), (9, "E")],
            "9": [(8, "W"), (5, "N")],
            "10": [(2, "W"), (2, "E"), (6, "S")],
        }
        return [[""]]

        pass
