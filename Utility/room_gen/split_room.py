from Utility.room_gen.room import Room
import random
from Utility.room_gen.tilearray import tileArray
from Utility.CONSTANTS import TEST
import pygame
from Utility.room_gen.corridor import Corridor

# We should change it to LRTP
# Original was left, bottom, right, top


class split_room(Room):
    def __init__(
        self, left: int, right: int, top: int, bottom: int, tile_array: tileArray
    ) -> None:
        super().__init__(left, right, top, bottom, tile_array)

        self.minWidth: int = 8
        self.maxWidth: int = 20
        self.minHeight: int = 8
        self.maxHeight: int = 20
        self.horizontal_split: bool = False
        self.vertical_split: bool = False

        self.left_Room: split_room | None = None
        self.right_Room: split_room | None = None

        if self.get_Width() < self.minWidth or self.get_Height() < self.minHeight:
            print(
                f"Room too small ({self.get_Width()}, {self.get_Height()}) to split. "
                f"Width min: {self.minWidth}, Height min: {self.minHeight}"
            )

    def is_leaf(self) -> bool:
        return not self.horizontal_split and not self.vertical_split

    def split_horizontally(self) -> None:
        if self.get_Height() < (2 * self.minHeight):
            return

        if (self.get_Bottom() + self.minHeight) > (self.get_Top() - self.minHeight):
            return

        split_point: int = 0
        if not TEST:
            split_point = random.randint(
                self.get_Bottom() + self.minHeight, self.get_Top() - self.minHeight
            )
        else:
            split_point = self.get_Bottom() + self.get_Height() // 2

        self.left_Room = split_room(
            self.get_Left(),
            self.get_Right(),
            split_point,
            self.get_Bottom(),
            self.tile_array,
        )

        self.right_Room = split_room(
            self.get_Left(),
            self.get_Right(),
            self.get_Top(),
            split_point + 1,
            self.tile_array,
        )
        self.left_Room.split()
        self.right_Room.split()
        self.horizontal_split = True

    def split_vertically(self) -> None:
        if self.get_Width() < (2 * self.minWidth):
            return

        if (self.get_Left() + self.minWidth) > (self.get_Right() - self.minWidth):
            return

        split_point: int = 0
        if not TEST:
            split_point = random.randint(
                self.get_Left() + self.minWidth, self.get_Right() - self.minWidth
            )
        else:
            split_point = self.get_Left() + self.get_Width() // 2

        self.left_Room = split_room(
            self.get_Left(),
            split_point,
            self.get_Top(),
            self.get_Bottom(),
            self.tile_array,
        )
        self.right_Room = split_room(
            split_point + 1,
            self.get_Right(),
            self.get_Top(),
            self.get_Bottom(),
            self.tile_array,
        )
        self.left_Room.split()
        self.right_Room.split()
        self.vertical_split = True

    def split(self) -> None:
        rand_value = random.random()

        if rand_value < 0.5 and self.get_Width() >= 2 * self.minWidth:
            self.split_vertically()
            return

        elif self.get_Height() >= 2 * self.minHeight:
            self.split_horizontally()
            return

        if self.get_Width() > self.maxWidth:
            self.split_vertically()
            return

        if self.get_Height() > self.maxHeight:
            self.split_horizontally()
            return

    def create_room(self) -> None:
        if self.is_leaf():
            self.tile_array.carve_Area(
                self.get_Left(),
                self.get_Right(),
                self.get_Top(),
                self.get_Bottom(),
                "#",
                ".",
            )
        else:
            assert self.left_Room is not None and self.right_Room is not None
            self.left_Room.create_room()
            self.right_Room.create_room()

    def shrink_room(self) -> None:
        self.left += self.shrink
        self.bottom += self.shrink
        self.right -= self.shrink
        self.top -= self.shrink

        if self.left_Room:
            self.left_Room.shrink_room()
        if self.right_Room:
            self.right_Room.shrink_room()

    def get_Right_Positions(self) -> list[int]:
        right_Connections: list[int] = []
        if not self.is_leaf():
            if self.right_Room:
                right_Connections.extend(self.right_Room.get_Right_Positions())
            if self.horizontal_split and self.left_Room:
                right_Connections.extend(self.left_Room.get_Right_Positions())
        else:
            y: int = self.get_Bottom() + self.corridor_Margin
            while y <= (self.get_Top() - self.corridor_Margin):
                right_Connections.append(y)
                y += 1
        return right_Connections

    def get_Left_Positions(self) -> list[int]:
        left_Connections: list[int] = []
        if not self.is_leaf():
            if self.right_Room:
                left_Connections.extend(self.right_Room.get_Left_Positions())
            if self.horizontal_split and self.left_Room:
                left_Connections.extend(self.left_Room.get_Left_Positions())
        else:
            y: int = self.get_Top() - self.corridor_Margin
            while y >= (self.get_Bottom() + self.corridor_Margin):
                left_Connections.append(y)
                y -= 1
        return left_Connections

    def get_Top_Positions(self) -> list[int]:
        top_Connections: list[int] = []

        if not self.is_leaf():
            if self.right_Room:
                top_Connections.extend(self.right_Room.get_Top_Positions())
            if self.vertical_split and self.left_Room:
                top_Connections.extend(self.left_Room.get_Top_Positions())
        else:
            x: int = self.get_Left() + self.corridor_Margin
            while x <= (self.get_Right() - self.corridor_Margin):
                top_Connections.append(x)
                x += 1
        return top_Connections

    def get_Bottom_Positions(self) -> list[int]:
        bottom_Connections: list[int] = []

        if not self.is_leaf():
            if self.right_Room:
                bottom_Connections.extend(self.right_Room.get_Bottom_Positions())
            if self.vertical_split and self.left_Room:
                bottom_Connections.extend(self.left_Room.get_Bottom_Positions())
        else:
            x: int = self.get_Right() - self.corridor_Margin
            while x >= (self.get_Left() + self.corridor_Margin):
                bottom_Connections.append(x)
                x -= 1
        return bottom_Connections

    def get_Intersections(self, points_A: list[int], points_B: list[int]) -> list[int]:
        intersections = sorted(set(points_A) & set(points_B))
        return intersections

    def get_Position_Intersections_Groups(self, points: list[int]) -> list[list[int]]:
        intersections: list[list[int]] = []

        first_Iter: bool = True

        current_Intersection: list[int] = [0, 0]
        num: int = 0
        for i in range(len(points)):
            num = points[i]
            if first_Iter or points[i - 1] != points[i] - 1:
                if not first_Iter:
                    intersections.append(current_Intersection)

                first_Iter = False
                current_Intersection = [num, num]
            else:
                current_Intersection[1] += 1
        if not first_Iter:
            intersections.append(current_Intersection)

        return [
            group
            for group in intersections
            if group[1] - group[0] >= self.minCorridorThickness
        ]

    def make_Corridor(self) -> None:
        if self.is_leaf():
            return

        if self.left_Room:
            self.left_Room.make_Corridor()
        if self.right_Room:
            self.right_Room.make_Corridor()

        if self.left_Room and self.right_Room:
            p: list[int] = []
            groups: list[list[int]] = [[]]
            positions: list[int] = []
            corridor: Corridor | None = None

            if self.vertical_split:
                positions = self.get_Intersections(
                    self.left_Room.get_Right_Positions(),
                    self.right_Room.get_Left_Positions(),
                )
                groups = self.get_Position_Intersections_Groups(positions)
                p = random.choice(groups)
                corridor = Corridor(
                    self.left_Room.get_Right() + 1,
                    self.left_Room.get_Right() + 2,
                    p[1],
                    p[0],
                    self.tile_array,
                    "v",
                )
            else:
                positions = self.get_Intersections(
                    self.left_Room.get_Bottom_Positions(),
                    self.right_Room.get_Top_Positions(),
                )
                groups = self.get_Position_Intersections_Groups(positions)
                p = random.choice(groups)
                corridor = Corridor(
                    p[0],
                    p[1],
                    self.left_Room.get_Bottom() - 1,
                    self.left_Room.get_Bottom() - 2,
                    self.tile_array,
                    "h",
                )
