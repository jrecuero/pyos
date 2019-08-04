import pygame


class Entity:

    def __init__(self, sprite, dx, dx, color):
        self.sprite = sprite
        self.dx = dx
        self.dy = dy
        self.color = color
        self._enable = True

    def enable(self):
        self._enable = True

    def disable(self):
        self._enable = False

    def is_enable(self):
        return self._enable

    def render_at(self, surface, x, y, **kwargs):
        if self.is_enable():
            self.sprite.x = x
            self.sprite.y = y
            pygame.draw.rect(surface, self.color, self.sprite)
