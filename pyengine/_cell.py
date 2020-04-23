class Cell:
    """Class Cell identifies every unique instance in a grid. A Cell has a
    position in the bi-dimensional grid and it can contain furher objects.
    """

    def __init__(self, row, col, gobject=None):
        self.row = row
        self.col = col
        self.gobjects = [gobject, ]

    def __str__(self):
        return f"({self.row}, {self.col})"
