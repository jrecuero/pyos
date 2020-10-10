import random
import pygame


class Content:
    def __init__(self, dx, dy, colors):
        self.dx = dx
        self.dy = dy
        self.color = random.choice(colors)
        self._enable = True

    def enable(self):
        self._enable = True

    def disable(self):
        self._enable = False

    def is_enable(self):
        return self._enable

    def render_at(self, surface, x, y, **kwargs):
        if self.is_enable():
            pygame.draw.rect(surface, self.color, (x, y, self.dx, self.dy))
