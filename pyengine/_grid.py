from ._loggar import Log
from ._size import Size
from ._cell import Cell
from ._layer import Layer
from ._gobject import GObject
from ._color import Color
from ._gevent import GEvent
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
        super(Grid, self).__init__(name, self.g_origin.x, self.g_origin.y, self.g_size.x, self.g_size.y, **kwargs)
        self.db = [[Cell(i, j) for j in range(self.cols)] for i in range(self.rows)]
        self.catch_keyboard_gobject = None
        self.gobjects = {Layer.BACKGROUND: pygame.sprite.Group(),
                         Layer.GROUND: pygame.sprite.Group(),
                         Layer.TOP: pygame.sprite.Group(), }
        self.running = True
        self.render_grid = kwargs.get("render_grid", True)

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

    def g_to_cell(self, x, y):
        """g_to_cell translates graphical x-y coordinates to grid row/col values.
        """
        col = (x - self.g_origin.x) / self.g_cell_size.x
        row = (y - self.g_origin.y) / self.g_cell_size.y
        return int(row), int(col)

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

    def add_gobject_to_cell(self, gobject):
        """add_gobject_to_cell add a graphical object to the cell related with the
        gobject position.
        """
        row, col = self.g_to_cell(gobject.x, gobject.y)
        Log.Grid(self.name).AddGObjToCell(gobject.name).Cell(f"{row}, {col}").XY(f"{gobject.x}, {gobject.y}").call()
        cell = self.cell(row, col)
        cell.add_gobject(gobject)
        # gobject._cell = cell
        # cell.gobjects.append(gobject)

    def del_gobject_from_cell(self, gobject):
        """del_gobject_from_cell removes the graphical object from the cell related
        with the gobject position.
        """
        cell = gobject._cell
        if cell:
            cell.del_gobject(gobject)
            # cell.gobjects.remove(gobject)
            # gobject._cell = None
            Log.Grid(self.name).DelGObjFromCell(gobject.name).Cell(f"{cell.row}, {cell.col}").XY(f"{gobject.x}, {gobject.y}").call()

    def add_gobject(self, gobject, relative=True):
        """add_gobject adds a graphical object to the grid.
        """
        if gobject.catch_keyboard and self.catch_keyboard_gobject:
            raise Exception(f"Already configured catch keyboard gobject: {self.catch_keyboard_gobject}")
        layer = gobject.z
        self.gobjects[layer].add(gobject)
        if gobject.catch_keyboard:
            self.catch_keyboard_gobject = gobject
        if relative:
            gobject.x += self.g_origin.x
            gobject.y += self.g_origin.y
        self.add_gobject_to_cell(gobject)

    def del_gobject(self, gobject):
        """del_gobject deletes a graphical object from the grid.
        """
        layer = gobject.z
        if gobject in self.gobjects[layer]:
            self.gobjects[layer].remove(gobject)
            if gobject._cell:
                self.del_gobject_from_cell(gobject)

    def start_tick(self):
        """start_tick should set all elements ready for a new tick.
        """
        for gobj in [o for _, go in self.gobjects.items() for o in go]:
            gobj.start_tick()

    def end_tick(self):
        """end_tick shoudl set all elements ready for the end of a tick. Any
        structure to be clean up can be done at this point.
        """
        for gobj in [o for _, go in self.gobjects.items() for o in go]:
            gobj.end_tick()

    def move_it_gobject(self, gobject, dx, dy):
        """move_it_gobject moves the given object the given x-y delta.
        """
        dx, dy = int(dx), int(dy)
        new_x, new_y = gobject.move_it(dx, dy, dry=True)
        row, col = self.g_to_cell(new_x, new_y)
        if (0 <= row < self.rows) and (0 <= col < self.cols):
            if not self.cell(row, col).collision(gobject):
                self.del_gobject_from_cell(gobject)
                gobject.move_it(dx, dy)
                self.add_gobject_to_cell(gobject)
                return True, None
            return False, self.cell(row, col)
        return False, None

    def handle_keyboard_event(self, event):
        """handle_keyboard_event should process the keyboard event given.
        """
        # Log.Grid(self.name).KeyboardEvent(event.key).call()
        if self.running:
            # if self.catch_keyboard_gobject:
            #     key_pressed = pygame.key.get_pressed()
            #     Log.Grid(self.name).KeyboardEvent(event).GObject(self.catch_keyboard_gobject.name).call()
            #     if key_pressed[pygame.K_LEFT]:
            #         self.move_it_gobject(self.catch_keyboard_gobject, -self.g_cell_size.x, 0)
            #     if key_pressed[pygame.K_RIGHT]:
            #         self.move_it_gobject(self.catch_keyboard_gobject, self.g_cell_size.x, 0)
            #     if key_pressed[pygame.K_UP]:
            #         self.move_it_gobject(self.catch_keyboard_gobject, 0, -self.g_cell_size.y)
            #     if key_pressed[pygame.K_DOWN]:
            #         self.move_it_gobject(self.catch_keyboard_gobject, 0, self.g_cell_size.y)
            for gobj in [o for _, go in self.gobjects.items() for o in go]:
                gobj.handle_keyboard_event(event)

    def handle_mouse_event(self, event):
        """handle_mouse_event should process the mouse event given.
        Mouse events are passed to the active scene to be handle.
        """
        for gobj in [o for _, go in self.gobjects.items() for o in go]:
            gobj.handle_mouse_event(event)

    def handle_custom_event(self, event):
        """handle_custom_event should process pygame custom event given.
        Any object in the game, like, scene, graphic objects, ... can post
        customs events, and those should be handled at this time.
        """
        if event.destination == GEvent.BOARD and event.type == GEvent.CALLBACK:
            Log.Grid(self.name).Event(event.source).Payload(str(event.payload)).call()
            if event.subtype == GEvent.MOVE_TO:
                new_pos = pygame.math.Vector2(event.payload["validation"]())
                ok, _ = self.move_it_gobject(event.source, new_pos.x, new_pos.y)
                if ok:
                    event.payload["callback"]()
            elif event.subtype == GEvent.DELETE:
                self.del_gobject(event.source)
        for gobj in [o for _, go in self.gobjects.items() for o in go]:
            gobj.handle_custom_event(event)

    def update(self, surface, **kwargs):
        """update provides any functionality to be done every tick.
        """
        for gobj in [o for _, go in self.gobjects.items() for o in go]:
            gobj.update(surface)

    def render(self, surface, **kwargs):
        """render should draws the instance on the given surface.
        """
        if self.render_grid:
            for row in range(self.rows + 1):
                r = self.g_origin.y + (row * self.g_cell_size.y)
                pygame.draw.line(surface, Color.BLACK, (self.g_origin.x, r), (self.g_origin.x + self.g_size.x, r))
            for col in range(self.cols + 1):
                c = self.g_origin.x + (col * self.g_cell_size.x)
                pygame.draw.line(surface, Color.BLACK, (c, self.g_origin.y), (c, self.g_origin.y + self.g_size.y))

        for _, gobjects in self.gobjects.items():
            gobjects.draw(surface)
