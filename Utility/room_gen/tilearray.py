from Utility.CONSTANTS import *
import random
import heapq


class tileArray:
    def __init__(self, width: int, height: int) -> None:

        # Basic
        self.empty: str = " "
        self.map_width: int = width
        self.map_height: int = height
        self.w_range: list[int] = list(range(self.map_width))
        self.h_range: list[int] = list(range(self.map_height))
        self.tile_array: list[list[str]] = [
            [self.empty for _ in range(self.map_width)] for _ in range(self.map_height)
        ]
        # Wall Tiles
        self.wall_North: str = "N"
        self.wall_South: str = "S"
        self.wall_East: str = "E"
        self.wall_West: str = "W"
        self.cornertr: str = "]"
        self.cornertl: str = "["
        self.cornerbr: str = "}"
        self.cornerbl: str = "{"
        self.wall_hL: str = "L"
        self.wall_hR: str = "R"
        self.wall_CornerR: str = ">"
        self.wall_CornerL: str = "<"

        # Wall Arrays

        self.corner_coord: list[tuple[int, int]] = []  # row, column
        self.wall_coords: list[tuple[int, int]] = []  # row, column

        # Floor Tiles

        self.floor: str = "."

        # Corridor Pre Door

        self.corridor_v: str = "|"
        self.corridor_h: str = "-"
        self.corridor_cord: list[tuple[tuple[int, int], tuple[int, int]]] = (
            []
        )  # (corridor 1: (row, column) , corridor 2: (row, column))

        # Door
        self.door_coord: list[tuple[int, int]] = []
        self.door_percent: float = 0.125
        self.door: str = "P"
        self.locked: str = "!"

        # PATHFINDING

        self.costs: dict[str, int] = {
            self.floor: 1,
            self.corridor_v: 0,
            self.corridor_h: 0,
            self.wall_North: 10000,
            self.wall_South: 10000,
            self.wall_East: 10000,
            self.wall_West: 10000,
            self.cornertr: 10000,
            self.cornertr: 10000,
            self.cornertl: 10000,
            self.cornerbr: 10000,
            self.cornerbl: 10000,
            self.wall_hL: 10000,
            self.wall_hR: 10000,
            self.wall_CornerR: 10000,
            self.wall_CornerL: 10000,
        }
        self.directions: dict[str, tuple[int, int]] = {
            "N": (0, -1),
            "S": (0, 1),
            "E": (1, 0),
            "W": (-1, 0),
        }

    def get_tile(self, row: int, col: int) -> str:
        if row in self.h_range and col in self.w_range:
            return self.tile_array[row][col]
        return ""

    def get_directions(self, row: int, column: int) -> dict[str, str]:
        direction_dictionary: dict[str, str] = {
            "north": self.get_tile(row - 1, column),
            "south": self.get_tile(row + 1, column),
            "east": self.get_tile(row, column + 1),
            "west": self.get_tile(row, column - 1),
            "northeast": self.get_tile(row - 1, column + 1),
            "northwest": self.get_tile(row - 1, column - 1),
            "southeast": self.get_tile(row + 1, column + 1),
            "southwest": self.get_tile(row + 1, column - 1),
        }

        return direction_dictionary

    def carve_Area(self, x_min: int, x_max: int, y_min: int, y_max: int) -> None:

        for row in range(y_min, y_max):
            for column in range(x_min, x_max):

                is_top: bool = row == y_min
                is_bottom: bool = row == y_max - 1
                is_left: bool = column == x_min
                is_right: bool = column == x_max - 1
                is_right_end: bool = column == x_max - 2
                is_left_end: bool = column == x_min + 1

                if is_top and is_left:
                    tile = self.cornertl

                elif is_top and is_right:
                    tile = self.cornertr

                elif is_bottom and is_left:
                    tile = self.cornerbl

                elif is_bottom and is_right:
                    tile = self.cornerbr

                elif (is_top or is_bottom) and is_left_end:
                    tile = self.wall_hL

                elif (is_top or is_bottom) and is_right_end:
                    tile = self.wall_hR

                elif is_top:
                    tile = self.wall_North

                elif is_bottom:
                    tile = self.wall_South

                elif is_left:
                    tile = self.wall_West

                elif is_right:
                    tile = self.wall_East

                else:
                    tile = self.floor

                self.tile_array[row][column] = tile

                if tile != self.floor:
                    self.wall_coords.append((row, column))

                if tile in (self.cornertl, self.cornertr, self.cornerbl, self.cornerbr):
                    self.corner_coord.append((row, column))

    def carve_Corridors(
        self,
        iter_list: list[tuple[tuple[int, int], tuple[int, int]]],
        min_val: int,
        max_val: int,
        horizontal: bool = True,
    ):
        while iter_list:
            rand_index: int = (
                random.randrange(len(iter_list)) if len(iter_list) > 2 else 0
            )
            element = iter_list.pop(rand_index)
            rand_pos = random.randint(min_val, max_val)

            if horizontal:
                self.tile_array[rand_pos][element[0][1]] = self.corridor_h
                self.tile_array[rand_pos][element[1][1]] = self.corridor_h
                self.corridor_cord.append(
                    ((rand_pos, element[0][1]), (rand_pos, element[1][1]))
                )
            else:
                self.tile_array[element[0][0]][rand_pos] = self.corridor_v
                self.tile_array[element[1][0]][rand_pos] = self.corridor_v
                self.corridor_cord.append(
                    ((element[0][0], rand_pos), (element[1][0], rand_pos))
                )

    def iterative_doors(self) -> None:
        coord_list: list[tuple[tuple[int, int], tuple[int, int]]] = []
        x_list: list[int] = []
        y_list: list[int] = []
        for row in range(self.map_height):
            joined_row: str = "".join(self.tile_array[row])
            for column in range(self.map_width):
                valid_row: bool = all(
                    [
                        [self.wall_West, self.floor]
                        == [self.tile_array[row][0], self.tile_array[row][1]],
                        [self.floor, self.wall_East]
                        == [
                            self.tile_array[row][self.map_width - 2],
                            self.tile_array[row][self.map_width - 1],
                        ],
                        self.wall_North not in joined_row,
                        self.wall_South not in joined_row,
                    ]
                )
                if valid_row:
                    if column < self.map_width - 2:
                        if (
                            self.tile_array[row][column] == self.wall_East
                            and self.tile_array[row][column + 1] == self.wall_West
                        ):
                            if column not in x_list:
                                coord_list.append(((row, column), (row, column + 1)))
                                x_list.append(column)
                            y_list.append(row)
                            y_list = sorted(y_list)
                else:
                    if len(coord_list) > 0:
                        self.carve_Corridors(coord_list, y_list[0], y_list[-1])
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
                valid_column: bool = all(
                    [
                        (
                            [self.wall_North, self.floor]
                            == [self.tile_array[0][column], self.tile_array[1][column]]
                        ),
                        (
                            [self.floor, self.wall_South]
                            == [
                                self.tile_array[self.map_height - 2][column],
                                self.tile_array[self.map_height - 1][column],
                            ]
                        ),
                        self.wall_East not in joined_column,
                        self.wall_West not in joined_column,
                    ]
                )
                if valid_column:
                    if row < self.map_height - 2:
                        if (
                            self.tile_array[row][column] == self.wall_South
                            and self.tile_array[row + 1][column] == self.wall_North
                        ):
                            if row not in y_list:
                                coord_list.append(((row, column), (row + 1, column)))
                                y_list.append(row)
                            x_list.append(column)
                            x_list = sorted(x_list)

            if not valid_column:
                if len(coord_list) > 0:
                    self.carve_Corridors(
                        coord_list, x_list[0], x_list[-1], horizontal=False
                    )
                    x_list = []
                    y_list = []
                    coord_list = []

    def reconstruct_path(
        self,
        came_from: dict[tuple[int, int] | None, tuple[int, int] | None],
        start: tuple[int, int],
        end: tuple[int, int],
    ):

        current: tuple[int, int] | None = end
        path: list[tuple[int, int] | None] = []

        if end not in came_from:
            return []
        while current != start:
            prev: tuple[int, int] | None = came_from[current]
            path.append(prev)
            current = prev
        return path

    def a_star_Heuristic(self, start: tuple[int, int], end: tuple[int, int]) -> int:
        return start[0] - end[0] + start[1] - end[1]

    def a_Star(self, start: tuple[int, int], end: tuple[int, int]):
        frontier: list = []
        heapq.heappush(frontier, (0, start))
        came_from: dict[tuple[int, int], tuple[int, int] | None] = {}
        cost_so_far: dict[tuple[int, int], int] = {}

        came_from[start] = None
        cost_so_far[start] = 0

        while frontier:

            priority, current = heapq.heappop(frontier)

            if current == end:
                break

            north: tuple[int, int] = (
                current[0] + self.directions["N"][0],
                current[1] + self.directions["N"][1],
            )
            south: tuple[int, int] = (
                current[0] + self.directions["S"][0],
                current[1] + self.directions["S"][1],
            )
            east: tuple[int, int] = (
                current[0] + self.directions["E"][0],
                current[1] + self.directions["E"][1],
            )
            west: tuple[int, int] = (
                current[0] + self.directions["W"][0],
                current[1] + self.directions["W"][1],
            )
            print(f"N {north} S {south} E {east} W {west}")
            neighbors: list[tuple[int, int]] = []
            if any([north, south, east, west]):
                neighbors = [north, south, east, west]
                random.shuffle(neighbors)

            for next in neighbors:
                if (
                    (next[1] < self.map_height and next[1] >= 0)
                    and (next[0] < self.map_width and next[0] >= 0)
                    and self.tile_array[next[1]][next[0]]
                    not in [
                        self.wall_North,
                        self.wall_South,
                        self.wall_East,
                        self.wall_West,
                        self.cornerbl,
                        self.cornerbr,
                        self.cornertl,
                        self.cornertr,
                    ]
                ):
                    new_cost: int = (
                        cost_so_far[current]
                        + self.costs[self.tile_array[next[1]][next[0]]]
                    )
                    if (
                        next not in cost_so_far
                        or new_cost < cost_so_far[(next[0], next[1])]
                    ):
                        cost_so_far[(next[0], next[1])] = new_cost
                        priority = new_cost + self.a_star_Heuristic(start, end)
                        heapq.heappush(frontier, (priority, (next[0], next[1])))
                        came_from[(next[0], next[1])] = current

        return came_from, cost_so_far

    def leaf_Recursion(
        self, start: tuple[int, int], leaves: list[tuple[int, int]]
    ) -> list[tuple[int, int]]:
        path_glob: list[tuple[int, int]] = []

        if len(leaves) == 0:
            return []

        came_from, _ = self.a_Star(start, leaves[-1])
        path = self.reconstruct_path(came_from, start, leaves[-1])
        path_glob.extend(path)
        path_glob.extend(self.leaf_Recursion(start, leaves[:-1]))
        return path_glob

    def create_Doors(self, path: list[tuple[int, int]]) -> None:

        for i in path:
            directions = self.get_directions(i[1], i[0])
            if any(
                [
                    directions["north"]
                    in [
                        self.wall_East,
                        self.wall_West,
                        self.cornerbl,
                        self.cornerbr,
                        self.cornertl,
                        self.cornertr,
                    ],
                    directions["south"]
                    in [
                        self.wall_East,
                        self.wall_West,
                        self.cornerbl,
                        self.cornerbr,
                        self.cornertl,
                        self.cornertr,
                    ],
                    directions["east"]
                    in [
                        self.wall_North,
                        self.wall_South,
                        self.cornerbl,
                        self.cornerbr,
                        self.cornertl,
                        self.cornertr,
                    ],
                    directions["west"]
                    in [
                        self.wall_North,
                        self.wall_South,
                        self.cornerbl,
                        self.cornerbr,
                        self.cornertl,
                        self.cornertr,
                    ],
                ]
            ):
                self.tile_array[i[1]][i[0]] = self.door
                self.door_coord.append((i[1], i[0]))
            else:
                self.tile_array[i[1]][i[0]] = self.floor

        for coord in self.corridor_cord:
            directions = self.get_directions(coord[0][0], coord[0][1])

            coordinate: str = self.tile_array[coord[0][0]][coord[0][1]]
            if coordinate != self.door:
                if coordinate == self.corridor_v:
                    if random.random() < self.door_percent:
                        if self.wall_North in [directions["east"], directions["west"]]:
                            self.tile_array[coord[0][0]][coord[0][1]] = self.wall_North
                            self.tile_array[coord[1][0]][coord[1][1]] = self.wall_South
                        else:
                            self.tile_array[coord[0][0]][coord[0][1]] = self.wall_South
                            self.tile_array[coord[1][0]][coord[1][1]] = self.wall_North
                    else:

                        self.tile_array[coord[0][0]][coord[0][1]] = self.locked
                        self.tile_array[coord[1][0]][coord[1][1]] = self.locked
                        self.door_coord.append((coord[0][0], coord[0][1]))
                        self.door_coord.append((coord[1][0], coord[1][1]))
                elif coordinate == self.corridor_h:
                    if random.random() < self.door_percent:
                        if self.wall_East in [directions["north"], directions["south"]]:
                            self.tile_array[coord[0][0]][coord[0][1]] = self.wall_East
                            self.tile_array[coord[1][0]][coord[1][1]] = self.wall_West
                        else:
                            self.tile_array[coord[0][0]][coord[0][1]] = self.wall_West
                            self.tile_array[coord[1][0]][coord[1][1]] = self.wall_East
                    else:
                        self.tile_array[coord[0][0]][coord[0][1]] = self.locked
                        self.tile_array[coord[1][0]][coord[1][1]] = self.locked
                        self.door_coord.append((coord[0][0], coord[0][1]))
                        self.door_coord.append((coord[1][0], coord[1][1]))

    def mesh_walls(self) -> None:
        for corner in self.corner_coord:
            directions = self.get_directions(corner[0], corner[1])

            replace_north_right: bool = directions["north"] in [
                self.wall_East,
                self.cornertr,
                self.cornerbr,
                self.wall_CornerL,
            ]

            replace_south_right: bool = directions["south"] in [
                self.wall_East,
                self.cornertr,
                self.cornerbr,
                self.wall_CornerL,
            ]

            replace_north_left: bool = directions["north"] in [
                self.wall_West,
                self.cornertl,
                self.cornerbl,
                self.wall_CornerR,
            ]

            replace_south_left: bool = directions["south"] in [
                self.wall_West,
                self.cornertl,
                self.cornerbl,
                self.wall_CornerR,
            ]
            if replace_north_right and replace_south_right:
                self.tile_array[corner[0]][corner[1]] = self.wall_East
            elif replace_north_left and replace_south_left:
                self.tile_array[corner[0]][corner[1]] = self.wall_West

    def clean_Doors(self):
        for door in self.door_coord:

            if self.tile_array[door[0]][door[1]] in [self.door, self.locked]:
                directions = self.get_directions(door[0], door[1])
                if directions["south"] in [self.door, self.locked]:
                    self.tile_array[door[0] + 1][door[1]] = self.floor

                elif directions["east"] in [self.door, self.locked] or directions[
                    "west"
                ] in [
                    self.door,
                    self.locked,
                ]:
                    if random.random() < 0.5:
                        self.tile_array[door[0]][door[1] + 1] = self.floor
                    else:
                        self.tile_array[door[0]][door[1]] = self.floor

    def clean_Walls(self) -> None:
        for wall in self.wall_coords:
            directions = self.get_directions(wall[0], wall[1])

            is_wall: bool = self.tile_array[wall[0]][wall[1]] in [
                self.wall_North,
                self.wall_South,
                self.wall_hL,
                self.wall_hR,
            ]

            remove_south: bool = directions["south"] in [
                self.wall_North,
                self.wall_South,
                self.wall_hL,
                self.wall_hR,
            ]
            if remove_south and is_wall:
                self.tile_array[wall[0] + 1][wall[1]] = self.floor

    # def cleanup_Dungeon(self) -> None:

    #     # Cleanup corners to mesh with walls

    #     for corner in self.corner_coord:
    #         north, south, east, west, northeast, northwest, southeast, southwest = (
    #             self.get_directions(corner[0], corner[1], w_range, h_range)
    #         )

    #         if north in [self.wall_West, self.wall_CornerR] and south in [
    #             self.wall_West,
    #             self.cornertl,
    #         ]:

    #             self.tile_array[corner[0]][corner[1]] = self.wall_West
    #         elif north in [self.wall_East, self.wall_CornerL] and south in [
    #             self.wall_East,
    #             self.cornertr,
    #         ]:
    #             self.tile_array[corner[0]][corner[1]] = self.wall_East
