import pygame
from .._point import Point
from .._gobject import GObject


class GCircle(GObject):
    """GCircle implements a graphical object that is rendered as a circle.
    """

    def __init__(self, name, x, y, radius, **kwargs):
        super(GCircle, self).__init__(name, x, y, radius * 2, radius * 2, **kwargs)
        self.radius = radius
        center = Point(self.radius, self.radius)
        pygame.draw.circle(
            self.image, self.color, center.get(), self.radius, self.outline
        )

    def __str__(self):
        center = Point(self.x + self.radius, self.y + self.radius)
        return f"[{self.gid}] : {self.__class__.__name__}@{self.name} | {self.ctype} {center}, {self.radius}"
