from Utility.CONSTANTS import *
import random


class tileArray:
    def __init__(self, width: int, height: int) -> None:
        self.map_width: int = width
        self.map_height: int = height
        self.floor: str = " "
        self.wall: str = "#"
        self.door: str = "@"
        self.empty: str = " "
        self.corridor_v: str = "|"
        self.corridor_h: str = "-"
        self.wall_v: str = "]"
        self.wall_h: str = "_"
        self.dungeon_endcap: str = "!"
        self.tile_array: list[list[str]] = [
            [self.empty for column in range(self.map_width)]
            for row in range(self.map_height)
        ]

    def carve_Area(self, x_min: int, x_max: int, y_min: int, y_max: int) -> None:
        w_range: list[int] = list(range(self.map_width))
        h_range: list[int] = list(range(self.map_height))
        for row in range(y_min, y_max):
            for column in range(x_min, x_max):
                # north, south, east, west, northeast, northwest, southeast, southwest = (
                #     self.get_directions(row, column, w_range, h_range)
                # )
                if column in [x_min, x_max - 1] or row in [y_min, y_max - 1]:
                    # if self.tile_array[row][column] in [
                    #     self.corridor_v,
                    #     self.corridor_h,
                    # ]:
                    #     self.tile_array[row][column] = self.floor
                    # else:
                    if self.tile_array[row][column] not in [
                        self.corridor_v,
                        self.corridor_h,
                    ]:
                        self.tile_array[row][column] = self.wall
                else:
                    self.tile_array[row][column] = self.floor

    def create_Corridors(
        self, path_List: list[tuple[tuple[int, int], tuple[int, int]]]
    ) -> None:
        for path in path_List:
            if path[0][1] == path[1][1]:
                for i in range(path[1][0] - path[0][0]):
                    if self.tile_array[path[1][1]][path[0][0] + i] not in [
                        self.corridor_v,
                        self.corridor_h,
                    ]:
                        self.tile_array[path[1][1]][path[0][0] + i] = self.corridor_h
            else:
                for i in range(path[1][1] - path[0][1]):
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

    def vertical_corridors(
        self, iter_list: list[list[list[int]]], max: int, min: int
    ) -> None:
        rand_index: int = 0
        if len(iter_list) > 0:
            if len(iter_list) > 2:
                rand_index = random.randrange(0, len(iter_list))
            element: list[list[int]] = iter_list.pop(rand_index)
            rand_row: int = random.randint(min, max)
            # for element in iter_list:
            print(element)
            self.tile_array[rand_row][element[0][1]] = self.corridor_h
            self.tile_array[rand_row][element[1][1]] = self.corridor_h
            self.vertical_corridors(iter_list, max, min)
        return

    def horizontal_corridors(
        self, iter_list: list[list[list[int]]], max: int, min: int
    ) -> None:
        rand_index: int = 0
        if len(iter_list) > 0:
            if len(iter_list) > 2:
                rand_index = random.randrange(0, len(iter_list))
            element: list[list[int]] = iter_list.pop(rand_index)
            rand_column: int = random.randint(min, max)
            # for element in iter_list:
            print(element)
            self.tile_array[element[0][0]][rand_column] = self.corridor_v
            self.tile_array[element[1][0]][rand_column] = self.corridor_v
            self.horizontal_corridors(iter_list, max, min)
        return

    def iterative_doors(self) -> None:
        coord_list: list[list[list[int]]] = []
        x_list: list[int] = []
        y_list: list[int] = []
        for row in range(self.map_height):
            joined_row: str = "".join(self.tile_array[row])
            for column in range(self.map_width):
                valid_row: bool = (
                    (
                        [self.wall, self.empty]
                        == [self.tile_array[row][0], self.tile_array[row][1]]
                    )
                    and (
                        [self.empty, self.wall]
                        == [
                            self.tile_array[row][self.map_width - 2],
                            self.tile_array[row][self.map_width - 1],
                        ]
                    )
                    and (f"{self.wall}{self.wall}{self.wall}" not in joined_row)
                )

                if valid_row:
                    if column < self.map_width - 2:
                        if (
                            self.tile_array[row][column] == self.wall
                            and self.tile_array[row][column + 1] == self.wall
                        ):
                            if column not in x_list:
                                coord_list.append([[row, column], [row, column + 1]])
                                x_list.append(column)
                            y_list.append(row)
                            y_list = sorted(y_list)

            if not valid_row:
                if len(coord_list) > 0:
                    self.vertical_corridors(coord_list, y_list[-1], y_list[0])
                    x_list = []
                    y_list = []
                    coord_list = []

        x_list = []
        y_list = []
        coord_list = []
        for column in range(self.map_width):
            joined_column: str = "".join(
                [self.tile_array[x][column] for x in range(self.map_height)]
            )
            for row in range(self.map_height):
                valid_column: bool = (
                    (
                        [self.wall, self.empty]
                        == [self.tile_array[0][column], self.tile_array[1][column]]
                    )
                    and (
                        [self.empty, self.wall]
                        == [
                            self.tile_array[self.map_height - 2][column],
                            self.tile_array[self.map_height - 1][column],
                        ]
                    )
                    and (f"{self.wall}{self.wall}{self.wall}" not in joined_column)
                )
                if valid_column:
                    if row < self.map_height - 2:
                        if (
                            self.tile_array[row][column] == self.wall
                            and self.tile_array[row + 1][column] == self.wall
                        ):
                            if row not in y_list:
                                coord_list.append([[row, column], [row + 1, column]])
                                y_list.append(row)
                            x_list.append(column)
                            x_list = sorted(x_list)

            if not valid_column:
                if len(coord_list) > 0:
                    self.horizontal_corridors(coord_list, x_list[-1], x_list[0])
                    x_list = []
                    y_list = []
                    coord_list = []
