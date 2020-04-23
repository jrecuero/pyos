from ._point import Point
from ._size import Size


class Rect:
    """Class Rect identifies coordinates and handling fro any 2-dimensional
    rectangle.
    """

    def __init__(self, x, y, dx, dy, z=0):
        self.origin = Point(x, y)
        self.size = Size(dx, dy)
        self.z = z

    @property
    def center(self):
        return Point(self.origin.x + self.size.halfx, self.origin.y + self.size.halfx)

    @property
    def coordinates(self):
        return [Point(self.origin.x, self.origin.y),
                Point(self.origin.x + self.size.x, self.origin.y),
                Point(self.origin.x, self.origin.y + self.size.y),
                Point(self.origin.x + self.size.x, self.origin.y + self.size.y)]

    def __eq__(self, other):
        """__eq__ overloads logical equal operation for Rect instances.
        """
        return (self.origin == other.origin) and (self.size == other.size)

    def __ne__(self, other):
        """__ne__ overloads logical not equal operation for Rect instances.
        """
        return (self.origin != other.origin) or (self.size != other.size)
