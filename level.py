import pygame
from CONSTANTS import IMAGE_DIR, TILE_SCALE
from display import Display
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

        # # Base Case

        # if w <= 2 * ROOM_WIDTH or h <= 2 * ROOM_HEIGHT:
        #     print(f"Drawing room at ({x}, {y}) with size ({w}, {h})")
        #     pygame.draw.rect(self.background, "blue", (x, y, w, h))
        #     pygame.draw.rect(self.background, "white", (x, y, w, h), 2)

        #     pygame.display.flip()
        # elif (w >= (2*ROOM_WIDTH)) or (h >= (2*ROOM_HEIGHT)):
        #     # Recursive Step
        #     direction: str = random.choice(["horizontal", "vertical"])

        #     tile_width = random.randint(1, (w // TILE_SIZE) - 1) * TILE_SIZE
        #     tile_height = random.randint(1, (h // TILE_SIZE) - 1) * TILE_SIZE

        #     # Split vertically
        #     if direction == "vertical":
        #         pass
        #         self.binary_space_partition(x, y, tile_width, h)
        #         self.binary_space_partition(x + tile_width, y, w - tile_width, h)
        #     # Split horizontally
        #     elif direction == "horizontal":
        #         pass
        #         self.binary_space_partition(x, y, w, tile_height)
        #         self.binary_space_partition(x, y + tile_height, w, h - tile_height)

    def generate_room(self) -> pygame.Surface:

        return pygame.Surface(
            (0, 0)
        )  # Placeholder return value until the function is implemented

        pass
