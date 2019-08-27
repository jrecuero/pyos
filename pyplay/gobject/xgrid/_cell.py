import pygame
from ..._move import Move
from ..._color import Color


class Cell:
    """Cell represents every entry in the graphical grid.
    """

    def __init__(self, name, x, y, dx, dy, **kwargs):
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

    def update(self, surface, **kwargs):
        pass

    def render(self, surface, **kwargs):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.dx, self.dy))
