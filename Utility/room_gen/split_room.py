from Utility.room_gen.room import Room
import random
from Utility.room_gen.tilearray import tileArray


class split_room(Room):
    def __init__(
        self, x_min: int, y_min: int, x_max: int, y_max: int, tile_array: tileArray
    ) -> None:
        self.width_min: int = 8
        self.width_max: int = 20
        self.height_min: int = 8
        self.height_max: int = 20
        self.corridor_width: int = 2
        self.horizontal_split: bool = False
        self.vertical_split: bool = False
        self.left: split_room | None = None
        self.right: split_room | None = None
        self.shrink: int = 1
        super().__init__(x_min, y_min, x_max, y_max, tile_array)

        if self.get_width() < self.width_min or self.get_height() < self.height_min:
            print(
                f"Room too small ({self.get_width()}, {self.get_height()}) to split. "
                f"Width min: {self.width_min}, Height min: {self.height_min}"
            )

    def is_leaf(self) -> bool:
        return not self.horizontal_split and not self.vertical_split

    def split_horizontally(self) -> None:
        if self.y_min + self.height_min >= self.y_max - self.height_min:
            return

        split_point = random.randint(
            self.y_min + self.height_min, self.y_max - self.height_min
        )

        self.left = split_room(
            self.x_min, self.y_min, self.x_max, split_point, self.tile_array
        )

        self.right = split_room(
            self.x_min, split_point, self.x_max, self.y_max, self.tile_array
        )
        self.left.split()
        self.right.split()
        self.horizontal_split = True

    def split_vertically(self) -> None:
        if self.x_min + self.width_min >= self.x_max - self.width_min:
            return
        split_point = random.randint(
            self.x_min + self.width_min, self.x_max - self.width_min
        )
        self.left = split_room(
            self.x_min, self.y_min, split_point, self.y_max, self.tile_array
        )
        self.right = split_room(
            split_point, self.y_min, self.x_max, self.y_max, self.tile_array
        )
        self.left.split()
        self.right.split()
        self.vertical_split = True

    def create_room(self) -> None:
        if self.is_leaf():
            self.tile_array.carve_Area(
                self.x_min, self.y_min, self.x_max, self.y_max, "#", "."
            )
            return
        else:
            self.left.create_room()
            self.right.create_room()
            return

    def split(self) -> None:
        rand_value = random.random()

        if rand_value < 0.5 and self.get_width() >= 2 * self.width_min:
            self.split_horizontally()
            return
        elif self.get_height() >= 2 * self.height_min:
            self.split_vertically()
            return

        if self.get_height() > self.height_max:
            self.split_horizontally()
            return

        if self.get_width() > self.width_max:
            self.split_vertically()
            return

    def shrink_room(self) -> None:
        self.x_min += self.shrink
        self.y_min += self.shrink
        self.x_max -= self.shrink
        self.y_max -= self.shrink

        if self.left:
            self.left.shrink_room()
        if self.right:
            self.right.shrink_room()
        return
