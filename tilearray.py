from CONSTANTS import *


class tileArray:
    def __init__(self, width: int, height: int) -> None:
        self.map_width: int = width
        self.map_height: int = height
        self.tile_size: int = TILE_SIZE
        self.tile_array: list[list[str]] = [
            [" " for column in range(self.map_width // TILE_SIZE)]
            for row in range(self.map_height // TILE_SIZE)
        ]

    def carve_Area(self, x: int, y: int, w: int, h: int, wall: str, floor: str) -> None:
        for row in range(y // TILE_SIZE, (y + h) // TILE_SIZE):
            for column in range(x // TILE_SIZE, (x + w) // TILE_SIZE):
                if (row == ((y + h) // TILE_SIZE) - 1 or row == (y // TILE_SIZE)) or (
                    column == ((x + w) // TILE_SIZE) - 1 or column == (x // TILE_SIZE)
                ):
                    self.tile_array[row][column] = wall
                else:
                    self.tile_array[row][column] = floor
