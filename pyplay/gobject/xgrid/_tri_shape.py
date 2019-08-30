import pygame

# from ..._loggar import log
from ._cell import Cell
from ._shape import Shape
from ._grid_event import GridEvent


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
        if not self.allow_rotation:
            return
        self.is_rotation = True
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
        if not self.allow_rotation:
            return
        self.is_rotation = True
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
            self.rotate_clockwise()
        elif event.key == pygame.K_DOWN:
            self.rotate_anticlockwise()
        elif event.key == pygame.K_SPACE:
            # self.gravity_move(1)
            gravity_event = pygame.event.Event(GridEvent.GRAVITY)
            pygame.event.post(gravity_event)
