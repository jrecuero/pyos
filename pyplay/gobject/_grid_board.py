import pygame
from ._point import Point
from ._collision import CollisionBox
from ._board import Board


class GridBoard(Board):
    def __init__(self, name, x, y, dx, dy, gsize, **kwargs):
        super(GridBoard, self).__init__(name, x, y, dx, dy, **kwargs)
        self.gsize = gsize
        self.detailed = kwargs.get("detailed", True)
        self.color = kwargs.get("color", True)
        self.pos = []
        for x in range(self.dx):
            self.pos.append(Point(self.x + x, self.y))
            self.pos.append(Point(self.x + x, self.y + self.dy))
        for y in range(self.dy):
            self.pos.append(Point(self.x, self.y + y))
            self.pos.append(Point(self.x + self.dx - 1, self.y + y))

    def add_cell(self, cell):
        cell.x = cell.x + self.x
        cell.y = cell.y + self.y
        return cell

    def gx(self, x):
        return x * self.gsize

    def gy(self, y):
        return y * self.gsize

    def grect(self, x, y):
        return (self.gx(x), self.gy(y), self.gsize, self.gsize)

    # def add_pos(self, pos):
    #     self.pos.extend(pos)

    def is_inside(self, pos):
        x, y = pos.get()
        return (self.x < x < (self.x + self.dx)) and (self.y < y < (self.y + self.dy))

    def get_collision_box(self):
        collision_box = CollisionBox()
        for p in self.pos:
            collision_box.add(p)
        return collision_box

    def render(self, surface, **kwargs):
        for p in self.pos:
            pygame.draw.rect(surface, self.color, self.grect(p.x, p.y))
        if self.detailed:
            for x in range(self.dx):
                pygame.draw.line(
                    surface,
                    self.color,
                    ((self.x + x) * self.gsize, (self.y * self.gsize)),
                    ((self.x + x) * self.gsize, (self.y + self.dy) * self.gsize),
                    1,
                )
            for y in range(self.dy):
                pygame.draw.line(
                    surface,
                    self.color,
                    (self.x * self.gsize, (self.y + y) * self.gsize),
                    ((self.x + self.dx) * self.gsize, (self.y + y) * self.gsize),
                    1,
                )
