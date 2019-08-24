import pygame
from .._point import Point
from .._gobject import GObject


class GRect(GObject):
    """GRect implements a graphical object that is rendered as a rectangle.
    """

    def __init__(self, name, x, y, dx, dy, **kwargs):
        super(GRect, self).__init__(name, pos=Point(x, y), **kwargs)
        self.dx = dx
        self.dy = dy
        self.set_content(pygame.Rect(self.x, self.y, self.dx, self.dy), GObject.RECT)

    def __str__(self):
        return f"[{self.gid}] : {self.__class__.__name__}@{self.name} | ({self.x}, {self.y}) ({self.dx}, {self.dy})"

    def bounds(self):
        """bounds should returns a rectangle that contains the whole
        graphical object.
        """
        return self.content

    def update(self, surface, **kwargs):
        super(GRect, self).update(surface, **kwargs)
        self.content.x = self.x
        self.content.y = self.y

    def render(self, surface, **kwargs):
        pygame.draw.rect(surface, self.color, self.content, self.outline)
