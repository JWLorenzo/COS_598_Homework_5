from Utility.room_gen.tilearray import tileArray
import random


class Node:
    def __init__(
        self, min_x: int, max_x: int, min_y: int, max_y: int, tile_array: tileArray
    ) -> None:
        self.left: Node | None = None
        self.right: Node | None = None
        self.min_x: int = min_x
        self.max_x: int = max_x
        self.min_y: int = min_y
        self.max_y: int = max_y

        self.min_width: int = 8
        self.max_width: int = 20
        self.min_height: int = 8
        self.max_height: int = 20

        self.tile_array: tileArray = tile_array

        self.trim_amount: int = 1

        self.split_dir: str = ""

        self.corridor_margin: int = 2

        self.min_corridor_thickness: int = 3
        self.wilted: bool = False

    def get_Center(self) -> tuple[int, int]:

        return (
            (self.max_x + self.min_x) // 2,
            (self.max_y + self.min_y) // 2,
        )

    def is_Leaf(self):
        return ((self.left == None) or self.left.wilted) and (
            (self.right == None) or self.right.wilted
        )

    def get_Width(self):
        return self.max_x - self.min_x

    def get_Height(self):
        return self.max_y - self.min_y

    def split_Vert(self):
        split_Point_x = random.randint(
            self.min_x + (self.min_width), self.max_x - (self.min_width)
        )
        self.left = Node(
            self.min_x, split_Point_x, self.min_y, self.max_y, self.tile_array
        )
        self.right = Node(
            split_Point_x, self.max_x, self.min_y, self.max_y, self.tile_array
        )
        self.left.create_Dungeon()
        self.right.create_Dungeon()
        self.split_dir = "v"

    def split_Hori(self):
        split_Point_y = random.randint(
            self.min_y + (self.min_height), self.max_y - (self.min_height)
        )
        self.left = Node(
            self.min_x, self.max_x, self.min_y, split_Point_y, self.tile_array
        )
        self.right = Node(
            self.min_x, self.max_x, split_Point_y, self.max_y, self.tile_array
        )
        self.left.create_Dungeon()
        self.right.create_Dungeon()
        self.split_dir = "h"

    def create_Dungeon(self) -> None:
        if (
            self.get_Width() <= 2 * self.min_width
            or self.get_Height() <= 2 * self.min_height
        ):
            if self.get_Width() > 2 * self.min_width:
                self.split_Vert()
                return
            if self.get_Height() > 2 * self.min_height:
                self.split_Hori()
                return
            self.wilted = True
            return

        if (
            self.get_Width() > 2 * self.min_width
            and self.get_Height() > 2 * self.min_height
        ):
            if self.get_Height() >= self.get_Width():
                # Recursive Case Small Horizontal Line
                self.split_Hori()
                return

            else:
                # Recursive Case Small Vertical Line
                self.split_Vert()
                return

    def carve_Dungeon(self) -> None:
        if self.is_Leaf():
            self.tile_array.carve_Area(self.min_x, self.max_x, self.min_y, self.max_y)
            return
        if self.left:
            self.left.carve_Dungeon()
        if self.right:
            self.right.carve_Dungeon()

    def trim_Rooms(self) -> None:
        if self.is_Leaf():
            # trim_min_x: int = self.min_x + random.randint(
            #     self.trim_amount, self.trim_amount + 1
            # )
            # trim_max_x: int = self.max_x - random.randint(
            #     self.trim_amount, self.trim_amount + 1
            # )
            # trim_min_y: int = self.min_y + random.randint(
            #     self.trim_amount, self.trim_amount + 1
            # )
            # trim_max_y: int = self.max_y - random.randint(
            #     self.trim_amount, self.trim_amount + 1
            # )
            self.min_x += self.trim_amount
            self.max_x -= self.trim_amount
            self.min_y += self.trim_amount
            self.max_y -= self.trim_amount

            print(
                f"Rectangle created at: (x_1 {self.min_x} y_1 {self.min_y}), (x_2 {self.max_x}, y_2 {self.max_y})"
            )
        if self.left:
            self.left.trim_Rooms()

        if self.right:
            self.right.trim_Rooms()

    def get_corridors(self) -> list[tuple[tuple[int, int], tuple[int, int]]]:
        corridors: list[tuple[tuple[int, int], tuple[int, int]]] = []

        if self.left:
            corridors += self.left.get_corridors()

        if self.right:
            corridors += self.right.get_corridors()

        if (self.left) and (self.right):
            left_center: tuple[int, int] = self.left.get_Center()
            right_center: tuple[int, int] = self.right.get_Center()

            print(f"Corridor: left: {left_center} right: {right_center}")
            corridors.append((left_center, right_center))
        return corridors

    def get_right_connections(self) -> list[int]:
        connections: list[int] = []
        if not self.is_Leaf():
            if self.right:

                connections.extend(self.right.get_right_connections())
            if self.left and self.split_dir == "h":
                connections.extend(self.left.get_right_connections())
        else:
            for y in range(
                self.min_y + self.corridor_margin - 1,
                self.max_y - self.corridor_margin + 1,
            ):
                connections.append(y)
                # self.tile_array.tile_array[y][self.max_x - 1] = "E"
        return connections

    def get_left_connections(self) -> list[int]:
        connections: list[int] = []
        if not self.is_Leaf():
            if self.left:
                connections.extend(self.left.get_left_connections())
            if self.right and self.split_dir == "h":
                connections.extend(self.right.get_left_connections())
        else:
            for y in range(
                self.min_y + self.corridor_margin - 1,
                self.max_y - self.corridor_margin + 1,
            ):
                connections.append(y)
                # self.tile_array.tile_array[y][self.min_x] = "W"
        return connections

    def get_top_connections(self) -> list[int]:
        connections: list[int] = []
        if not self.is_Leaf():
            if self.left:
                connections.extend(self.left.get_top_connections())
            if self.right and self.split_dir == "v":
                connections.extend(self.right.get_top_connections())
        else:
            for x in range(
                self.min_x + self.corridor_margin - 1,
                self.max_x - self.corridor_margin + 1,
            ):
                connections.append(x)
                # self.tile_array.tile_array[self.min_y][x] = "N"
        return connections

    def get_bottom_connections(self) -> list[int]:
        connections: list[int] = []
        if not self.is_Leaf():
            if self.right:
                connections.extend(self.right.get_bottom_connections())
            if self.left and self.split_dir == "v":
                connections.extend(self.left.get_bottom_connections())
        else:
            for x in range(
                self.min_x + self.corridor_margin - 1,
                self.max_x - self.corridor_margin + 1,
            ):
                connections.append(x)
                # self.tile_array.tile_array[self.max_y - 1][x] = "S"
        return connections

    def get_intersection_groups(
        self, group_a: list[int], group_b: list[int]
    ) -> list[int]:
        return sorted(set(group_a) & set(group_b))

    def get_connection_groups(self, points: list[int]) -> list[list[int]]:
        groups: list[list[int]] = []

        first_iteration: bool = True

        current_group: list[int] = [0, 0]

        for i in range(len(points)):
            num: int = points[i]

            if first_iteration or points[i - 1] != points[i] - 1:
                if not first_iteration:
                    groups.append(current_group)

                first_iteration = False
                current_group = [num, num]
            else:
                current_group[1] += 1

        if not first_iteration:
            groups.append(current_group)

        return [g for g in groups if g[1] - g[0] >= self.min_corridor_thickness]

    def add_corridors(self) -> None:
        positions: list[int] = []
        groups: list[list[int]] = []
        p: list[int] = []
        q: int = 0
        if self.is_Leaf():
            return

        if self.left:
            self.left.add_corridors()
        if self.right:
            self.right.add_corridors()

        if self.left and self.right:
            if self.split_dir == "v":
                positions = self.get_intersection_groups(
                    self.left.get_right_connections(), self.right.get_left_connections()
                )
                groups = self.get_connection_groups(positions)

                p = random.choice(groups)
                q = random.randrange(p[0], p[1])
                self.tile_array.draw_corridor(
                    self.left.max_x - 1, self.left.max_x + 1, p[0], p[1]
                )
            else:
                positions = self.get_intersection_groups(
                    self.left.get_bottom_connections(), self.right.get_top_connections()
                )
                groups = self.get_connection_groups(positions)
                p = random.choice(groups)
                q = random.randrange(p[0], p[1])
                self.tile_array.draw_corridor(
                    p[0], p[1], self.left.min_y - 1, self.left.min_y + 1
                )
