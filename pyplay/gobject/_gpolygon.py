import pygame
from .._gobject import GObject


class GPolygon(GObject):
    """GPolygon implements a graphical object that is rendered as a polygon.
    """

    def __init__(self, name, x, y, points, **kwargs):
        rect = self._calculate_content(points)
        super(GPolygon, self).__init__(name, x, y, rect.w, rect.h, **kwargs)
        self.points = points
        points = [p.get() for p in self.points]
        pygame.draw.polygon(self.image, self.color, points, self.outline)

    def _calculate_content(self, points):
        """_calculate_content creates the rectangle that contains all polygon
        points.
        """
        xs = [p.x for p in points]
        ys = [p.y for p in points]
        min_x = min(xs)
        max_x = max(xs)
        min_y = min(ys)
        max_y = max(ys)
        self.dx = max_x - min_x
        self.dy = max_y - min_y
        return pygame.Rect(min_x, min_y, self.dx, self.dy)

    def __str__(self):
        return f"[{self.gid}] : {self.__class__.__name__}@{self.name} | {[str(p) for p in self.points]}"

    def bounce_x(self):
        """bounce_x bounces against an X-plane, it means y-component will
        be reversed.
        """
        result = super(GPolygon, self).bounce_x()
        self.move_inc(self.move.x, self.move.y)
        return result

    def bounce_y(self):
        """bounce_y bounces against an Y-plane, it means x-component will
        be reversed.
        """
        result = super(GPolygon, self).bounce_y()
        self.move_inc(self.move.x, self.move.y)
        return result
