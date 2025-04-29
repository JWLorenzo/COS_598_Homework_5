from Utility.room_gen.tilearray import tileArray


class Room:
    def __init__(
        self, x_min: int, y_min: int, x_max: int, y_max: int, tile_array: tileArray
    ) -> None:
        self.x_min: int = x_min
        self.y_min: int = y_min
        self.x_max: int = x_max
        self.y_max: int = y_max
        self.tile_array: tileArray = tile_array

    def get_width(self) -> int:
        return self.x_max - self.x_min

    def get_height(self) -> int:
        return self.y_max - self.y_min

    def get_xmin(self) -> int:
        return self.x_min

    def get_ymin(self) -> int:
        return self.y_min

    def get_xmax(self) -> int:
        return self.x_max

    def get_ymax(self) -> int:
        return self.y_max
