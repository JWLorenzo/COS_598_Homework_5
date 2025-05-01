from Utility.CONSTANTS import *


class tileArray:
    def __init__(self, width: int, height: int) -> None:
        self.map_width: int = width
        self.map_height: int = height
        self.tile_array: list[list[str]] = [
            [" " for column in range(self.map_width)] for row in range(self.map_height)
        ]

    def carve_Area(
        self, x_min: int, x_max: int, y_min: int, y_max: int, wall: str, floor: str
    ) -> None:

        column: int = x_min
        while column < x_max:
            row: int = y_min
            while row < y_max:
                edge_row: bool = row == y_min or row == y_max - 1
                edge_column: bool = column == x_max - 1 or column == x_min
                if edge_row or edge_column:
                    if self.tile_array[row][column] != floor:
                        self.tile_array[row][column] = wall
                else:
                    self.tile_array[row][column] = floor
                row += 1
            column += 1

    def create_Corridors(self,path_List:list[tuple[tuple[int, int], tuple[int, int],str]])->None:
        for i in path_List:
            print("New Path",i)
            for x in range(min(i[0][0],i[1][0]),max(i[0][0],i[1][0])+1):
                for y in range(min(i[0][1], i[1][1]), max(i[0][1], i[1][1]) + 1):
                    if i[2] == "h":
                        self.tile_array[y][x] = "|"
                        self.tile_array[y][x-1] = "#"
                        self.tile_array[y][x+1] = "#"
                    else:
                        self.tile_array[y][x] = "-"
                        self.tile_array[y-1][x] = "#"
                        self.tile_array[y+1][x] = "#"
                    print((x,y))