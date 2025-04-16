from display import *


def game_loop(display: Display) -> None:
    winw, winh = pygame.display.get_window_size()
    background = pygame.Surface((winw, winh))
    background.fill("white")

    while display.run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                display.run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    display.run = False
