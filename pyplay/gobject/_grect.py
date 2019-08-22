import pygame
from .._color import Color
from .._point import Point
from .._gobject import GObject


class GRect(GObject):
    """GRect implements a graphical object that is rendered as a rectangle.
    """

    def __init__(self, name, x, y, dx, dy, **kwargs):
        super(GRect, self).__init__(name, pos=Point(x, y), **kwargs)
        self.dx = dx
        self.dy = dy
        self.color = kwargs.get("color", Color.BLACK)
        self.outline = kwargs.get("outline", 0)
        self.set_content(pygame.Rect(self.x, self.y, self.dx.self.dy), GObject.RECT)

    def bounds(self):
        """bounds should returns a rectangle that contains the whole
        graphical object.
        """
        return self.content

    def render(self, surface, **kwargs):
        pygame.draw.rect(surface, self.color, self.content, width=self.outline)
