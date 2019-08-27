import sys
import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
from pyplay import GHandler, Scene, Color
from pyplay.gobject import GText

# from pyplay.gobject.grid import GridBoard, GridShape
from pyplay.gobject.xgrid import Cell, Shape, GravityBoard


# class Actor(GridShape):
#     def __init__(self, x, y, matrix, gsize, **kwargs):
#         super(Actor, self).__init__("actor", x, y, matrix, gsize, **kwargs)


def _create_game(surface):
    gh = GHandler("app", surface)
    scene = Scene("main", surface)
    board = GravityBoard("gravity-board", 50, 50, 450, 600, 50, outline=1)
    # actor = Actor(0, 0, [[0, 0, 0], [1, 1, 1], [0, 0, 0]], 50, color=Color.BLUE)
    actor = Shape("actor")
    actor.add_cell(Cell("cell-actor", 0, 0, 50, 50, color=Color.GREEN))
    actor.add_cell(Cell("cell-actor", 1, 1, 50, 50, color=Color.GREEN))
    actor.add_cell(Cell("cell-actor", 2, 2, 50, 50, color=Color.GREEN))
    board.add_gobject(actor)
    text = GText("text", 10, 660, "loading...")
    scene.add_gobject(board)
    scene.add_gobject(text)
    gh.add_scene(scene)
    gh.hscene.active()
    return gh


def main():
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption("B-GRID")
    surface = pygame.display.set_mode((550, 700))
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
        # text.message = f"({actor.gridx}, {actor.gridy})"
        # <-

        # -> render objects
        surface.fill((255, 255, 255))
        gh.render()
        pygame.display.flip()
        # <-


if __name__ == "__main__":
    main()
