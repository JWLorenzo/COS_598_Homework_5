from Utility.CONSTANTS import *


class tileArray:
    def __init__(self, width: int, height: int) -> None:
        self.map_width: int = width
        self.map_height: int = height
        self.floor: str = " "
        self.wall: str = "#"
        self.door: str = "@"
        self.empty: str = "+"
        self.corridor_v: str = "|"
        self.corridor_h: str = "-"
        self.tile_array: list[list[str]] = [
            [self.empty for column in range(self.map_width)]
            for row in range(self.map_height)
        ]

    def carve_Area(self, x_min: int, x_max: int, y_min: int, y_max: int) -> None:
        w_range: list[int] = list(range(self.map_width))
        h_range: list[int] = list(range(self.map_height))
        for row in range(y_min, y_max):
            for column in range(x_min, x_max):
                north, south, east, west, northeast, northwest, southeast, southwest = (
                    self.get_directions(row, column, w_range, h_range)
                )
                if column in [x_min, x_max - 1] or row in [y_min, y_max - 1]:
                    if self.tile_array[row][column] in [
                        self.corridor_v,
                        self.corridor_h,
                    ]:
                        self.tile_array[row][column] = self.floor
                    else:
                        self.tile_array[row][column] = self.wall
                else:
                    self.tile_array[row][column] = self.floor

    def create_Corridors(
        self, path_List: list[tuple[tuple[int, int], tuple[int, int]]]
    ) -> None:
        for path in path_List:
            if path[0][1] == path[1][1]:
                for i in range(path[1][0] - path[0][0]):
                    # print("hori", i)
                    # print(f"x: {path[0][0] + i}, y: {path[1][1]}")
                    self.tile_array[path[1][1]][path[0][0] + i] = self.corridor_h
            else:
                for i in range(path[1][1] - path[0][1]):
                    # print("vert", i)
                    # print(f"x: {path[0][0]}, y: {path[0][1] + i}")
                    self.tile_array[path[0][1] + i][path[0][0]] = self.corridor_v

    def get_directions(
        self, row: int, column: int, w_range: list[int], h_range: list[int]
    ) -> tuple[str, str, str, str, str, str, str, str]:
        north: str = self.tile_array[row - 1][column] if (row - 1) in h_range else ""
        south: str = self.tile_array[row + 1][column] if (row + 1) in h_range else ""
        east: str = self.tile_array[row][column + 1] if (column + 1) in w_range else ""
        west: str = self.tile_array[row][column - 1] if (column - 1) in w_range else ""
        northeast: str = (
            self.tile_array[row - 1][column + 1]
            if (row - 1) in h_range and (column + 1) in w_range
            else ""
        )
        northwest: str = (
            self.tile_array[row - 1][column - 1]
            if (row - 1) in h_range and (column - 1) in w_range
            else ""
        )

        southeast: str = (
            self.tile_array[row + 1][column + 1]
            if (row + 1) in h_range and (column + 1) in w_range
            else ""
        )

        southwest: str = (
            self.tile_array[row + 1][column - 1]
            if (row + 1) in h_range and (column - 1) in w_range
            else ""
        )
        return north, south, east, west, northeast, northwest, southeast, southwest

    def dungeon_cleanup(self) -> None:
        w_range: list[int] = list(range(self.map_width))
        h_range: list[int] = list(range(self.map_height))
        for row in range(self.map_height):
            for column in range(self.map_width):
                north, south, east, west, northeast, northwest, southeast, southwest = (
                    self.get_directions(row, column, w_range, h_range)
                )

                if self.tile_array[row][column] == self.empty:
                    # Fill in empty spots with normal walls
                    if any(
                        symbol in [self.floor, self.corridor_h, self.corridor_v]
                        for symbol in [
                            north,
                            south,
                            east,
                            west,
                            northeast,
                            northwest,
                            southeast,
                            southwest,
                        ]
                    ):
                        self.tile_array[row][column] = self.wall

        # for row in range(self.map_height):
        #     for column in range(self.map_width):
        #         north, south, east, west, northeast, northwest, southeast, southwest = (
        #             self.get_directions(row, column, w_range, h_range)
        #         )

        #         if self.tile_array[row][column] in [self.corridor_h, self.corridor_v]:
        #             # Fill in ends of corridors with doors
        #             # print(
        #             #     f"checking {north} {south} {east} {west} {northeast} {northwest} {southeast} {southwest}"
        #             # )
        #             if (
        #                 (self.wall == north and north == south)
        #                 or (self.wall == east and east == west)
        #             ) and (self.floor in [northeast, southeast, northwest, southwest]):
        #                 self.tile_array[row][column] = self.door

        # for row in range(self.map_height):
        #     for column in range(self.map_width):
        #         if self.tile_array[row][column] in [self.corridor_h, self.corridor_v]:
        #             self.tile_array[row][column] = self.floor

    def draw_corridor(self, min_x: int, max_x: int, min_y: int, max_y: int) -> None:
        for row in range(min_y, max_y):
            for column in range(min_x, max_x):
                self.tile_array[row][column] = "%"
