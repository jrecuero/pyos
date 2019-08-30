import sys
import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
from pyplay import Scene
from pyplay.gobject import GText
from _game_board import GameBoard
from _game_handler import GameHandler


def _create_game(surface):
    """_create_game creates all custom instances required for handling the
    actual game implementation.
    """
    gh = GameHandler("app", surface)
    scene = Scene("main", surface)
    board = GameBoard(
        "gravity-board", 50, 50, 450, 700, 50, outline=1, gravity_timer=1000
    )
    board.next_actor()
    gh.console = GText("console", 10, 760, " " * 50)
    scene.add_gobject(board)
    scene.add_gobject(gh.console)
    gh.add_scene(scene)
    gh.hscene.active()
    return gh


def main():
    """main implements the full game application.
    """
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption("SIRTET")
    surface = pygame.display.set_mode((550, 800))
    clock = pygame.time.Clock()
    # -> Create game handler, scenes and graphical objects.
    gh = _create_game(surface)
    # <-
    while True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                gh.handle_keyboard_event(event)
            elif event.type >= pygame.USEREVENT:
                gh.handle_custom_event(event)

        # -> update objects
        gh.update()
        # <-

        # -> render objects
        surface.fill((255, 255, 255))
        gh.render()
        pygame.display.flip()
        # <-


if __name__ == "__main__":
    main()
