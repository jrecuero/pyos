import pygame
from ._gobject import GObject, Color


class GMenuItem(GObject):
    """GMenuItem implements a graphical menu item entiry.
    """

    VERTICAL = 1
    HORIZONTAL = 2

    def __init__(self, name, text, x=0, y=0, **kwargs):
        self.text = text
        self.menu_items = []
        self.shortcut = kwargs.get("shortcut", None)
        self.orientation = kwargs.get("orientation", GMenuItem.HORIZONTAL)
        self.callback = kwargs.get("callback", None)
        self.font_name = kwargs.get("font_name", "Courier")
        self.font_size = kwargs.get("font_size", 18)
        self.font_bold = kwargs.get("font_bold", False)
        self.font_italic = kwargs.get("font_italic", False)
        self.color = kwargs.get("color", Color.BLACK)
        self.background_color = kwargs.get("bcolor", Color.WHITE)
        self.font = pygame.font.SysFont(self.font_name, self.font_size, bold=self.font_bold, italic=self.font_italic)
        self.gtext = self.font.render(self.text, True, self.color)
        rect = self.gtext.get_rect()
        super(GMenuItem, self).__init__(name, x, y, rect.w, rect.h, **kwargs)
        self.image.fill(self.background_color)
        self.image.blit(self.gtext, (0, 0, self.dx, self.dy))

    def add_menu_item(self, menu_item):
        """add_menu_item adds a new menu item entry.
        """
        self.menu_items.append(menu_item)
        return True

    def select(self, **kwargs):
        """select implements functionality to be called whe menu item is
        selected.
        """
        if self.callback:
            self.callback(**kwargs)

    def render(self, surface, **kwargs):
        """render should draws the instance on the given surface.
        """
        if self.enable:
            # Render Menu Item
            # self.gtext = self.font.render(self.text, True, self.color)
            # self.rect = self.gtext.get_rect()
            # self.rect.x = self.x
            # self.rect.y = self.y
            # self._dx = self.rect.w
            # self._dy = self.rect.h
            # self.image.fill((255, 255, 255, 0))
            # self.image.fill(self.background_color)
            # self.image.blit(self.gtext, (0, 0, self.dx, self.dy))
            pass

            if not self.grayout and self.selected:
                # Render all menu items children
                for mi in self.menu_items:
                    mi.render(surface, **kwargs)
