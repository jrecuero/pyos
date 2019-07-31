class Point(object):
    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, val):
        self._y = val

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, val):
        self._x = val

    def hash(self):
        return (self.x, self.y)

    def set(self, x=None, y=None):
        self._x = self.x if x is None else x
        self._y = self.y if y is None else y

    def inc(self, x=None, y=None):
        self._x = self.x if x is None else (self.x + x)
        self._y = self.y if y is None else (self.y + y)

    def incr(self, x=None, y=None):
        x = self.x if x is None else (self.x + x)
        y = self.y if y is None else (self.y + y)
        return Point(x, y)

    def dec(self, x=None, y=None):
        self._x = self.x if x is None else (self.x - x)
        self._y = self.y if y is None else (self.y - y)

    def decr(self, x=None, y=None):
        x = self.x if x is None else (self.x - x)
        y = self.y if y is None else (self.y - y)
        return Point(x, y)

    def __add__(self, other):
        p = Point(self.x, self.y)
        if isinstance(other, int):
            p = Point(self.x + other, self.y + other)
        elif isinstance(self, Point):
            p = Point(self.x + other.x, self.y + other.y)
        return p

    def __sub__(self, other):
        p = Point(self.x, self.y)
        if isinstance(other, int):
            p = Point(self.x - other, self.y - other)
        elif isinstance(self, Point):
            p = Point(self.x - other.x, self.y - other.y)
        return p

    def __mul__(self, other):
        p = Point(self.x, self.y)
        if isinstance(other, int):
            p = Point(self.x * other, self.y * other)
        elif isinstance(self, Point):
            p = Point(self.x * other.x, self.y * other.y)
        return p

    def get(self):
        return (self.x, self.y)

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)

    def __ne__(self, other):
        return (self.x != other.x) or (self.y != other.y)

    def inside(self, x, y, max_x, max_y):
        return (x < self.x < x + max_x) and (y < self.y < y + max_y)

    def __str__(self):
        return "({}, {})".format(self.x, self.y)
