from Utility.display import *
from Game.player import Player
from Utility.CONSTANTS import (
    FPS,
    IMAGE_DIR,
    WORLD_X,
    WORLD_Y,
    TILE_SIZE,
    RUN_GAME,
    TEST,
)
import os
from Utility.level import Level
from Utility.room_gen.tilearray import tileArray
from Utility.room_gen.split_room import split_room


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
    tilemap: tileArray = tileArray(winw // TILE_SIZE, winw // TILE_SIZE)
    root: split_room = split_room(0, winw // TILE_SIZE, winw // TILE_SIZE, 0, tilemap)
    root.split()
    root.shrink_room()
    root.create_room()
    root.make_Corridor()

    if TEST:
        right_test: list[int] = root.get_Right_Positions()
        left_test: list[int] = root.get_Left_Positions()
        top_test: list[int] = root.get_Top_Positions()
        bottom_test: list[int] = root.get_Bottom_Positions()
        common_lr_test: list[int] = root.get_Intersections(right_test, left_test)
        corridor_coords_test: list[list[int]] = root.get_Position_Intersections_Groups(
            common_lr_test
        )
        print("Right", right_test)
        print("Left", left_test)

        print("common", common_lr_test),

        print("corridor coords", corridor_coords_test)

        print("Top", top_test)
        print("Bottom", bottom_test)

    with open("tilemap.txt", "w") as f:
        for row in tilemap.tile_array:
            for column in row:
                f.write(column)
            f.write("\n")
    """
    MAIN LOOP
    """
    if RUN_GAME:
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
