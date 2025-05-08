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
    path = list(set(root.tile_array.leaf_Recursion(leaves[-1], leaves[:-1])))

    root.tile_array.create_Doors(path)
    # for i in path:
    #     root.tile_array.tile_array[i[1]][i[0]] = root.tile_array.door
    root.tile_array.clean_Walls()
    root.tile_array.mesh_walls()
    root.tile_array.create_inner_Corners()
    root.tile_array.clean_Doors()

    # root.tile_array.cleanup_Dungeon()
    with open("tilemap.txt", "w") as f:
        for row in range(len(tilemap.tile_array)):
            for column in range(len(tilemap.tile_array[row])):
                f.write(tilemap.tile_array[row][column])
            if row != len(tilemap.tile_array) - 1:
                f.write("\n")

    generate_dungeon_image(root.tile_array)


def generate_dungeon_image(tile_map: tileArray) -> None:

    tiles = {
        tile_map.wall_North: Image.open(
            "game_images/Dungeon_Tiles/final/Wall_Horizontal_Middle.jpg"
        ),
        tile_map.wall_South: Image.open(
            "game_images/Dungeon_Tiles/final/Wall_Horizontal_Middle.jpg"
        ),
        tile_map.wall_West: Image.open(
            "game_images/Dungeon_Tiles/final/Wall_Vertical_Left.jpg"
        ),
        tile_map.wall_East: Image.open(
            "game_images/Dungeon_Tiles/final/Wall_Vertical_Right.jpg"
        ),
        tile_map.wall_hR: Image.open(
            "game_images/Dungeon_Tiles/final/Wall_Horizontal_Right.jpg"
        ),
        tile_map.wall_hL: Image.open(
            "game_images/Dungeon_Tiles/final/Wall_Horizontal_Left.jpg"
        ),
        tile_map.cornerbl: Image.open(
            "game_images/Dungeon_Tiles/final/Corner_Left.jpg"
        ),
        tile_map.cornerbr: Image.open(
            "game_images/Dungeon_Tiles/final/Corner_Right.jpg"
        ),
        # tile_map.cornertr: Image.open(
        #     "game_images/Dungeon_Tiles/final/Wall_Vertical_Right.jpg"
        # ),
        # tile_map.cornertl: Image.open(
        #     "game_images/Dungeon_Tiles/final/Wall_Vertical_Left.jpg"
        # ),
        tile_map.floor: Image.open("game_images/Dungeon_Tiles/final/Floor.jpg"),
        tile_map.wall_CornerR: Image.open(
            "game_images/Dungeon_Tiles/final/Wall_Corner_Inner_Right.jpg"
        ),
        tile_map.wall_CornerL: Image.open(
            "game_images/Dungeon_Tiles/final/Wall_Corner_Inner_Left.jpg"
        ),
        tile_map.locked: Image.open("game_images/Dungeon_Tiles/final/Door_Locked.jpg"),
        tile_map.door: Image.open("game_images/Dungeon_Tiles/final/Door.jpg"),
    }

    width, height = tiles[tile_map.wall_North].size
    image = Image.new(
        "RGBA", (tile_map.map_width * width, tile_map.map_height * height)
    )
    for row in range(tile_map.map_height):
        for column in range(tile_map.map_width):
            tile = tiles[tile_map.tile_array[row][column]]
            image.paste(tile, (column * width, row * height))
    image.save("dungeon_image.png")
