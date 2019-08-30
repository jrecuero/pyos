import pygame
from ..._loggar import log
from ..._gevent import GEvent
from ._cell import Cell
from ._shape import Shape


class TriShape(Shape):
    """TriShape implements a 3x3 shape that can rotates its content.
    """

    def __init__(self, name, x, y, matrix, xsize, ysize, **kwargs):
        super(TriShape, self).__init__(name, x, y, **kwargs)
        self._matrix = matrix
        self.xsize = xsize
        self.ysize = ysize
        self._matrix_to_cells(x, y, **kwargs)

    def _matrix_to_cells(self, x, y, **kwargs):
        """_matrix_to_cells populates cells attributes based on the given
        matrix array. It creates one rectangular cell (default) for every
        one in the matrix provided.
        """
        self.cells = []
        r, c = y, x
        for row in self._matrix:
            for col in row:
                if col:
                    self.add_cell(
                        Cell(f"{row},{col}", c, r, self.xsize, self.ysize, **kwargs)
                    )
                c += 1
            r += 1
            c = x

    def rotate_clockwise(self):
        """rotate_clockwise rotates the shape by 90 degrees clockwise.
        """
        # result = [row[:] for row in self._matrix]
        # matrix_size = len(self._matrix[0])
        # for x in range(0, matrix_size):
        #     for j in range(0, matrix_size):
        #         result[j][matrix_size - 1 - x] = self._matrix[x][j]
        # self._matrix = result
        # self._matrix_to_cells(self.gridx, self.gridy)
        matrix_size = len(self._matrix)
        for cell in self.cells:
            gridx = cell.gridx - self.gridx
            gridy = cell.gridy - self.gridy
            deltax = matrix_size - 1 - gridy - gridx
            deltay = gridx - gridy
            cell.move_it(deltax, deltay)

    def rotate_anticlockwise(self):
        """rotate_anticlockwise rotates the shape by 90 degrees anti-clockwise.
        """
        # result = [row[:] for row in self._matrix]
        # matrix_size = len(self._matrix[0])
        # for x in range(0, matrix_size):
        #     for j in range(0, matrix_size):
        #         result[x][j] = self._matrix[j][matrix_size - 1 - x]
        # self._matrix = result
        # self._matrix_to_cells(self.gridx, self.gridy)
        matrix_size = len(self._matrix)
        for cell in self.cells:
            gridx = cell.gridx - self.gridx
            gridy = cell.gridy - self.gridy
            deltay = matrix_size - 1 - gridx - gridy
            deltax = gridy - gridx
            cell.move_it(deltax, deltay)

    def handle_keyboard_event(self, event):
        """handle_keyboard_event should process the keyboard event given.
        """
        self.gravity_step = False
        if event.key == pygame.K_LEFT:
            self.move_it(-1, 0)
        elif event.key == pygame.K_RIGHT:
            self.move_it(1, 0)
        elif event.key == pygame.K_UP:
            #     self.move_it(0, -1)
            #     self.gridy -= 1
            self.rotate_clockwise()
        elif event.key == pygame.K_DOWN:
            #     self.move_it(0, 1)
            #     self.gridy += 1
            self.rotate_anticlockwise()
        # if event.key == pygame.K_SPACE:
        #     self.rotate_clockwise()

    # def handle_custom_event(self, event):
    #     """handle_custom_event should process pygame custom event given.
    #     Any object in the game, like, scene, graphic objects, ... can post
    #     customs events, and those should be handled at this time.
    #     """
    #     super(TriShape, self).handle_custom_event(event)
    #     if event.type == GEvent.GRAVITY:
    #         log.Gravity().TriShape(f"{self.gridx}, {self.gridy}").Cell(
    #             f"{self.cells[0].gridx}, {self.cells[0].gridy}"
    #         ).call()
