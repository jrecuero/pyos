import sys
import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
from pyplay import GHandler, Scene, Color
from pyplay.gobject import GText

# from pyplay.gobject.grid import GridBoard, GridShape
from pyplay.gobject.xgrid import Shape, GridBoard


# class Actor(GridShape):
#     def __init__(self, x, y, matrix, gsize, **kwargs):
#         super(Actor, self).__init__("actor", x, y, matrix, gsize, **kwargs)


def main():
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption("B-GRID")
    surface = pygame.display.set_mode((600, 500))
    clock = pygame.time.Clock()
    # -> Create game handler, scenes and graphical objects.
    gh = GHandler("app", surface)
    scene = Scene("main", surface)
    board = GridBoard("board", 50, 50, 500, 400, 50, outline=1)
    # actor = Actor(0, 0, [[0, 0, 0], [1, 1, 1], [0, 0, 0]], 50, color=Color.BLUE)
    actor = Shape("actor", 0, 0, 50, 50, color=Color.GREEN)
    # board.add_gobject(actor)
    board.add_shape(actor)
    text = GText("text", 10, 460, "loading...")
    scene.add_gobject(board)
    scene.add_gobject(text)
    gh.add_scene(scene)
    gh.hscene.active()
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
        text.message = f"({actor.gridx}, {actor.gridy})"
        # <-

        # -> render objects
        surface.fill((255, 255, 255))
        gh.render()
        pygame.display.flip()
        # <-


if __name__ == "__main__":
    main()