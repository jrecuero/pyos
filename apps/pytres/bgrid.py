import sys
import os
import random

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
from pyplay import GHandler, Scene, Color
from pyplay.gobject import GText

# from pyplay.gobject.grid import GridBoard, GridShape
from pyplay.gobject.xgrid import TriShape, GravityBoard, GridEvent


pieces = []
pieces.append([[1, 1, 0], [1, 0, 0], [1, 0, 0]])
pieces.append([[1, 0, 0], [1, 0, 0], [1, 1, 0]])
pieces.append([[0, 1, 0], [0, 1, 0], [0, 1, 0]])
pieces.append([[1, 1, 0], [0, 1, 1], [0, 0, 0]])
pieces.append([[0, 0, 0], [0, 1, 1], [1, 1, 0]])
pieces.append([[1, 1, 0], [1, 1, 0], [0, 0, 0]])
pieces.append([[1, 1, 1], [0, 1, 0], [0, 0, 0]])

colors = [Color.BLACK, Color.BLUE, Color.GREEN, Color.RED]


def next_piece():
    """next_piece generates the next piece to be placed in the board.
    """
    return random.choice(pieces)


def next_color():
    """next_color picks randomly the next color for the next piece.
    """
    return random.choice(colors)


def next_actor():
    """next_actor generates the next actor with random piece and color.
    """
    return TriShape("actor", 4, 0, next_piece(), 50, 50, color=next_color())


# class Actor(GridShape):
#     def __init__(self, x, y, matrix, gsize, **kwargs):
#         super(Actor, self).__init__("actor", x, y, matrix, gsize, **kwargs)


class GameBoard(GravityBoard):
    """GameBoard implements all custom functionality for the game board being
    played.
    """

    # def __init__(self, name, x, y, dx, dy, xsize, ysize=None, **kwargs):
    #     super(GameBoard, self).__init__(name, x, y, dx, dy, xsize, ysize, **kwargs)

    def handle_custom_event(self, event):
        """handle_custom_event should process pygame custom event given.
        Any object in the game, like, scene, graphic objects, ... can post
        customs events, and those should be handled at this time.
        """
        # First we have to handle the event before calling the super, because
        # some object could be added or created at this time.
        if event.type == GridEvent.CREATE:
            self.add_gobject(next_actor())
        elif event.type == GridEvent.DELETE:
            pass
        super(GameBoard, self).handle_custom_event(event)


class GameHandler(GHandler):
    """GameHandler implements all custom functionality for the actual game.
    """

    def handle_custom_event(self, event):
        """handle_custom_event should process pygame custom event given.
        Any object in the game, like, scene, graphic objects, ... can post
        customs events, and those should be handled at this time.
        """
        if event.type == GridEvent.COMPLETED:
            print(f"Line completed {event.source}")
            gh.console.message = f"{event.source}"
        super(GameHandler, self).handle_custom_event(event)


def _create_game(surface):
    """_create_game creates all custom instances required for handling the
    actual game implementation.
    """
    gh = GameHandler("app", surface)
    scene = Scene("main", surface)
    board = GameBoard("gravity-board", 50, 50, 450, 600, 50, outline=1)
    board.add_gobject(next_actor())
    gh.console = GText("text", 10, 660, "*" * 50)
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
