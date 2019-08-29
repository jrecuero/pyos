import pygame
from .._board import Board

# from ..._loggar import log


class GridBoard(Board):
    """GridBoard represents a grid that contains only cell elements.
    """

    def __init__(self, name, x, y, dx, dy, xsize, ysize=None, **kwargs):
        super(GridBoard, self).__init__(name, x, y, dx, dy, **kwargs)
        self.gobjects = []
        self.xsize = xsize
        self.ysize = ysize if ysize is not None else xsize
        self.border = kwargs.get("border", True)
        self.dx_cells = self.dx // self.xsize
        self.dy_cells = self.dy // self.ysize
        self.dx_play_cells = self.dx_cells
        self.dy_play_cells = self.dy_cells
        # self.play_cells = [[None] * self.dx_play_cells] * self.dy_play_cells
        self.play_cells = []
        for irow in range(self.dy_play_cells):
            row = []
            for icol in range(self.dx_play_cells):
                row.append(None)
            self.play_cells.append(row)
        # log.GravityBoard().PlayCells(
        #     f"{self.dx_play_cells}, {self.dy_play_cells}"
        # ).call()

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
        """update provides any functionality to be done every tick.
        """
        for shape in self.gobjects:
            shape.update(surface, **kwargs)

        for shape in self.gobjects:
            collision_box = shape.get_collision_box()
            if collision_box.check_out_of_bounds(
                0, 0, self.dx_play_cells, self.dy_play_cells
            ):
                # log.GridBoard().Collision(shape).call()
                shape.back_it()

    def render(self, surface, **kwargs):
        """render should draws the instance on the given surface.
        """
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
        for cell in [c for row in self.play_cells for c in row if c]:
            cell.render(surface, **kwargs)
        for shape in self.gobjects:
            shape.render(surface, **kwargs)
