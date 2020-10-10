import pygame
from .._gobject import GObject


class GCheckBox(GObject):
    """GCheckBox implements a graphical object for a check box.
    """

    def __init__(self, name, x, y, dx, dy, **kwargs):
        super(GCheckBox, self).__init__(name, x, y, dx, dy, **kwargs)
        self.selected = False
        # pygame.draw.rect(self.image, self.color, (0, 0, self.dx, self.dy), self.outline)

    def __str__(self):
        return f"[{self.gid}] : {self.__class__.__name__}@{self.name} | ({self.x}, {self.y}) ({self.dx}, {self.dy})"

    def handle_mouse_event(self, event):
        """handle_mouse_event should process the mouse event given.
        Mouse events are passed to the active scene to be handle.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(pos):
                self.selected = not self.selected

    def update(self, surface, **kwargs):
        """update calls update method for all scene graphical objects.
        """
        self.image.fill((255, 255, 255, 0))
        if self.selected:
            pygame.draw.rect(self.image, self.color, (0, 0, self.dx, self.dy))
        else:
            pygame.draw.rect(self.image, self.color, (0, 0, self.dx, self.dy), 2)
