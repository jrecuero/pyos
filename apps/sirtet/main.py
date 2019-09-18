import sys
import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame

# from _game_tools import (
#     CELL_SIZE,
#     XSIZE_CELLS,
#     YSIZE_CELLS,
#     YSIZE_THRESHOLD,
#     GRAVITY_TIMER,
# )
# from _game_board import GameBoard
from _game_board_scene import GameBoardScene
from _game_title_scene import GameTitleScene
from _game_handler import GameHandler


SCREEN_SIZE = (1200, 850)
# BOARD_ORIGIN = {"x": 50, "y": 50}
# BOARD_SIZE = {"dx": CELL_SIZE * XSIZE_CELLS, "dy": CELL_SIZE * YSIZE_CELLS}


def _create_game(surface):
    """_create_game creates all custom instances required for handling the
    actual game implementation.
    """
    gh = GameHandler("app", surface)
    scene = GameBoardScene(surface)
    # board = GameBoard(
    #     "gravity-board",
    #     BOARD_ORIGIN["x"],
    #     BOARD_ORIGIN["y"],
    #     BOARD_SIZE["dx"],
    #     BOARD_SIZE["dy"],
    #     CELL_SIZE,
    #     outline=1,
    #     threshold=YSIZE_THRESHOLD,
    #     gravity_timer=GRAVITY_TIMER,
    # )
    # board.next_piece()
    # scene.add_gobject(board)
    # scene.add_gobject(gh.gobj_console)
    # gh.gstat.x = 450
    # gh.gstat.y = 200
    # scene.add_gobject(gh.gstat)
    gobj_actor = gh.actor.gdisplay()
    gobj_actor.x = 450
    gobj_actor.y = 500
    scene.add_gobject(gobj_actor)

    scene.gobj_target = gh.targets[0].gdisplay()
    scene.gobj_target.x = 450
    scene.gobj_target.y = 564
    scene.add_gobject(scene.gobj_target)

    title_scene = GameTitleScene(surface)
    gh.add_scene(title_scene)
    gh.add_scene(scene)
    gh.hscene.active(title_scene)
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

    # ->
    # TODO: This should be called when a new match starts.
    gh.start_match()
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
            elif event.type == pygame.MOUSEMOTION:
                gh.handle_mouse_event(event)
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

    # ->
    # TODO: This should be called when a match ends.
    gh.end_match()
    # <-


if __name__ == "__main__":
    main()
