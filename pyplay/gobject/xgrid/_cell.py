import pygame
from ..._gid import new_gid
from ..._move import Move
from ..._color import Color
from ._collision_box import CollisionBox


class Cell:
    """Cell represents every entry in the graphical grid.
    """

    def __init__(self, name, x, y, dx, dy, **kwargs):
        self.__gid = new_gid()
        self.x = x
        self.y = y
        self.z = kwargs.get("z", 0)
        self.dx = dx
        self.dy = dy
        self.gridx = x
        self.gridy = y
        self.image = None
        self.rect = None
        self.move = kwargs.get("move", Move())
        self.pushed = kwargs.get("pushed", None)
        self.enable = kwargs.get("enable", True)
        self.visible = kwargs.get("visible", True)
        self.solid = kwargs.get("solid", True)
        self.color = kwargs.get("color", Color.BLACK)
        self.outline = kwargs.get("outline", 0)
        self.content = kwargs.get("content", None)
        self.stepx = None
        self.stepy = None

    @property
    def gid(self):
        return self.__gid

    def __str__(self):
        return f"[{self.gid}] : {self.__class__.__name__} | {self.x} {self.y} {self.dx} {self.dy} {self.gridx} {self.gridy}"

    def get_collision_box(self):
        """get_collision_box retrieves grid cells that can collide with any
        other cell.
        """
        collision_box = CollisionBox()
        collision_box.add(self.gridx, self.gridy)
        return collision_box

    def move_it(self, dx=0, dy=0):
        """move_it moves a cell the given X and Y offsets. Grid position and
        graphical position are stored and move delta is stored.
        """
        self.gridx += dx
        self.gridy += dy
        self.x += dx * self.dx
        self.y += dy * self.dy
        self.stepx = dx
        self.stepy = dy

    def back_it(self):
        """back_it moves back last cell move.
        """
        if self.stepx is not None and self.stepy is not None:
            self.gridx -= self.stepx
            self.gridy -= self.stepy
            self.x -= self.stepx * self.dx
            self.y -= self.stepy * self.dy
            self.stepx = None
            self.stepy = None

    def update(self, surface, **kwargs):
        pass

    def render(self, surface, **kwargs):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.dx, self.dy))
