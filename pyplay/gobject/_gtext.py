import pygame
from .._color import Color
from .._point import Point
from .._gobject import GObject


class GText(GObject):
    def __init__(self, name, x, y, message, **kwargs):
        super(GText, self).__init__(name, pos=Point(x, y), **kwargs)
        self.message = message
        self.font_name = kwargs.get("font_name", "Courier")
        self.font_size = kwargs.get("font_size", 18)
        self.color = kwargs.get("color", Color.BLACK)
        self.font = pygame.font.SysFont(self.font_name, self.font_size)
        self.gtext = self.font.render(self.message, True, self.color)
        rect = self.gtext.get_rect()
        rect.x = self.x
        rect.y = self.y
        self.set_content(rect, GObject.TEXT)

    def __str__(self):
        return f"[{self.gid}] : {self.__class__.__name__}@{self.name} | ({self.x}, {self.y}) {self.message}"

    def bounds(self):
        """bounds should returns a rectangle that contains the whole
        graphical object.
        """
        return self.content

    def render(self, surface, **kwargs):
        surface.blit(self.gtext, self.content)
