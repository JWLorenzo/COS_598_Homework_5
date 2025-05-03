# import random
# from Game.initialize import initialize_game
# from Game.gameloop import game_loop
from image_gen import generate_Dungeon


def main() -> None:
    # random.seed(None)
    # game_display = initialize_game()
    # game_loop(game_display)
    generate_Dungeon(60, 60)


if __name__ == "__main__":
    main()
