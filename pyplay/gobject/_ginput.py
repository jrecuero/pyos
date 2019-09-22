import pygame
from .._gobject import GObject


class GInput(GObject):
    """GInput implements a graphical object that allows text input.
    """

    def __init__(self, name, x, y, dx, dy, **kwargs):
        super(GInput, self).__init__(name, x, y, dx, dy, **kwargs)
        # in_focus attributes is used to indicate when the widget has to accept
        # user keyboard inputs.
        self.in_focus = False
        self._message = ""
        self.font_name = kwargs.get("font_name", "Courier")
        self.font_size = kwargs.get("font_size", 18)
        self.font_bold = kwargs.get("font_bold", False)
        self.font_italic = kwargs.get("font_italic", False)
        self.font = pygame.font.SysFont(
            self.font_name, self.font_size, bold=self.font_bold, italic=self.font_italic
        )
        pygame.draw.rect(self.image, self.color, (0, 0, self.dx, self.dy))

    def __str__(self):
        return f"[{self.gid}] : {self.__class__.__name__}@{self.name} | ({self.x}, {self.y}) ({self.dx}, {self.dy})"

    def handle_keyboard_event(self, event):
        """handle_keyboard_event should process the keyboard event given.
        """
        if event.type == pygame.KEYUP and self.in_focus:
            if event.key == pygame.K_BACKSPACE:
                self._message = self._message[:-1]
            else:
                self._message = self._message + chr(event.key)

    def handle_mouse_event(self, event):
        """handle_mouse_event should process the mouse event given.
        Mouse events are passed to the active scene to be handle.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(pos):
                self.in_focus = True
            else:
                self.in_focus = False

    def update(self, surface, **kwargs):
        """update calls update method for all scene graphical objects.
        """
        self.image.fill((255, 255, 255, 0))
        self.gtext = self.font.render(self._message, True, self.color)
        if self.in_focus:
            pygame.draw.rect(self.image, self.color, (0, 0, self.dx, self.dy), 1)
        else:
            pygame.draw.rect(self.image, self.color, (0, 0, self.dx, self.dy))
        self.image.blit(self.gtext, (0, 0, self.dx, self.dy))
