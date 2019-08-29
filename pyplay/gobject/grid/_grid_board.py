import pygame

from .._board import Board


class GridBoard(Board):
    def __init__(self, name, x, y, dx, dy, xsize, ysize=None, **kwargs):
        super(GridBoard, self).__init__(name, x, y, dx, dy, **kwargs)
        self.xsize = xsize
        self.ysize = ysize if ysize is not None else xsize
        self.detailed = kwargs.get("detailed", True)
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

    def __str__(self):
        return f"[{self.gid}] : {self.__class__.__name__} ({self.x}, {self.y}) ({self.dx}, {self.dy}) {self.xsize} {self.ysize}"

    def add_gobject(self, gobject):
        """add_gobject adds a graphical object to the scene.
        """
        gobject.x = self.x + gobject.x * self.xsize
        gobject.y = self.y + gobject.y * self.ysize
        self.gobjects.add(gobject)

    def is_inside(self, pos):
        """is_inside checks if the given position is inside the board.
        """
        x, y = pos.get()
        return (self.x < x < (self.x + self.dx)) and (self.y < y < (self.y + self.dy))
