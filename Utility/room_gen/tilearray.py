from Utility.CONSTANTS import *
import random
import heapq


class tileArray:
    def __init__(self, width: int, height: int) -> None:

        # SYMBOLS

        self.floor: str = "."
        self.empty: str = " "
        self.corridor_v: str = "|"
        self.corridor_h: str = "-"
        self.cornertr: str = "]"
        self.cornertl: str = "["
        self.cornerbr: str = "}"
        self.cornerbl: str = "{"
        self.wall_North: str = "N"
        self.wall_South: str = "S"
        self.wall_East: str = "E"
        self.wall_West: str = "W"
        self.wall_CornerR: str = ">"
        self.wall_CornerL: str = "<"
        self.wall_hL: str = "L"
        self.wall_hR: str = "R"

        # WALL_VARS

        self.corner_coord: list[tuple[int, int]] = []  # row, column
        self.wall_coords: list[tuple[int, int]] = []  # row, column

        # TILE_ARRAY

        self.map_width: int = width
        self.map_height: int = height
        self.tile_array: list[list[str]] = [
            [self.empty for _ in range(self.map_width)] for _ in range(self.map_height)
        ]

        # DOOR VARS
        self.door_coord: list[tuple[int, int]] = []
        self.corridor_cord: list[tuple[tuple[int, int], tuple[int, int]]] = []
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
        }
        self.directions: dict[str, tuple[int, int]] = {
            "N": (0, -1),
            "S": (0, 1),
            "E": (1, 0),
            "W": (-1, 0),
        }

    def carve_Area(self, x_min: int, x_max: int, y_min: int, y_max: int) -> None:
        w_range: list[int] = list(range(self.map_width))
        h_range: list[int] = list(range(self.map_height))
        for row in range(y_min, y_max):
            for column in range(x_min, x_max):
                north, south, east, west, northeast, northwest, southeast, southwest = (
                    self.get_directions(row, column, w_range, h_range)
                )

                if column == x_min and row == y_min:
                    # Corner BL
                    self.tile_array[row][column] = self.cornertl
                    self.corner_coord.append((row, column))
                elif column == x_max - 1 and row == y_min:
                    # Corner BR
                    self.tile_array[row][column] = self.cornertr
                    self.corner_coord.append((row, column))
                elif column == x_min and row == y_max - 1:
                    # Corner TL
                    self.tile_array[row][column] = self.cornerbl
                    self.corner_coord.append((row, column))
                elif column == x_max - 1 and row == y_max - 1:
                    # Corner TR
                    self.tile_array[row][column] = self.cornerbr
                    self.corner_coord.append((row, column))

                elif column in range(x_min, x_max) and row == y_min:
                    self.tile_array[row][column] = self.wall_North
                elif column in range(x_min, x_max) and row == y_max - 1:
                    self.tile_array[row][column] = self.wall_South
                elif row in range(y_min, y_max) and column == x_min:
                    self.tile_array[row][column] = self.wall_West
                elif row in range(y_min, y_max) and column == x_max - 1:
                    self.tile_array[row][column] = self.wall_East

                else:
                    self.tile_array[row][column] = self.floor

                if self.tile_array[row][column] != self.floor:
                    self.wall_coords.append((row, column))

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

    def vertical_corridors(
        self, iter_list: list[list[list[int]]], max: int, min: int
    ) -> None:
        rand_index: int = 0
        if len(iter_list) > 0:
            if len(iter_list) > 2:
                rand_index = random.randrange(0, len(iter_list))
            element: list[list[int]] = iter_list.pop(rand_index)
            rand_row: int = random.randint(min, max)
            self.tile_array[rand_row][element[0][1]] = self.corridor_h
            self.tile_array[rand_row][element[1][1]] = self.corridor_h
            self.corridor_cord.append(
                ((rand_row, element[0][1]), (rand_row, element[1][1]))
            )
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
            self.tile_array[element[0][0]][rand_column] = self.corridor_v
            self.tile_array[element[1][0]][rand_column] = self.corridor_v
            self.corridor_cord.append(
                ((element[0][0], rand_column), (element[1][0], rand_column))
            )
            self.horizontal_corridors(iter_list, max, min)
        return

    def iterative_doors(self) -> None:
        coord_list: list[list[list[int]]] = []
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
                                coord_list.append([[row, column], [row, column + 1]])
                                x_list.append(column)
                            y_list.append(row)
                            y_list = sorted(y_list)
                else:
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
        w_range: list[int] = list(range(self.map_width))
        h_range: list[int] = list(range(self.map_height))

        for i in path:
            north, south, east, west, northeast, northwest, southeast, southwest = (
                self.get_directions(i[1], i[0], w_range, h_range)
            )
            if any(
                [
                    north
                    in [
                        self.wall_East,
                        self.wall_West,
                        self.cornerbl,
                        self.cornerbr,
                        self.cornertl,
                        self.cornertr,
                    ],
                    south
                    in [
                        self.wall_East,
                        self.wall_West,
                        self.cornerbl,
                        self.cornerbr,
                        self.cornertl,
                        self.cornertr,
                    ],
                    east
                    in [
                        self.wall_North,
                        self.wall_South,
                        self.cornerbl,
                        self.cornerbr,
                        self.cornertl,
                        self.cornertr,
                    ],
                    west
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
            north, south, east, west, northeast, northwest, southeast, southwest = (
                self.get_directions(coord[0][0], coord[0][1], w_range, h_range)
            )
            coordinate: str = self.tile_array[coord[0][0]][coord[0][1]]
            print("COORD", coordinate)
            if coordinate != self.door:
                if coordinate == self.corridor_v:
                    if random.random() < self.door_percent:
                        if self.wall_North in [east, west]:
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
                        if self.wall_East in [north, south]:
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

    def cleanup_Dungeon(self) -> None:
        w_range: list[int] = list(range(self.map_width))
        h_range: list[int] = list(range(self.map_height))
        # Cleanup tiles above doorways
        for door in self.door_coord:

            north, south, east, west, northeast, northwest, southeast, southwest = (
                self.get_directions(door[0], door[1], w_range, h_range)
            )

            if south in [self.wall_East, self.cornerbr] or southeast == self.wall_West:
                # Set the southern tile to a corner
                if southwest != self.wall_South:
                    self.tile_array[door[0] + 1][door[1]] = self.wall_CornerR
                else:
                    self.tile_array[door[0] + 1][door[1]] = self.wall_South

            elif (
                south in [self.wall_West, self.cornerbl] or southwest == self.wall_East
            ):
                # Set the southern tile to a corner
                if southeast != self.wall_South:
                    self.tile_array[door[0] + 1][door[1]] = self.wall_CornerL
                else:
                    self.tile_array[door[0] + 1][door[1]] = self.wall_South

            if north in [self.wall_East, self.cornertr]:
                self.tile_array[door[0] - 1][door[1]] = self.wall_hL
            elif north in [self.wall_West, self.cornertl]:
                self.tile_array[door[0] - 1][door[1]] = self.wall_hR

        for door in self.door_coord:

            if self.tile_array[door[0]][door[1]] in [self.door, self.locked]:
                north, south, east, west, northeast, northwest, southeast, southwest = (
                    self.get_directions(door[0], door[1], w_range, h_range)
                )
                if south in [self.door, self.locked]:
                    self.tile_array[door[0] + 1][door[1]] = self.floor

                elif east in [self.door, self.locked] or west in [
                    self.door,
                    self.locked,
                ]:
                    if random.random() < 0.5:
                        self.tile_array[door[0]][door[1] + 1] = self.floor
                    else:
                        self.tile_array[door[0]][door[1]] = self.floor

        # Cleanup walls

        for wall in self.wall_coords:
            north, south, east, west, northeast, northwest, southeast, southwest = (
                self.get_directions(wall[0], wall[1], w_range, h_range)
            )
            # print("I WAS HERE")
            # print(self.tile_array[wall[0]][wall[1]])
            # print(south)
            if (self.tile_array[wall[0]][wall[1]] == self.wall_South) and (
                south == self.wall_North
            ):
                # print("NICE TRY")
                self.tile_array[wall[0] + 1][wall[1]] = self.floor

        # Cleanup corners to mesh with walls

        for corner in self.corner_coord:
            north, south, east, west, northeast, northwest, southeast, southwest = (
                self.get_directions(corner[0], corner[1], w_range, h_range)
            )

            if north in [self.wall_West, self.wall_CornerR] and south in [
                self.wall_West,
                self.cornertl,
            ]:
                self.tile_array[corner[0]][corner[1]] = self.wall_West
            elif north in [self.wall_East, self.wall_CornerL] and south in [
                self.wall_East,
                self.cornertr,
            ]:
                self.tile_array[corner[0]][corner[1]] = self.wall_East
