import pygame
from .._gobject import GObject


class GInput(GObject):
    """GInput implements a graphical object that allows text input.
    """

    def __init__(self, name, x, y, dx, dy, **kwargs):
        super(GInput, self).__init__(name, x, y, dx, dy, **kwargs)
        # in_focus attributes is used to indicate when the widget has to accept
        # user keyboard inputs.
        self.in_focus = False
        pygame.draw.rect(self.image, self.color, (0, 0, self.dx, self.dy), self.outline)

    def __str__(self):
        return f"[{self.gid}] : {self.__class__.__name__}@{self.name} | ({self.x}, {self.y}) ({self.dx}, {self.dy})"
