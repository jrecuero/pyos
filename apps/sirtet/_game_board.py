import random
import pygame
from pyplay import Color
from pyplay.gobject.grid import GravityBoard, GridEvent, TriShape

pieces = []
pieces.append({"piece": [[0, 1, 1], [0, 1, 0], [0, 1, 0]], "rotation": True})
pieces.append({"piece": [[1, 1, 0], [0, 1, 0], [0, 1, 0]], "rotation": True})
pieces.append({"piece": [[0, 1, 0], [0, 1, 0], [0, 1, 0]], "rotation": True})
pieces.append({"piece": [[1, 1, 0], [0, 1, 1], [0, 0, 0]], "rotation": True})
pieces.append({"piece": [[0, 0, 0], [0, 1, 1], [1, 1, 0]], "rotation": True})
pieces.append({"piece": [[1, 1, 0], [1, 1, 0], [0, 0, 0]], "rotation": False})
pieces.append({"piece": [[0, 0, 0], [1, 1, 1], [0, 1, 0]], "rotation": True})

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
    next_one = next_piece()
    return TriShape(
        "actor",
        4,
        0,
        next_one["piece"],
        50,
        50,
        color=next_color(),
        rotation=next_one["rotation"],
    )


class GameBoard(GravityBoard):
    """GameBoard implements all custom functionality for the game board being
    played.
    """

    def __init__(self, name, x, y, dx, dy, xsize, ysize=None, **kwargs):
        super(GameBoard, self).__init__(name, x, y, dx, dy, xsize, ysize, **kwargs)
        self.pause_timer = 0

    def next_actor(self):
        """next_actor adds a new actor to the board.
        """
        self.add_gobject(next_actor())

    def handle_keyboard_event(self, event):
        """handle_keyboard_event should process the keyboard event given.
        """
        if event.key == pygame.K_p:
            pygame.time.set_timer(GridEvent.GRAVITY, self.pause_timer)
            if self.pause_timer:
                self.pause_timer = 0
                pause_event = pygame.event.Event(GridEvent.PAUSE, source=False)
                self.running = True
            else:
                self.pause_timer = self.gravity_timer
                pause_event = pygame.event.Event(GridEvent.PAUSE, source=True)
                self.running = False
            pygame.event.post(pause_event)
        super(GravityBoard, self).handle_keyboard_event(event)

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
