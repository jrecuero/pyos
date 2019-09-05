import pygame

# from ..._loggar import log
from ._cell import Cell
from ._shape import Shape


class TriShape(Shape):
    """TriShape implements a 3x3 shape that can rotates its content.
    """

    def __init__(self, name, x, y, matrix, xsize, ysize, **kwargs):
        super(TriShape, self).__init__(
            name, x, y, len(matrix[0]), len(matrix), xsize, ysize, **kwargs
        )
        self._matrix = matrix
        self._matrix_to_cells(x, y, **kwargs)

    def _matrix_to_cells(self, x, y, **kwargs):
        """_matrix_to_cells populates cells attributes based on the given
        matrix array. It creates one rectangular cell (default) for every
        one in the matrix provided.
        """
        self.cells = []
        r, c = 0, 0
        for row in self._matrix:
            for col in row:
                if col:
                    self.add_cell(
                        Cell(f"{row},{col}", c, r, self.xsize, self.ysize, **kwargs)
                    )
                c += 1
            r += 1
            c = 0

    def handle_keyboard_event(self, event):
        """handle_keyboard_event should process the keyboard event given.
        """
        self.gravity_step = False
        if event.key == pygame.K_LEFT:
            # self.move_it(-1, 0)
            self.move_actions.append({"call": self.move_it, "args": (-1, 0)})
        elif event.key == pygame.K_RIGHT:
            # self.move_it(1, 0)
            self.move_actions.append({"call": self.move_it, "args": (1, 0)})
        elif event.key == pygame.K_UP:
            # self.rotate_clockwise()
            self.move_actions.append({"call": self.rotate_clockwise, "args": ()})
        elif event.key == pygame.K_DOWN:
            # self.rotate_anticlockwise()
            self.move_actions.append({"call": self.rotate_anticlockwise, "args": ()})
        elif event.key == pygame.K_SPACE:
            self.gravity_move(1)
