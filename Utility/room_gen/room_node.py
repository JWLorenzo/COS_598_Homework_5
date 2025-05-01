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

        self.min_width: int = 10
        self.max_width: int = 18
        self.min_height: int = 10
        self.max_height: int = 18

        self.tile_array: tileArray = tile_array

        self.trim_amount: int = 2

        self.split_dir: str = ""

    def get_Center(self) -> tuple[int, int]:
        return (self.min_x + self.get_Width() // 2, self.min_y + self.get_Height() // 2)

    def is_Leaf(self):
        return self.left == None and self.right == None

    def get_Width(self):
        return self.max_x - self.min_x

    def get_Height(self):
        return self.max_y - self.min_y

    def split_Vert(self):
        split_Point_x = random.randint(
            self.min_x + (self.max_width // 2), self.max_x - (self.max_width // 2)
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
            self.min_y + (self.max_height // 2), self.max_y - (self.max_height // 2)
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
        if self.get_Width() <= self.min_width or self.get_Height() <= self.min_height:
            # Base Case
            return

        if self.get_Width() >= self.tile_array.map_width // 2:
            # Recursive Case Vertical Line big area
            self.split_Vert()
            return

        if self.get_Height() >= self.tile_array.map_height // 2:
            # Recursive Case Horizontal Line big area
            self.split_Hori()
            return

        if self.get_Width() > self.max_width and self.get_Height() > self.max_height:
            if random.random() < 0.5:
                # Recursive Case Small Vertical Line
                self.split_Vert()
                return

            else:
                # Recursive Case Small Horizontal Line
                self.split_Hori()
                return

    def carve_Dungeon(self) -> None:
        if self.is_Leaf():
            self.tile_array.carve_Area(
                self.min_x, self.max_x, self.min_y, self.max_y, "#", "."
            )
            return
        if self.left:
            self.left.carve_Dungeon()
        if self.right:
            self.right.carve_Dungeon()

    def trim_Rooms(self) -> None:
        if self.is_Leaf():
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

    def get_corridors(self) -> list[tuple[tuple[int, int], tuple[int, int],str]]:
        corridors: list[tuple[tuple[int, int], tuple[int, int],str]] = []

        if self.left:
            corridors += self.left.get_corridors()

        if self.right:
            corridors += self.right.get_corridors()

        if self.left and self.right:
            left_center: tuple[int, int] = self.left.get_Center()
            right_center: tuple[int, int] = self.right.get_Center()

            print(f"Corridor: left: {left_center} right: {right_center}")
            corridors.append((left_center, right_center,self.split_dir))
        return corridors
