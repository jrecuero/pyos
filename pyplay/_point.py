class Point:
    """Class Point identifies coordinates and handling for any 2-dimensional
    object.
    """

    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def get(self):
        """get returns X and Y attributes as a tuple.
        """
        return (self.x, self.y)

    def zget(self):
        """zget returns Z attribute.
        """
        return (self.x, self.y, self.z)

    def set(self, x=None, y=None, z=None):
        """set allows to set any X, Y or Z attribute.
        """
        self.x = self.x if x is None else x
        self.y = self.y if y is None else y
        self.z = self.z if z is None else z

    def incr(self, x=None, y=None, z=None):
        """incr allows to increase the value for any X, Y or Z attribute.
        """
        self.x = self.x if x is None else (self.x + x)
        self.y = self.y if y is None else (self.y + y)
        self.z = self.z if z is None else (self.z + z)

    def decr(self, x=None, y=None, z=None):
        """decr allows to decrease the value for any X, Y or Z attribute.
        """
        self.x = self.x if x is None else (self.x - x)
        self.y = self.y if y is None else (self.y - y)
        self.z = self.z if z is None else (self.z - z)

    def clone(self):
        """clone clones the instance to a brand new Point instance with same
        values for all attributes.
        """
        return Point(self.x, self.y, self.z)

    def __add__(self, other):
        """__add__ overloads mathematical add operation for Point instances.
        """
        p = Point(self.x, self.y, self.z)
        if isinstance(other, int):
            p = Point(self.x + other, self.y + other, self.z)
        elif isinstance(other, Point):
            p = Point(self.x + other.x, self.y + other.y, self.z + other.z)
        return p

    def __sub__(self, other):
        """__sub__ overloads mathematical subtract operation for Point
        instances.
        """
        p = Point(self.x, self.y)
        if isinstance(other, int):
            p = Point(self.x - other, self.y - other, self.z)
        elif isinstance(other, Point):
            p = Point(self.x - other.x, self.y - other.y, self.z - other.z)
        return p

    def __mul__(self, other):
        """__mul__ overloads mathematical multiple operation for Point
        instances.
        """
        p = Point(self.x, self.y)
        if isinstance(other, int):
            p = Point(self.x * other, self.y * other, self.z)
        elif isinstance(other, Point):
            p = Point(self.x * other.x, self.y * other.y, self.z)
        return p

    def __eq__(self, other):
        """__eq__ overloads logical equal operation for Point instances.
        """
        return (self.x == other.x) and (self.y == other.y) and (self.z == other.z)

    def __ne__(self, other):
        """__ne__ overloads logical not equal operation for Point instances.
        """
        return (self.x != other.x) or (self.y != other.y) or (self.z != other.z)

    def inside(self, x, y, dx, dy):
        """inside checks if the point instance is in the rectangle provided.
        """
        return (x < self.x < x + dx) and (y < self.y < y + dy)

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"
