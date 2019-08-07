import pygame


class Entity:
    def __init__(self, sprite, dx, dy, color):
        self.sprite = sprite
        self.dx = dx
        self.dy = dy
        self.color = color
        self._enable = True

    def __str__(self):
        return f"[{self.dx}, {self.dy}, {self.color}]"

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
