import pygame
from .._gobject import GObject


class GPolygon(GObject):
    """GPolygon implements a graphical object that is rendered as a polygon.
    """

    def __init__(self, name, points, **kwargs):
        super(GPolygon, self).__init__(name, pos=points[0], **kwargs)
        self.points = points
        self.set_content(self._calculate_content(self.points), GObject.POLYGON)

    def _calculate_content(self, points):
        """_calculate_content creates the rectangle that contains all polygon
        points.
        """
        xs = [p.x for p in points]
        ys = [p.y for p in points]
        self.x = xs[0]
        self.y = ys[0]
        min_x = min(xs)
        max_x = max(xs)
        min_y = min(ys)
        max_y = max(ys)
        self.dx = max_x - min_x
        self.dy = max_y - min_y
        return pygame.Rect(min_x, min_y, self.dx, self.dy)

    def __str__(self):
        return f"[{self.gid}] : {self.__class__.__name__}@{self.name} | {self.points}"

    def bounds(self):
        """bounds should returns a rectangle that contains the whole
        graphical object.
        """
        return self.content

    def move_inc(self, inc_x, inc_y):
        """move_inc moves the grafical object by the given x and y components.
        """
        for p in self.points:
            p.x += int(inc_x)
            p.y += int(inc_y)
        self.content = self._calculate_content(self.points)

    def move_to(self, x, y):
        """move_to moves the grafical object to the given position.
        """
        dx = self.x - x
        dy = self.y - y
        for p in self.points:
            p.x += dx
            p.y += dy
        self.content = self._calculate_content(self.points)

    def scale(self, dx=None, dy=None):
        for p in self.points[1:]:
            if dx:
                p.x = self.x + int(((p.x - self.x) * dx) / 100)
            if dy:
                p.y = self.y + int(((p.y - self.y) * dy) / 100)
        self.content = self._calculate_content(self.points)

    def update(self, surface, **kwargs):
        for p in self.points:
            p.x += int(self.move.x)
            p.y += int(self.move.y)
        self.content = self._calculate_content(self.points)

    def render(self, surface, **kwargs):
        points = [p.get() for p in self.points]
        pygame.draw.polygon(surface, self.color, points, self.outline)
