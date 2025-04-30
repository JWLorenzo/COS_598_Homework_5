from Utility.room_gen.room import Room
from Utility.room_gen.tilearray import tileArray


class Corridor(Room):
    def __init__(
        self, left: int, bottom: int, right: int, top: int, tile_array: tileArray
    ) -> None:
        super().__init__(left, bottom, right, top, tile_array)
