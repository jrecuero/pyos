class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get(self):
        return (self.x, self.y)

    def set(self, x=None, y=None):
        self.x = self.x if x is None else x
        self.y = self.y if y is None else y

    def incr(self, x=None, y=None):
        self.x = self.x if x is None else (self.x + x)
        self.y = self.y if y is None else (self.y + y)

    def decr(self, x=None, y=None):
        self.x = self.x if x is None else (self.x - x)
        self.y = self.y if y is None else (self.y - y)

    def clone(self):
        return Point(self.x, self.y)

    def __add__(self, other):
        p = Point(self.x, self.y)
        if isinstance(other, int):
            p = Point(self.x + other, self.y + other)
        elif isinstance(other, Point):
            p = Point(self.x + other.x, self.y + other.y)
        return p

    def __sub__(self, other):
        p = Point(self.x, self.y)
        if isinstance(other, int):
            p = Point(self.x - other, self.y - other)
        elif isinstance(other, Point):
            p = Point(self.x - other.x, self.y - other.y)
        return p

    def __mul__(self, other):
        p = Point(self.x, self.y)
        if isinstance(other, int):
            p = Point(self.x * other, self.y * other)
        elif isinstance(other, Point):
            p = Point(self.x * other.x, self.y * other.y)
        return p

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)

    def __ne__(self, other):
        return (self.x != other.x) or (self.y != other.y)

    def inside(self, x, y, dx, dy):
        return (x < self.x < x * dx) and (y < self.y < y * dy)

    def __str__(self):
        return f"({self.x}, {self.y})"
