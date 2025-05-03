from Utility.CONSTANTS import *
import random
import heapq


class tileArray:
    def __init__(self, width: int, height: int) -> None:
        self.map_width: int = width
        self.map_height: int = height
        self.floor: str = "."
        self.wall: str = "#"
        self.door: str = "@"
        self.empty: str = " "
        self.corridor_v: str = "|"
        self.corridor_h: str = "-"
        self.path: str = "P"
        self.wallr: str = "R"
        self.walll: str = "L"
        self.tile_array: list[list[str]] = [
            [self.empty for column in range(self.map_width)]
            for row in range(self.map_height)
        ]
        self.costs: dict[str, int] = {
            self.floor: 1,
            self.wall: 10000,
            self.corridor_v: 0,
            self.corridor_h: 0,
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
                if column in [x_min, x_max - 1] or row in [y_min, y_max - 1]:
                    if self.tile_array[row][column] not in [
                        self.path,
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
                        [self.wall, self.floor]
                        == [self.tile_array[row][0], self.tile_array[row][1]]
                    )
                    and (
                        [self.floor, self.wall]
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
                        [self.wall, self.floor]
                        == [self.tile_array[0][column], self.tile_array[1][column]]
                    )
                    and (
                        [self.floor, self.wall]
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

    def reconstruct_path(
        self,
        came_from: dict[tuple[int, int], tuple[int, int] | None],
        start: tuple[int, int],
        end: tuple[int, int],
    ):

        current = end
        path = []

        if end not in came_from:
            return []
        while current != start:
            prev = came_from[current]
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

            print("prio", priority)
            print("curre", current)

            if current == end:
                print("el fin")
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
            print("curre", current)
            print(f"N {north} S {south} E {east} W {west}")

            neighbors: list[tuple[int, int]] = [north, south, east, west]

            for next in neighbors:
                if (
                    (next[1] < self.map_height and next[1] >= 0)
                    and (next[0] < self.map_width and next[0] >= 0)
                    and self.tile_array[next[1]][next[0]] != self.wall
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
