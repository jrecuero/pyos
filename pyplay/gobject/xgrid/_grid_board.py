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
        self.xsize = xsize
        self.ysize = ysize if ysize is not None else xsize
        self.border = kwargs.get("border", True)
        self.dx_cells = self.dx // self.xsize
        self.dy_cells = self.dy // self.ysize
        self.dx_play_cells = (self.dx_cells - 2) if self.border else self.dx_cells
        self.dy_play_cells = (self.dy_cells - 2) if self.border else self.dy_cells
        self.play_cells = [[None] * self.dx_play_cells] * self.dy_play_cells
        self.shapes = []

    def add_shape(self, shape):
        """add_shape adds a new shape to be handle by the grid board.
        """
        shape.x = self.x + shape.x * self.xsize
        shape.y = self.y + shape.y * self.ysize
        self.shapes.append(shape)

    def del_shape(self, shape):
        """del_shape deletes a shape from the grid board.
        """
        if shape in self.shapes:
            self.shapes.remove(shape)

    def update(self, surface, **kwargs):
        for shape in self.shapes:
            shape.update(surface, **kwargs)

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
        for shape in self.shapes:
            shape.render(surface, **kwargs)
