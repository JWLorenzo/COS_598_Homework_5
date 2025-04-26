from CONSTANTS import *
import random
from display import Display
import pygame

from tilearray import tileArray

ROOM_WIDTH: int = 128
ROOM_HEIGHT: int = 128
MAGIC_NUMBER: float = (0.05) * ROOM_WIDTH * ROOM_HEIGHT


class TreeNode:
    def __init__(
        self, data: list[int], display: pygame.Surface, tilemap: tileArray
    ) -> None:
        self.x: int = data[0]
        self.y: int = data[1]
        self.width: int = data[2]
        self.height: int = data[3]
        self.left: TreeNode | None = None
        self.right: TreeNode | None = None
        self.rooms: list[list[int]] = []
        self.screen: pygame.Surface = display
        self.tilemap: tileArray = tilemap

    def binary_space_partition(self, x: int, y: int, w: int, h: int) -> None:
        # Base Case
        if w <= MAGIC_NUMBER and h <= MAGIC_NUMBER:

            if w < ROOM_WIDTH or h < ROOM_HEIGHT:
                return
            # room_max_width = max(w - TILE_SIZE, ROOM_WIDTH)
            # room_max_height = max(h - TILE_SIZE, ROOM_HEIGHT)

            # room_w = random.randint(ROOM_WIDTH, room_max_width)
            # room_h = random.randint(ROOM_HEIGHT, room_max_height)

            # room_w = max((room_w // TILE_SIZE) * TILE_SIZE, ROOM_WIDTH)
            # room_h = max((room_h // TILE_SIZE) * TILE_SIZE, ROOM_HEIGHT)

            # room_x = random.randint(x, x + w - room_w)
            # room_y = random.randint(y, y + h - room_h)

            # room_x = (room_x // TILE_SIZE) * TILE_SIZE
            # room_y = (room_y // TILE_SIZE) * TILE_SIZE

            # # room_x = max(room_x, ROOM_WIDTH)
            # # room_y = max(room_y, ROOM_HEIGHT)

            # self.rooms.append([room_x, room_y, room_w, room_h])
            # print(
            #     f"Drawing room at ({room_x}, {room_y}) with size ({room_w}, {room_h})"
            # )
            # pygame.draw.rect(self.screen, "blue", (room_x, room_y, room_w, room_h))
            # pygame.draw.rect(self.screen, "white", (room_x, room_y, room_w, room_h), 2)
            # pygame.draw.rect(self.screen, "red", (x, y, w, h), 2)
            self.tilemap.carve_Area(x, y, w, h, "|", " ")

            return
        if w > MAGIC_NUMBER or h > MAGIC_NUMBER:
            if w > MAGIC_NUMBER:
                # if w - ROOM_WIDTH < ROOM_WIDTH:
                #     return
                # else:
                width_split = (
                    random.randint(ROOM_WIDTH, w - ROOM_WIDTH) // TILE_SIZE
                ) * TILE_SIZE

                self.left = TreeNode([x, y, width_split, h], self.screen, self.tilemap)
                self.right = TreeNode(
                    [x + width_split, y, w - width_split, h], self.screen, self.tilemap
                )
                self.left.binary_space_partition(x, y, width_split, h)
                self.right.binary_space_partition(
                    x + width_split, y, w - width_split, h
                )
            else:
                # if w - ROOM_HEIGHT < ROOM_HEIGHT:
                #     return
                # else:
                height_split = (
                    random.randint(ROOM_HEIGHT, h - ROOM_HEIGHT) // TILE_SIZE
                ) * TILE_SIZE
                self.left = TreeNode([x, y, w, height_split], self.screen, self.tilemap)
                self.right = TreeNode(
                    [x, y + height_split, w, h - height_split],
                    self.screen,
                    self.tilemap,
                )
                self.left.binary_space_partition(x, y, w, height_split)
                self.right.binary_space_partition(
                    x, y + height_split, w, h - height_split
                )
        return


# def pre_order_traversal(node):
#     if node is None:
#         return
#     print(node.data)
#     for child in node.children:
#         pre_order_traversal(child)


# def depth_first_search(node, target):
#     if node is None:
#         return False
#     if node.data == target:
#         return True
#     for child in node.children:
#         if depth_first_search(child, target):
#             return True
#     return False


# def insert_node(root, node):
#     if root is None:
#         root = node
#     else:
#         root.add_child(node)


# def delete_node(root, target):
#     if root is None:
#         return None
#     root.children = [child for child in root.children if child.data != target]
#     for child in root.children:
#         delete_node(child, target)


# def tree_height(node):
#     if node is None:
#         return 0
#     if not node.children:
#         return 1
#     return 1 + max(tree_height(child) for child in node.children)
