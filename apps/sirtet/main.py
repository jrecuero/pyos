import sys
import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame

from _game_scene_board import GameSceneBoard
from _game_scene_title import GameSceneTitle
from _game_scene_end import GameSceneEnd
from _game_handler import GameHandler


SCREEN_SIZE = (1200, 850)


def _create_game(surface):
    """_create_game creates all custom instances required for handling the
    actual game implementation.
    """
    gh = GameHandler("app", surface)
    scene_board = GameSceneBoard(surface)

    gobj_actor = gh.actor.gdisplay()
    gobj_actor.x = 450
    gobj_actor.y = 500
    scene_board.add_gobject(gobj_actor)

    scene_board.gobj_target = gh.targets[0].gdisplay()
    scene_board.gobj_target.x = 450
    scene_board.gobj_target.y = 564
    scene_board.add_gobject(scene_board.gobj_target)

    scene_title = GameSceneTitle(surface)
    scene_end = GameSceneEnd(surface)
    gh.add_scene(scene_title)
    gh.add_scene(scene_board)
    gh.add_scene(scene_end)
    gh.hscene.active(scene_title)
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
            elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                gh.handle_keyboard_event(event)
            elif event.type in [
                pygame.MOUSEMOTION,
                pygame.MOUSEBUTTONDOWN,
                pygame.MOUSEBUTTONUP,
            ]:
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
