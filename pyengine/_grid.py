from ._size import Size
from ._cell import Cell
from ._layer import Layer
from ._gobject import GObject
import pygame
from pygame.math import Vector2


class Grid(GObject):
    """Class Grid identifies a grid containing a group of ordered cells to be
    displayed at fixed positions/
    """

    def __init__(self, name, rows, cols, g_x, g_y, g_dx, g_dy, **kwargs):
        self.rows = rows
        self.cols = cols
        self.g_cell_size = Size(g_dx, g_dy)
        self.g_origin = Vector2(g_x, g_y)
        self.g_size = Size(cols * self.g_cell_size.x, rows * self.g_cell_size.y)
        super(Grid, self).__init__(self, self.g_origin.x, self.g_origin.y, self.g_size.x, self.g_size.y, **kwargs)
        self.db = [[Cell(i, j) for j in range(self.cols)] for i in range(self.rows)]
        self.gobjects = {Layer.BACKGROUND: pygame.sprite.Group(),
                         Layer.GROUND: pygame.sprite.Group(),
                         Layer.TOP: pygame.sprite.Group(), }
        self.running = True

    def __str__(self):
        return f"[{self.gid}] : {self.__class__.__name__} ({self.x}, {self.y}) ({self.dx}, {self.dy})"

    def cell(self, row, col):
        """cell returns the grid cell at the given coordinates.
        """
        return self.db[row][col]

    def g_cell(self, row, col):
        """g_cell returns the pixel location for the cell at the given
        coordinates.
        """
        return Vector2(self.g_origin.x + col * self.g_cell_size.x, self.g_origin.y + row * self.g_cell_size.y)

    def g_cell_rect(self, row, col):
        """g_cell_rect returns a rectangle with for the given cell.
        """
        origin = self.g_cell(row, col)
        return pygame.Rect(origin.x, origin.y, self.g_cell_size.x, self.g_cell_size.y)

    def grid_rect(self):
        """grid_rect returns a rectangle for the while grid.
        """
        return pygame.Rect(self.g_origin.x, self.g_origin.y, self.g_size.x, self.g_size.y)

    def in_bounds(self, row, col):
        """in_bounds returns in the given location is inside the grid or not.
        """
        return (0 <= row < self.rows) and (0 <= col < self.cols)

    def add_gobject(self, gobject):
        """add_gobject adds a graphical object to the grid.
        """
        layer = gobject.z
        self.gobjects[layer].add(gobject)

    def del_gobject(self, gobject):
        """del_gobject deletes a graphical object from the grid.
        """
        layer = gobject.z
        if gobject in self.gobjects[layer]:
            self.gobjects[layer].remove(gobject)

    def start_tick(self):
        """start_tick should set all elements ready for a new tick.
        """
        for gobj in [o for _, o in self.gobjects.items()]:
            gobj.start_tick()

    def end_tick(self):
        """end_tick shoudl set all elements ready for the end of a tick. Any
        structure to be clean up can be done at this point.
        """
        for gobj in [o for _, o in self.gobjects.items()]:
            gobj.end_tick()

    def handle_keyboard_event(self, event):
        """handle_keyboard_event should process the keyboard event given.
        """
        if self.running:
            for gobj in [o for _, o in self.gobjects.items()]:
                gobj.handle_keyboard_event(event)

    def handle_mouse_event(self, event):
        """handle_mouse_event should process the mouse event given.
        Mouse events are passed to the active scene to be handle.
        """
        for gobj in [o for _, o in self.gobjects.items()]:
            gobj.handle_mouse_event(event)

    def handle_custom_event(self, event):
        """handle_custom_event should process pygame custom event given.
        Any object in the game, like, scene, graphic objects, ... can post
        customs events, and those should be handled at this time.
        """
        for gobj in [o for _, o in self.gobjects.items()]:
            gobj.handle_custom_event(event)

    def update(self, surface, **kwargs):
        """update provides any functionality to be done every tick.
        """
        for gobj in [o for _, o in self.gobjects.items()]:
            gobj.update(surface)

    def render(self, surface, **kwargs):
        """render should draws the instance on the given surface.
        """
        for _, gobjects in self.gobjects.items():
            gobjects.draw(surface)
