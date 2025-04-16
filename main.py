import random
from initialize import initialize_game
from gameloop import game_loop


def main() -> None:
    random.seed(None)
    game_display = initialize_game()
    game_loop(game_display)


if __name__ == "__main__":
    main()
