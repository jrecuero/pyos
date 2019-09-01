import sys
import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
from _game_board import GameBoard
from _game_scene import GameScene
from _game_handler import GameHandler


SCREEN_SIZE = (1200, 850)
BOARD_ORIGIN = {"x": 50, "y": 50}
BOARD_SIZE = {"dx": 450, "dy": 700}
CSIZE = 50


def _create_game(surface):
    """_create_game creates all custom instances required for handling the
    actual game implementation.
    """
    gh = GameHandler("app", surface)
    scene = GameScene(surface)
    board = GameBoard(
        "gravity-board",
        BOARD_ORIGIN["x"],
        BOARD_ORIGIN["y"],
        BOARD_SIZE["dx"],
        BOARD_SIZE["dy"],
        CSIZE,
        outline=1,
        gravity_timer=500,
    )
    board.next_piece()
    scene.add_gobject(board)
    # scene.next_piece = board.get_next_piece_at(550, 50)
    # scene.add_gobject(scene.next_piece)
    scene.add_gobject(gh.console)
    scene.add_gobject(gh.gstat.gtext_total_lines)
    # scene.add_gobject(gh.actor.gtext)
    for gtext in gh.gstat.gtext_colors.values():
        scene.add_gobject(gtext)
    gh.add_scene(scene)
    gh.hscene.active()
    return gh


def main():
    """main implements the full game application.
    """
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption("SIRTET")
    surface = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()
    # -> Create game handler, scenes and graphical objects.
    gh = _create_game(surface)
    # <-
    while True:
        clock.tick(30)
        gh.start_tick()
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
        gh.end_tick()


if __name__ == "__main__":
    main()
