import pygame
from .._board import Board


class GridBoard(Board):
    """GridBoard represents a grid that contains only cell elements.
    """

    def __init__(self, name, x, y, dx, dy, xsize, ysize=None, **kwargs):
        super(GridBoard, self).__init__(name, x, y, dx, dy, **kwargs)
        # self.x = x
        # self.y = y
        # self.dx = dx
        # self.dy = dy
        self.gobjects = []
        self.xsize = xsize
        self.ysize = ysize if ysize is not None else xsize
        self.border = kwargs.get("border", True)
        self.dx_cells = self.dx // self.xsize
        self.dy_cells = self.dy // self.ysize
        self.dx_play_cells = (self.dx_cells - 2) if self.border else self.dx_cells
        self.dy_play_cells = (self.dy_cells - 2) if self.border else self.dy_cells
        self.play_cells = [[None] * self.dx_play_cells] * self.dy_play_cells

    def add_gobject(self, shape):
        """add_shape adds a new shape to be handle by the grid board.
        """
        for cell in shape.cells:
            cell.x = self.x + cell.x * self.xsize
            cell.y = self.y + cell.y * self.ysize
        self.gobjects.append(shape)

    def del_gobject(self, shape):
        """del_shape deletes a shape from the grid board.
        """
        if shape in self.gobjects:
            self.gobjects.remove(shape)

    def update(self, surface, **kwargs):
        for shape in self.gobjects:
            shape.update(surface, **kwargs)

        for shape in self.gobjects:
            x = 1 if self.border else 0
            y = 1 if self.border else 0
            collision_box = shape.get_collision_box()
            if collision_box.check_out_of_bounds(
                x, y, self.dx_play_cells, self.dy_play_cells
            ):
                pass

    def render(self, surface, **kwargs):
        for x in range(self.dx // self.xsize):
            pygame.draw.line(
                self.image,
                self.color,
                (x * self.xsize, 0),
                (x * self.xsize, self.dy),
                1,
            )
        for y in range(self.dy // self.ysize):
            pygame.draw.line(
                self.image,
                self.color,
                (0, y * self.ysize),
                (self.dx, y * self.ysize),
                1,
            )
        for shape in self.gobjects:
            shape.render(surface, **kwargs)
