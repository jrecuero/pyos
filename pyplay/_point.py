class Point:
    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = 0

    def get(self):
        return (self.x, self.y)

    def zget(self):
        return (self.x, self.y, self.z)

    def set(self, x=None, y=None, z=None):
        self.x = self.x if x is None else x
        self.y = self.y if y is None else y
        self.z = self.z if z is None else z

    def incr(self, x=None, y=None, z=None):
        self.x = self.x if x is None else (self.x + x)
        self.y = self.y if y is None else (self.y + y)
        self.z = self.z if z is None else (self.z + z)

    def decr(self, x=None, y=None, z=None):
        self.x = self.x if x is None else (self.x - x)
        self.y = self.y if y is None else (self.y - y)
        self.z = self.z if z is None else (self.z - z)

    def clone(self):
        return Point(self.x, self.y, self.z)

    def __add__(self, other):
        p = Point(self.x, self.y, self.z)
        if isinstance(other, int):
            p = Point(self.x + other, self.y + other, max(p.z, self.z))
        elif isinstance(other, Point):
            p = Point(self.x + other.x, self.y + other.y, max(p.z, self.z))
        return p

    def __sub__(self, other):
        p = Point(self.x, self.y)
        if isinstance(other, int):
            p = Point(self.x - other, self.y - other, max(p.z, self.z))
        elif isinstance(other, Point):
            p = Point(self.x - other.x, self.y - other.y, max(p.z, self.z))
        return p

    def __mul__(self, other):
        p = Point(self.x, self.y)
        if isinstance(other, int):
            p = Point(self.x * other, self.y * other, max(p.z, self.z))
        elif isinstance(other, Point):
            p = Point(self.x * other.x, self.y * other.y, max(p.z, self.z))
        return p

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y) and (self.z == other.z)

    def __ne__(self, other):
        return (self.x != other.x) or (self.y != other.y) or (self.z != other.z)

    def inside(self, x, y, dx, dy):
        return (x < self.x < x * dx) and (y < self.y < y * dy)

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"
