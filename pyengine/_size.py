class Size:
    """Class Size identifies a 2-dimentional size.
    """

    def __init__(self, dx, dy):
        self.x = dx
        self.y = dy

    @property
    def halfx(self):
        """halfx property returns half of the x-size.
        """
        return self.x / 2

    @property
    def halfy(self):
        """halfy property returns half of the y-size.
        """
        return self.y / 2

    @property
    def half(self):
        """half property returns half of the size.
        """
        return (self.halfx, self.halfy)

    def in_x(self, x):
        """in_x returns in the given x-size fits in the size.
        """
        return x >= 0 and x < self.x

    def in_y(self, y):
        """in_y returns if the given y-size fits in the size.
        """
        return y >= 0 and y < self.y

    def in_size(self, x, y):
        """in returns if the give x-size and y-size fits in the size.
        """
        return self.in_x(x) and self.in_y(y)

    def __add__(self, other):
        """__add__ overloads mathematical add operation for Size instances.
        """
        return Size(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """__sub__ overloads mathematical subtract operation for Size
        instances.
        """
        return Size(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        """__eq__ overloads logical equal operation for Size instances.
        """
        return (self.x == other.x) and (self.y == other.y)

    def __ne__(self, other):
        """__ne__ overloads logical not equal operation for Size instances.
        """
        return (self.x != other.x) or (self.y != other.y)
