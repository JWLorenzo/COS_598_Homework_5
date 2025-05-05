from Utility.room_gen.tilearray import tileArray
from Utility.room_gen.room_node import Node
from PIL import Image
from Utility.room_gen.tilearray import tileArray
from Utility.CONSTANTS import TILE_SIZE


def generate_Dungeon(width: int, height: int) -> None:
    tilemap: tileArray = tileArray(width, height)
    root: Node = Node(0, width, 0, height, tilemap)
    root.create_Dungeon()
    root.carve_Dungeon()
    root.tile_array.iterative_doors()
    leaves: list[tuple[int, int]] = root.get_leaf_centers()

    path = root.tile_array.leaf_Recursion(leaves[-1], leaves[:-1])
    root.tile_array.create_Doors(path)

    with open("tilemap.txt", "w") as f:
        for row in range(len(tilemap.tile_array)):
            for column in range(len(tilemap.tile_array[row])):
                f.write(tilemap.tile_array[row][column])
            if row != len(tilemap.tile_array) - 1:
                f.write("\n")

    generate_dungeon_image(root.tile_array)


def generate_dungeon_image(tile_map: tileArray) -> None:

    tiles = {
        tile_map.north: Image.open("game_images/Dungeon_Tiles/final/WHM.jpg"),
        tile_map.south: Image.open("game_images/Dungeon_Tiles/final/WHM.jpg"),
        tile_map.floor: Image.open("game_images/Dungeon_Tiles/final/F.jpg"),
        tile_map.door: Image.open("game_images/Dungeon_Tiles/final/D.jpg"),
        tile_map.west: Image.open("game_images/Dungeon_Tiles/final/WVL.jpg"),
        tile_map.east: Image.open("game_images/Dungeon_Tiles/final/WVR.jpg"),
        tile_map.cornerbl: Image.open("game_images/Dungeon_Tiles/final/PL.jpg"),
        tile_map.cornerbr: Image.open("game_images/Dungeon_Tiles/final/PR.jpg"),
        tile_map.cornertr: Image.open("game_images/Dungeon_Tiles/final/WCR.jpg"),
        tile_map.cornertl: Image.open("game_images/Dungeon_Tiles/final/WCL.jpg"),
    }

    width, height = tiles[tile_map.north].size
    image = Image.new(
        "RGBA", (tile_map.map_width * width, tile_map.map_height * height)
    )
    for row in range(tile_map.map_height):
        for column in range(tile_map.map_width):
            tile = tiles[tile_map.tile_array[row][column]]
            image.paste(tile, (column * width, row * height))
    image.save("dungeon_image.png")
