import pygame
from ..._gevent import GEvent
from ._grid_board import GridBoard


class GravityBoard(GridBoard):
    """GravityBoard implements a board with a timer that simulates downward
    gravity.
    """

    def __init__(self, name, x, y, dx, dy, xsize, ysize=None, **kwargs):
        super(GravityBoard, self).__init__(name, x, y, dx, dy, xsize, ysize, **kwargs)
        pygame.time.set_timer(GEvent.GRAVITY, 1000)
