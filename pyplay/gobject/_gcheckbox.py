import pygame
from .._gobject import GObject


class GCheckBox(GObject):
    """GCheckBox implements a graphical object for a check box.
    """

    def __init__(self, name, x, y, dx, dy, **kwargs):
        super(GCheckBox, self).__init__(name, x, y, dx, dy, **kwargs)
        pygame.draw.rect(self.image, self.color, (0, 0, self.dx, self.dy), self.outline)

    def __str__(self):
        return f"[{self.gid}] : {self.__class__.__name__}@{self.name} | ({self.x}, {self.y}) ({self.dx}, {self.dy})"
