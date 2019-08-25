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
        x, y = pos.get()
        return (self.x < x < (self.x + self.dx)) and (self.y < y < (self.y + self.dy))

    # def get_collision_box(self):
    #     collision_box = CollisionBox()
    #     for p in self.pos:
    #         collision_box.add(p)
    #     return collision_box
    #
    # def render(self, surface, **kwargs):
    #     for p in self.pos:
    #         pygame.draw.rect(surface, self.color, self.grect(p.x, p.y))
    #     if self.detailed:
    #         for x in range(self.dx):
    #             pygame.draw.line(
    #                 surface,
    #                 self.color,
    #                 ((self.x + x) * self.gsize, (self.y * self.gsize)),
    #                 ((self.x + x) * self.gsize, (self.y + self.dy) * self.gsize),
    #                 1,
    #             )
    #         for y in range(self.dy):
    #             pygame.draw.line(
    #                 surface,
    #                 self.color,
    #                 (self.x * self.gsize, (self.y + y) * self.gsize),
    #                 ((self.x + self.dx) * self.gsize, (self.y + y) * self.gsize),
    #                 1,
    #             )
