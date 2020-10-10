import os
import pygame
from .._gobject import GObject


class GImage(GObject):
    """GRect implements a graphical object that is an image.
    """

    def __init__(self, name, image, x, y, dx, dy, **kwargs):
        super(GImage, self).__init__(name, x, y, dx, dy, **kwargs)
        # self.filename = filename
        # self.image = pygame.image.load(self.filename)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def __str__(self):
        return f"[{self.gid}] : {self.__class__.__name__}@{self.name} | ({self.x}, {self.y}) ({self.dx}, {self.dy})"
