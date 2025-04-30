from Utility.room_gen.room import Room
from Utility.room_gen.tilearray import tileArray


class Corridor(Room):
    def __init__(
        self,
        left: int,
        right: int,
        top: int,
        bottom: int,
        tile_array: tileArray,
        direction: str,
    ) -> None:
        self.direction: str = direction
        super().__init__(left, right, top, bottom, tile_array)
        tile_array.carve_Corridor(
            self.left, self.right, self.top, self.bottom, "|", "_", self.direction
        )
