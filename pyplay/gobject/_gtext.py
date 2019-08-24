import pygame
from .._color import Color
from .._gobject import GObject


class GText(GObject):
    def __init__(self, name, x, y, message, **kwargs):
        self.message = message
        self.font_name = kwargs.get("font_name", "Courier")
        self.font_size = kwargs.get("font_size", 18)
        self.font = pygame.font.SysFont(self.font_name, self.font_size)
        self.color = kwargs.get("color", Color.BLACK)
        self.gtext = self.font.render(self.message, True, self.color)
        rect = self.gtext.get_rect()
        super(GText, self).__init__(name, x, y, rect.w, rect.h, **kwargs)
        self.image.blit(self.gtext, (0, 0, self.dx, self.dy))

    def __str__(self):
        return f"[{self.gid}] : {self.__class__.__name__}@{self.name} | ({self.x}, {self.y}) {self.message}"
