from Utility.CONSTANTS import *


class tileArray:
    def __init__(self, width: int, height: int) -> None:
        self.map_width: int = width
        self.map_height: int = height
        self.tile_array: list[list[str]] = [
            [" " for column in range(self.map_width)] for row in range(self.map_height)
        ]

    def carve_Area(
        self, left: int, right: int, top: int, bottom: int, wall: str, floor: str
    ) -> None:

        column: int = left
        while column <= right:
            row: int = bottom
            while row <= top:
                edge_row: bool = row == bottom or row == top
                edge_column: bool = column == right or column == left
                if edge_row or edge_column:
                    self.tile_array[row][column] = wall
                else:
                    self.tile_array[row][column] = floor
                row += 1
            column += 1

    def carve_Corridor(
        self,
        left: int,
        right: int,
        top: int,
        bottom: int,
        wall: str,
        floor: str,
        direction: str,
    ) -> None:

        column: int = left
        while column <= right:
            row: int = bottom
            while row <= top:
                edge_row: bool = row == bottom or row == top
                edge_column: bool = column == right or column == left

                if direction == "v":
                    if edge_row:
                        self.tile_array[row][column] = wall
                    else:
                        self.tile_array[row][column] = floor
                elif direction == "h":
                    if edge_column:
                        self.tile_array[row][column] = wall
                    else:
                        self.tile_array[row][column] = floor
                else:
                    self.tile_array[row][column] = floor

                row += 1
            column += 1
