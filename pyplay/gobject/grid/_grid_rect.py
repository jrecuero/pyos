import pygame
from ._grid_object import GridObject


class GridRect(GridObject):
    """GridRect implements a graphical object that is rendered as a rectangle
    in a grid.
    """

    def __init__(self, name, x, y, dx, dy, **kwargs):
        super(GridRect, self).__init__(name, x, y, dx, dy, **kwargs)
        pygame.draw.rect(self.image, self.color, (0, 0, self.dx, self.dy), self.outline)
