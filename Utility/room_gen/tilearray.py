from Utility.CONSTANTS import *
import random
import heapq
import math


class tileArray:
    def __init__(self, width: int, height: int) -> None:

        # Basic
        self.empty: str = "."
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
        self.cornerbr: str = "}"
        self.cornerbl: str = "{"
        self.wall_hL: str = "L"
        self.wall_hR: str = "R"
        self.wall_CornerR: str = ">"
        self.wall_CornerL: str = "<"

        # Wall Arrays

        self.corner_coord: list[tuple[int, int]] = []  # row, column
        self.wall_coords: dict[tuple[int, int], None] = {}  # row, column
        self.corridor_rooms: dict[
            tuple[int, int, int, int], dict[str, list[tuple[int, int]]]
        ] = {}  # xmin, xmax, ymin,ymax : row,col
        # Floor Tiles

        self.floor: str = " "

        # Corridor Pre Door

        self.corridor_v: str = "|"
        self.corridor_h: str = "-"
        self.corridor_cord: list[tuple[tuple[int, int], tuple[int, int]]] = (
            []
        )  # (corridor 1: (row, column) , corridor 2: (row, column))

        # Door
        self.door_coord: list[tuple[int, int]] = []
        self.door_percent: float = 0.25
        self.door: str = "P"
        self.locked: str = "!"

        # PATHFINDING

        self.costs: dict[str, int] = {
            self.floor: 2,
            self.door: 0,
            self.corridor_v: 1,
            self.corridor_h: 1,
            self.wall_North: 100000000,
            self.wall_South: 100000000,
            self.wall_East: 100000000,
            self.wall_West: 100000000,
            self.cornerbr: 100000000,
            self.cornerbl: 100000000,
            self.wall_hL: 100000000,
            self.wall_hR: 100000000,
            self.wall_CornerR: 100000000,
            self.wall_CornerL: 100000000,
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
                    tile = self.wall_West

                elif is_top and is_right:
                    tile = self.wall_East

                elif is_bottom and is_left:
                    tile = self.cornerbl

                elif is_bottom and is_right:
                    tile = self.cornerbr

                elif (is_top or is_bottom) and is_left_end:
                    tile = self.wall_hL

                # elif (is_top or is_bottom) and is_right_end:
                #     tile = self.wall_hR

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
                    self.wall_coords[(row, column)] = None

                if tile in (self.cornerbl, self.cornerbr):
                    self.corner_coord.append((row, column))

    def carve_Entries(
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
                        self.carve_Entries(coord_list, y_list[0], y_list[-1])
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
                    self.carve_Entries(
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
            # if any([north, south, east, west]):
            neighbors = [north, south, east, west]
            # neighbors

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
                        self.wall_hL,
                        self.wall_hR,
                        self.wall_CornerR,
                        self.wall_CornerL,
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

    def a_Star_Version_2(self, start: tuple[int, int], end: tuple[int, int]):
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
            print(f"V2 N {north} S {south} E {east} W {west}")
            neighbors: list[tuple[int, int]] = []
            neighbors = [north, south, east, west]
            # neighbors

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
                        self.wall_hL,
                        self.wall_hR,
                        self.wall_CornerR,
                        self.wall_CornerL,
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
        if TEST:
            came_from, _ = self.a_Star_Version_2(start, leaves[-1])
        else:
            came_from, _ = self.a_Star(start, leaves[-1])
        path = self.reconstruct_path(came_from, start, leaves[-1])
        path_glob.extend(path)
        if TEST:
            for i in path:
                self.tile_array[i[1]][i[0]] = self.door
            path_glob.extend(self.leaf_Recursion(leaves[-1], leaves[:-1]))
        else:
            path_glob.extend(self.leaf_Recursion(leaves[-1], leaves[:-1]))
        return path_glob

    def create_Doors(self, path: list[tuple[int, int]]) -> None:

        for i in path:
            directions = self.get_directions(i[1], i[0])
            east: bool = directions["east"] in [
                self.wall_North,
                self.wall_South,
                self.wall_East,
                self.wall_West,
                self.cornerbl,
                self.cornerbr,
                self.wall_hL,
                self.wall_hR,
                self.wall_CornerR,
                self.wall_CornerL,
            ]

            west: bool = directions["west"] in [
                self.wall_North,
                self.wall_South,
                self.wall_East,
                self.wall_West,
                self.cornerbl,
                self.cornerbr,
                self.wall_hL,
                self.wall_hR,
                self.wall_CornerR,
                self.wall_CornerL,
            ]

            north: bool = directions["north"] in [
                self.wall_North,
                self.wall_South,
                self.wall_East,
                self.wall_West,
                self.cornerbl,
                self.cornerbr,
                self.wall_hL,
                self.wall_hR,
                self.wall_CornerR,
                self.wall_CornerL,
            ]

            south: bool = directions["south"] in [
                self.wall_North,
                self.wall_South,
                self.wall_East,
                self.wall_West,
                self.cornerbl,
                self.cornerbr,
                self.wall_hL,
                self.wall_hR,
                self.wall_CornerR,
                self.wall_CornerL,
            ]

            if (north and south) or (east and west):
                self.tile_array[i[1]][i[0]] = self.door
                self.door_coord.append((i[1], i[0]))
            else:
                self.tile_array[i[1]][i[0]] = self.floor

        for coord in self.corridor_cord:
            directions = self.get_directions(coord[0][0], coord[0][1])

            coordinate: str = self.tile_array[coord[0][0]][coord[0][1]]
            if coordinate != self.door:
                if coordinate == self.corridor_v:
                    if random.random() > self.door_percent:
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
                        self.wall_coords.pop((coord[0][0], coord[0][1]), None)
                        self.wall_coords.pop((coord[1][0], coord[1][1]), None)
                elif coordinate == self.corridor_h:
                    if random.random() > self.door_percent:
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
                        self.wall_coords.pop((coord[0][0], coord[0][1]), None)
                        self.wall_coords.pop((coord[1][0], coord[1][1]), None)

    def mesh_walls(self) -> None:
        for corner in self.corner_coord:
            directions = self.get_directions(corner[0], corner[1])

            replace_north_right: bool = directions["north"] in [
                self.wall_East,
                self.cornerbl,
                self.cornerbr,
                self.wall_CornerL,
                self.wall_CornerR,
                self.wall_hL,
                self.wall_hR,
            ]

            replace_south_right: bool = directions["south"] in [
                self.wall_East,
                self.wall_CornerL,
                self.wall_CornerR,
                self.wall_hL,
                self.wall_hR,
            ]

            replace_north_left: bool = directions["north"] in [
                self.wall_West,
                self.wall_CornerL,
                self.wall_CornerR,
                self.wall_hL,
                self.wall_hR,
            ]
            replace_south_left: bool = directions["south"] in [
                self.wall_West,
                self.wall_CornerL,
                self.wall_CornerR,
                self.wall_hL,
                self.wall_hR,
            ]
            if replace_north_right and replace_south_right:
                self.tile_array[corner[0]][corner[1]] = self.wall_East
            elif replace_north_left and replace_south_left:
                self.tile_array[corner[0]][corner[1]] = self.wall_West
        pass

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
        cleanup_list: list[tuple[int, int]] = []
        for wall in self.wall_coords:
            directions = self.get_directions(wall[0], wall[1])

            is_wall: bool = self.tile_array[wall[0]][wall[1]] in [
                self.wall_North,
                self.wall_South,
                self.cornerbl,
                self.cornerbr,
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
                cleanup_list.append((wall[0] + 1, wall[1]))
        for i in cleanup_list:
            self.wall_coords.pop(i, None)

    def create_inner_Corners(self) -> None:
        for wall in self.wall_coords:
            directions = self.get_directions(wall[0], wall[1])

            current_tile: str = self.tile_array[wall[0]][wall[1]]

            nonwall_list: list[str] = [
                self.door,
                self.locked,
                self.floor,
            ]

            corner_list: list[str] = [
                self.cornerbl,
                self.cornerbr,
            ]

            inner_corner_list: list[str] = [
                self.wall_CornerL,
                self.wall_CornerR,
            ]

            horizontal_wall_list: list[str] = [
                self.wall_North,
                self.wall_South,
                self.wall_hL,
                self.wall_hR,
            ]

            vertical_wall_list: list[str] = [
                self.wall_East,
                self.wall_West,
            ]

            north_nonwall: bool = directions["north"] in nonwall_list

            south_nonwall: bool = directions["south"] in nonwall_list
            east_nonwall: bool = directions["east"] in nonwall_list

            west_nonwall: bool = directions["west"] in nonwall_list
            southeast_nonwall: bool = directions["southeast"] in nonwall_list
            southwest_nonwall: bool = directions["southwest"] in nonwall_list
            is_horizontal_wall: bool = current_tile in horizontal_wall_list
            is_vertical_wall: bool = current_tile in vertical_wall_list
            is_north_vertical: bool = directions["north"] in vertical_wall_list
            is_south_vertical: bool = directions["south"] in vertical_wall_list
            is_west_vertical: bool = directions["west"] in vertical_wall_list
            is_east_vertical: bool = directions["east"] in vertical_wall_list
            is_southwest_vertical: bool = directions["southwest"] in vertical_wall_list
            is_southeast_vertical: bool = directions["southeast"] in vertical_wall_list

            is_south_horizontal: bool = directions["south"] in horizontal_wall_list
            is_north_horizontal: bool = directions["north"] in horizontal_wall_list

            is_innner_corner: bool = current_tile in inner_corner_list

            is_east_inner_corner: bool = directions["east"] in inner_corner_list
            is_west_inner_corner: bool = directions["west"] in inner_corner_list
            is_corner: bool = current_tile in corner_list
            is_east_corner = directions["east"] in corner_list
            is_west_corner = directions["west"] in corner_list
            is_north_corner = directions["north"] in corner_list
            is_south_corner = directions["south"] in corner_list
            is_south_empty: bool = directions["south"] == ""
            is_north_empty: bool = directions["north"] == ""
            tile: str = ""

            if is_corner:
                if south_nonwall:
                    if (not east_nonwall) and southeast_nonwall:
                        tile = self.wall_South
                    elif (not west_nonwall) and southwest_nonwall:
                        tile = self.wall_South
                    elif directions["west"] == self.wall_CornerR:
                        tile = self.wall_hL
                elif is_south_vertical:
                    if north_nonwall:
                        if directions["south"] == self.wall_East:
                            tile = self.wall_CornerL
                        elif directions["south"] == self.wall_West:
                            tile = self.wall_CornerR
                    elif is_southeast_vertical:
                        tile = self.wall_CornerL
                    elif is_southwest_vertical:
                        tile = self.wall_CornerR

            elif is_vertical_wall and north_nonwall:
                if is_south_vertical:
                    if is_southeast_vertical:
                        tile = self.wall_CornerL
                    elif is_southwest_vertical:
                        tile = self.wall_CornerR
                    elif directions["east"] == self.wall_CornerR:
                        tile = self.wall_CornerL
                    elif directions["west"] == self.wall_CornerL:
                        tile = self.wall_CornerR
                elif is_south_horizontal or is_south_corner:
                    if current_tile == self.wall_East:
                        tile = self.wall_CornerL
                    elif current_tile == self.wall_West:
                        tile = self.wall_CornerR

            elif is_vertical_wall and (not north_nonwall) and south_nonwall:
                if not east_nonwall:
                    tile = self.wall_hL
                elif not west_nonwall:
                    tile = self.wall_South

            elif is_horizontal_wall and is_north_empty:
                if is_west_vertical:
                    tile = self.wall_hL

            elif is_horizontal_wall and north_nonwall:

                if is_south_vertical:
                    if is_southeast_vertical:
                        tile = self.wall_CornerL
                    elif is_southwest_vertical:
                        tile = self.wall_CornerR

                elif east_nonwall:
                    tile = self.wall_South
                elif west_nonwall:
                    tile = self.wall_hL

                elif is_west_inner_corner:
                    tile = self.wall_hL
                elif is_east_inner_corner:
                    tile = self.wall_South
            elif is_south_empty and north_nonwall:
                tile = self.wall_South

            elif is_north_empty and south_nonwall:
                tile = self.wall_North
            if tile:
                self.tile_array[wall[0]][wall[1]] = tile

    def create_Corridor(self) -> None:

        for room in self.corridor_rooms:
            x_min, x_max, y_min, y_max = room
            for row in range(y_min + 1, y_max - 1):
                for column in range(x_min + 1, x_max - 1):
                    self.tile_array[row][column] = self.empty
            # col_avg_coord: int = sum([x[1] for x in self.corridor_rooms[room]]) // len(
            #     self.corridor_rooms[room]
            # )
            # row_avg_coord: int = sum([y[0] for y in self.corridor_rooms[room]]) // len(
            #     self.corridor_rooms[room]
            # )
            print(
                f"flat x: {[x[1] for l in self.corridor_rooms[room].values() for x in l]}"
            )
            print(
                f"flat y: {[x[0] for l in self.corridor_rooms[room].values() for x in l]}"
            )
            flat_x: list[int] = [
                x[1] for l in self.corridor_rooms[room].values() for x in l
            ]
            flat_y: list[int] = [
                y[0] for l in self.corridor_rooms[room].values() for y in l
            ]

            x_center: int = math.ceil(sum(flat_x) / len(flat_x))
            y_center: int = math.ceil(sum(flat_y) / len(flat_y))

            self.tile_array[y_center][x_center] = self.floor

            for direction in self.corridor_rooms[room]:
                for door in self.corridor_rooms[room][direction]:
                    lesser_x: bool = door[1] < x_center
                    greater_x: bool = door[1] > x_center
                    lesser_y: bool = door[0] < y_center
                    greater_y: bool = door[0] > y_center

                    door_row, door_col = door

                    if direction == "N":
                        for row in range(door_row + 1, y_center + 1):
                            self.tile_array[row][door_col] = self.floor
                        if lesser_x:
                            for col in range(door_col + 1, x_center + 1):
                                self.tile_array[y_center][col] = self.floor
                        elif greater_x:
                            for col in range(x_center, door_col):
                                self.tile_array[y_center][col] = self.floor
                    elif direction == "S":
                        for row in range(y_center, door_row):
                            self.tile_array[row][door_col] = self.floor
                        if lesser_x:
                            for col in range(door_col + 1, x_center + 1):
                                self.tile_array[y_center][col] = self.floor
                        elif greater_x:
                            for col in range(x_center, door_col):
                                self.tile_array[y_center][col] = self.floor
                    elif direction == "E":
                        for col in range(x_center, door_col):
                            self.tile_array[door_row][col] = self.floor
                        if lesser_y:
                            for row in range(door_row + 1, y_center + 1):
                                self.tile_array[row][x_center] = self.floor
                        else:
                            for row in range(y_center, door_row):
                                self.tile_array[row][x_center] = self.floor
                    elif direction == "W":
                        for col in range(door_col + 1, x_center + 1):
                            self.tile_array[door_row][col] = self.floor
                        if lesser_y:
                            for row in range(door_row + 1, y_center + 1):
                                self.tile_array[row][x_center] = self.floor
                        else:
                            for row in range(y_center, door_row):
                                self.tile_array[row][x_center] = self.floor
            print(room, self.corridor_rooms[room])
            # print(f"Wall Door Coords: North {}")

    # Pseudocode for handling the corridor cells.
    """
    Hold a boolean that contains if the cell is a corridor or a room
    We can add this as a tag during the binary space partitioning with ease. 
    We can also keep track of the coordinates of the four corners of the room.

    When generating paths, we generate as normal, then we iterate over just the corridor rooms.

    Check each wall of the room, if it contains a doorway, keep it, else, if there is a blank spot, use that as the corridor entry point.

    For each wall, get the coordinates of the door or entryway. Randomly pick one of the doorways and then do l-shaped corridors towards that doorway. 

    For deciding the shape of the doorway, we pick the center of the room.
    - If either coord aligns with the center, we just draw a straight line of floor tiles
    - If the y coordinate is greater, we draw a line horizontally until we are at the x of the center, then we draw a line upwards to the middle
    - If the y coordinate is lesser, we draw a line horizontally until we are at the x of the center, then we draw downwards
    - If the x is greater, we draw going left
    - If the x is lesser, we draw going right
    
    Then, just run the wall cleanup as before.
    """
