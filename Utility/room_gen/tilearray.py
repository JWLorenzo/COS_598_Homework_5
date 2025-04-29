from Utility.CONSTANTS import *


class tileArray:
    def __init__(self, width: int, height: int) -> None:
        self.map_width: int = width
        self.map_height: int = height
        self.tile_array: list[list[str]] = [
            [" " for column in range(self.map_width)] for row in range(self.map_height)
        ]

    def carve_Area(
        self, x_min: int, y_min: int, x_max: int, y_max: int, wall: str, floor: str
    ) -> None:
        for row in range(y_min, y_max):
            for column in range(x_min, x_max):
                if (row == y_max - 1 or row == y_min) or (
                    column == x_max - 1 or column == x_min
                ):
                    self.tile_array[row][column] = wall
                else:
                    self.tile_array[row][column] = floor
