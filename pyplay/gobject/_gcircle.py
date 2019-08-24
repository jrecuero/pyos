import pygame
from .._point import Point
from .._gobject import GObject


class GCircle(GObject):
    """GCircle implements a graphical object that is rendered as a circle.
    """

    def __init__(self, name, x, y, radius, **kwargs):
        super(GCircle, self).__init__(name, pos=Point(x, y), **kwargs)
        self.radius = radius
        self.set_content(
            pygame.Rect(self.x, self.y, self.radius * 2, self.radius * 2),
            GObject.CIRCLE,
        )

    def __str__(self):
        center = Point(self.x + self.radius, self.y + self.radius)
        return f"[{self.gid}] : {self.__class__.__name__}@{self.name} | {self.ctype} {center}, {self.radius}"

    def bounds(self):
        """bounds should returns a rectangle that contains the whole
        graphical object.
        """
        return self.content

    def update(self, surface, **kwargs):
        super(GCircle, self).update(surface, **kwargs)
        self.content.x = self.x
        self.content.y = self.y

    def render(self, surface, **kwargs):
        center = Point(self.content.x + self.radius, self.content.y + self.radius)
        pygame.draw.circle(surface, self.color, center.get(), self.radius, self.outline)
