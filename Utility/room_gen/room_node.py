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
        self.max_width: int = 16
        self.min_height: int = 8
        self.max_height: int = 16

        self.tile_array: tileArray = tile_array

        self.trim_amount: int = 1

        self.split_dir: str = ""

        self.corridor_margin: int = 2

        self.min_corridor_thickness: int = 3
        self.is_corridor: bool = False

        self.corridor_chance = 0.5

    def get_Center(self) -> tuple[int, int]:
        return (
            (self.max_x + self.min_x) // 2,
            (self.max_y + self.min_y) // 2,
        )

    def get_Endpoint_North(self) -> tuple[int, int]:
        return ((self.max_x + self.min_x) // 2, self.max_y)

    def get_Endpoint_South(self) -> tuple[int, int]:
        return ((self.max_x + self.min_x) // 2, self.min_y)

    def get_Endpoint_East(self) -> tuple[int, int]:
        return (self.max_x, (self.max_y + self.min_y) // 2)

    def get_Endpoint_West(self) -> tuple[int, int]:
        return (self.min_x, (self.max_y + self.min_y) // 2)

    def is_Leaf(self):
        return (self.left == None) and (self.right == None)

    def get_Width(self):
        return self.max_x - self.min_x

    def get_Height(self):
        return self.max_y - self.min_y

    def get_leaf_centers(self) -> list[tuple[int, int]]:
        leaf_list: list[tuple[int, int]] = []

        if self.is_Leaf():
            return [self.get_Center()]

        if self.left:
            leaf_list.extend(self.left.get_leaf_centers())

        if self.right:
            leaf_list.extend(self.right.get_leaf_centers())

        return leaf_list

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

    def mark_as_Corridor(self) -> None:
        if self.is_Leaf():

            door_list: list[str] = [
                self.tile_array.door,
                self.tile_array.locked,
            ]

            north_wall: list[str] = self.tile_array.tile_array[self.min_y][
                self.min_x + 1 : self.max_x
            ]
            south_wall: list[str] = self.tile_array.tile_array[self.max_y - 1][
                self.min_x + 1 : self.max_x
            ]
            east_wall: list[str] = [
                self.tile_array.tile_array[y][self.max_x - 1]
                for y in range(self.min_y + 1, self.max_y)
            ]
            west_wall: list[str] = [
                self.tile_array.tile_array[y][self.min_x]
                for y in range(self.min_y + 1, self.max_y)
            ]
            north_valid: bool = any([x in north_wall for x in door_list])
            south_valid: bool = any([x in south_wall for x in door_list])
            east_valid: bool = any([x in east_wall for x in door_list])
            west_valid: bool = any([x in west_wall for x in door_list])

            if (
                [north_valid, south_valid, east_valid, west_valid].count(True) >= 2
            ) and random.random() > self.corridor_chance:
                print("Successfully marked")
                self.is_corridor = True
                self.tile_array.corridor_rooms.append(
                    (self.min_x, self.max_x, self.min_y, self.max_y)
                )
            return

        if self.left:
            self.left.mark_as_Corridor()
        if self.right:
            self.right.mark_as_Corridor()

    def trim_Rooms(self) -> None:
        if self.is_Leaf():
            self.min_x += self.trim_amount
            self.max_x -= self.trim_amount
            self.min_y += self.trim_amount
            self.max_y -= self.trim_amount

        if self.left:
            self.left.trim_Rooms()

        if self.right:
            self.right.trim_Rooms()
