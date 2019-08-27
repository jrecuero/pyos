import pygame
from ._grid_object import GridObject


class GridShape(GridObject):
    def __init__(self, name, x, y, matrix, gsize, **kwargs):
        super(GridShape, self).__init__(
            name, x, y, gsize * len(matrix[0]), gsize * len(matrix), **kwargs
        )
        self.matrix = matrix
        self.gsize = gsize
        r = 0
        c = 0
        for row in self.matrix:
            for col in row:
                if col:
                    pygame.draw.rect(
                        self.image, self.color, (r, c, self.gsize, self.gsize)
                    )
                c += self.gsize
            r += self.gsize
            c = 0

    def handle_keyboard_event(self, event):
        """handle_keyboard_event should process the keyboard event given.
        """
        if event.key == pygame.K_LEFT:
            self.move_inc(self.gsize * (-1), 0)
            self.gridx -= 1
        if event.key == pygame.K_RIGHT:
            self.move_inc(self.gsize, 0)
            self.gridx += 1
        if event.key == pygame.K_UP:
            self.move_inc(0, self.gsize * (-1))
            self.gridy -= 1
        if event.key == pygame.K_DOWN:
            self.move_inc(0, self.gsize)
            self.gridy += 1
        if event.key == pygame.K_SPACE:
            self.image = pygame.transform.rotate(self.image, -90)
