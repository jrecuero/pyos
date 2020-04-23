from ._size import Size
from ._cell import Cell
from pygame import Rect
from pygame.math import Vector2


class Grid:
    """Class Grid identifies a grid containing a group of ordered cells to be
    displayed at fixed positions/
    """

    def __init__(self, rows, cols, g_x, g_y, g_dx, g_dy, **kwargs):
        self.rows = rows
        self.cols = cols
        self.g_cell_size = Size(g_dx, g_dy)
        self.g_origin = Vector2(g_x, g_y)
        self.g_size = Size(cols * self.g_cell_size.x, rows * self.g_cell_size.y)
        self.db = [[Cell(i, j) for j in range(self.cols)] for i in range(self.rows)]

    def cell(self, row, col):
        """cell returns the grid cell at the given coordinates.
        """
        return self.db[row][col]

    def g_cell(self, row, col):
        """g_cell returns the pixel location for the cell at the given
        coordinates.
        """
        return Vector2(self.g_origin.x + col * self.g_cell_size.x, self.g_origin.y + row * self.g_cell_size.y)

    def g_cell_rect(self, row, col):
        """g_cell_rect returns a rectangle with for the given cell.
        """
        origin = self.g_cell(row, col)
        return Rect(origin.x, origin.y, self.g_cell_size.x, self.g_cell_size.y)

    def grid_rect(self):
        """grid_rect returns a rectangle for the while grid.
        """
        return Rect(self.g_origin.x, self.g_origin.y, self.g_size.x, self.g_size.y)

    def in_bounds(self, row, col):
        """in_bounds returns in the given location is inside the grid or not.
        """
        return (0 <= row < self.rows) and (0 <= col < self.cols)
