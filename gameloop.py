from display import *
from player import Player
from CONSTANTS import FPS, IMAGE_DIR, WORLD_X, WORLD_Y, TILE_SIZE
import os
from level import Level
from treenode import TreeNode
from tilearray import tileArray


def game_loop(display: Display) -> None:
    """
    SETUP
    """
    winw, winh = pygame.display.get_window_size()

    ## TODO add level maker func

    cur_level = Level(display)

    player = Player()
    player.rect.x = 0
    player.rect.y = 0

    player_list: pygame.sprite.Group = pygame.sprite.Group()
    player_list.add(player)
    tilemap: tileArray = tileArray(winw, winh)

    dungeonTree: TreeNode = TreeNode(
        [0, 0, (winw // TILE_SIZE) * TILE_SIZE, (winh // TILE_SIZE) * TILE_SIZE],
        display.screen,
        tilemap,
    )
    dungeonTree.binary_space_partition(
        0, 0, (winw // TILE_SIZE) * TILE_SIZE, (winh // TILE_SIZE) * TILE_SIZE
    )
    with open("tilemap.txt", "w") as f:
        for row in tilemap.tile_array:
            for column in row:
                f.write(column)
            f.write("\n")
    """
    MAIN LOOP
    """
    while display.run:

        # Handle user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                display.run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    display.run = False
                if event.key == pygame.K_LEFT or event.key == ord("a"):
                    player.control(-player.steps, 0)
                if event.key == pygame.K_RIGHT or event.key == ord("d"):
                    player.control(player.steps, 0)
                if event.key == pygame.K_UP or event.key == ord("w"):
                    player.control(0, -player.steps)
                if event.key == pygame.K_DOWN or event.key == ord("s"):
                    player.control(0, player.steps)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == ord("a"):
                    player.control(player.steps, 0)
                if event.key == pygame.K_RIGHT or event.key == ord("d"):
                    player.control(-player.steps, 0)
                if event.key == pygame.K_UP or event.key == ord("w"):
                    player.control(0, player.steps)
                if event.key == pygame.K_DOWN or event.key == ord("s"):
                    player.control(0, -player.steps)
        display.screen.blit(cur_level.background, (0, 0))
        # player.update()
        # player_list.draw(display.screen)
        pygame.display.flip()
        display.clock.tick(FPS)
