import pygame
from ._gobject import GObject
from ._loggar import Log
from ._gmenuitem import GMenuItem


class GMenu(GObject):
    """GMenu implementsa graphical menu entity.
    """

    def __init__(self, name, x, y, dx, dy, **kwargs):
        super(GMenu, self).__init__(name, x, y, dx, dy, **kwargs)
        self.menu_items = pygame.sprite.Group()
        self._next_item_x = self.x
        self._next_item_y = self.y
        Log.Menu(self.name).Create().call()

    def add_menu_item(self, text, **kwargs):
        """add_menu_item adds a new menu item entry.
        """
        # menu_item.x = self.x
        # menu_item.y = self.y
        # menu_item.dx = self.dx
        # menu_item.dy = self.dy
        menu_item = GMenuItem(text, text, self._next_item_x, self._next_item_y)
        self._next_item_x += 100
        self.menu_items.add(menu_item)
        return True

    def render(self, surface, **kwargs):
        """render should draws the instance on the given surface.
        """
        # Render all menu items children
        self.menu_items.draw(surface)
        for mi in self.menu_items:
            mi.render(surface, **kwargs)
