from Utility.room_gen.tilearray import tileArray


class Room:
    def __init__(
        self, left: int, bottom: int, right: int, top: int, tile_array: tileArray
    ) -> None:
        self.left: int = left
        self.bottom: int = bottom
        self.right: int = right
        self.top: int = top
        self.tile_array: tileArray = tile_array
        self.corridor_Width: int = 2
        self.corridor_Margin: int = 1
        self.shrink: int = 1
        self.minCorridorThickness: int = 2

    def get_Width(self) -> int:
        return self.right - self.left + 1

    def get_Height(self) -> int:
        return self.top - self.bottom + 1

    def get_Left(self) -> int:
        return self.left

    def get_Bottom(self) -> int:
        return self.bottom

    def get_Right(self) -> int:
        return self.right

    def get_Top(self) -> int:
        return self.top
