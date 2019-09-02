import random
import pygame
from pyplay import Color, GObject, GEvent
from pyplay.gobject.grid import GravityBoard, TriShape

pieces = []
pieces.append({"piece": [[0, 1, 1], [0, 1, 0], [0, 1, 0]], "rotation": True})
pieces.append({"piece": [[1, 1, 0], [0, 1, 0], [0, 1, 0]], "rotation": True})
pieces.append({"piece": [[0, 1, 0], [0, 1, 0], [0, 1, 0]], "rotation": True})
pieces.append({"piece": [[1, 1, 0], [0, 1, 1], [0, 0, 0]], "rotation": True})
pieces.append({"piece": [[0, 0, 0], [0, 1, 1], [1, 1, 0]], "rotation": True})
pieces.append({"piece": [[1, 1, 0], [1, 1, 0], [0, 0, 0]], "rotation": False})
pieces.append({"piece": [[0, 0, 0], [1, 1, 1], [0, 1, 0]], "rotation": True})

colors = [Color.BLACK, Color.BLUE, Color.GREEN, Color.RED]


def new_piece():
    """next_piece generates the next piece to be placed in the board.
    """
    return random.choice(pieces)


def next_color():
    """next_color picks randomly the next color for the next piece.
    """
    return random.choice(colors)


def next_piece():
    """next_actor generates the next actor with random piece and color.
    """
    next_one = new_piece()
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
        self.the_next_piece = None

    def next_piece(self):
        """next_piece adds a new actor/piece to the board.
        """
        if self.the_next_piece:
            self.add_gobject(self.the_next_piece)
        else:
            self.add_gobject(next_piece())
        self.the_next_piece = next_piece()
        next_piece_event = pygame.event.Event(
            GEvent.ENGINE, subtype=GEvent.NEXT, source=self.get_next_piece_at()
        )
        pygame.event.post(next_piece_event)

    def get_next_piece_at(self, x=0, y=0):
        sprite = GObject("next", x, y, 150, 150)
        pygame.draw.rect(sprite.image, Color.BLACK, (0, 0, 150, 150), 1)
        for cell in self.the_next_piece.cells:
            x = (cell.x - 4) * cell.dx
            y = cell.y * cell.dy
            pygame.draw.rect(sprite.image, cell.color, (x, y, cell.dx, cell.dy))
        return sprite

    def handle_keyboard_event(self, event):
        """handle_keyboard_event should process the keyboard event given.
        """
        if event.key == pygame.K_p:
            pygame.time.set_timer(GEvent.T_GRAVITY, self.pause_timer)
            if self.pause_timer:
                self.pause_timer = 0
                pause_event = pygame.event.Event(
                    GEvent.ENGINE, subtype=GEvent.PAUSE, source=False
                )
                self.running = True
            else:
                self.pause_timer = self.gravity_timer
                pause_event = pygame.event.Event(
                    GEvent.ENGINE, subtype=GEvent.PAUSE, source=True
                )
                self.running = False
            pygame.event.post(pause_event)
        super(GameBoard, self).handle_keyboard_event(event)

    def handle_custom_event(self, event):
        """handle_custom_event should process pygame custom event given.
        Any object in the game, like, scene, graphic objects, ... can post
        customs events, and those should be handled at this time.
        """
        # First we have to handle the event before calling the super, because
        # some object could be added or created at this time.
        if event.type == GEvent.ENGINE and event.subtype == GEvent.CREATE:
            # self.add_gobject(next_piece())
            self.next_piece()
        elif event.type == GEvent.ENGINE and event.subtype == GEvent.DELETE:
            pass
        super(GameBoard, self).handle_custom_event(event)