import pygame
from ..._gid import new_gid
from ..._color import Color
from ..._move import Move
from ._collision_box import CollisionBox
from ._grid_event import GridEvent


class Shape:
    """Shape represents a collection of cells to be displayed in a grid board.
    """

    def __init__(self, name, x, y, xcells, ycells, xsize, ysize, cells=None, **kwargs):
        self.__gid = new_gid()
        self.name = name
        self.gridx = x
        self.gridy = y
        self.xcells = xcells
        self.ycells = ycells
        self.xsize = xsize
        self.ysize = ysize
        self.cells = cells if cells else []
        self.move = kwargs.get("move", Move())
        self.pushed = kwargs.get("pushed", None)
        self.color = kwargs.get("color", Color.BLACK)
        self.gravity = kwargs.get("gravity", True)
        self.allow_rotation = (
            kwargs.get("rotation", True) if (self.xcells == self.ycells) else False
        )
        self.allow_key_handle = kwargs.get("hkey", False)
        self.transient = kwargs.get("transient", False)
        self.gravity_step = False
        self.is_rotation = False
        self.dx_move = xsize
        self.dy_move = ysize

        for cell in self.cells:
            cell.incr_xy(self.gridx, self.gridy)
            cell.move = self.move

    @property
    def gid(self):
        return self.__gid

    def __str__(self):
        return f"[{self.gid}] : {self.__class__.__name__}@{self.name} | {self.gridx} {self.gridy}"

    def add_cell(self, cell):
        """add_cell add a new cell to the shape.
        """
        cell.incr_xy(self.gridx, self.gridy)
        cell.move = self.move
        self.cells.append(cell)

    def del_cell(self, cell):
        """del_cell deletes a cell from the shape.
        """
        if cell in self.cells:
            self.cells.remove(cell)

    def move_it(self, dx, dy, update=True):
        """move_it moves a shape the given X and Y offsets. Grid position
        and graphical position are stored and move delta is stored. It moreover
        updates gridx and gridy attributes if update flag is True.
        """
        self.is_rotation = False
        if update:
            self.gridx += dx
            self.gridy += dy
        for cell in self.cells:
            cell.move_it(dx, dy)

    def back_it(self):
        """back_it moves back all cells in the shape move. It basically the
        reverse operation for move_it().
        """
        result = []
        for cell in self.cells:
            result.append(cell.back_it())
        # Rotation does not update grid position, so they should not be changed
        # back now.
        if not self.is_rotation:
            backx, backy = result[-1]
            self.gridx -= backx
            self.gridy -= backy
        return result

    def rotate_clockwise(self):
        """rotate_clockwise rotates the shape by 90 degrees clockwise.
        """
        if not self.allow_rotation:
            return
        self.is_rotation = True
        for cell in self.cells:
            gridx = cell.gridx - self.gridx
            gridy = cell.gridy - self.gridy
            deltax = self.xcells - 1 - gridy - gridx
            deltay = gridx - gridy
            cell.move_it(deltax, deltay)

    def rotate_anticlockwise(self):
        """rotate_anticlockwise rotates the shape by 90 degrees anti-clockwise.
        """
        if not self.allow_rotation:
            return
        self.is_rotation = True
        for cell in self.cells:
            gridx = cell.gridx - self.gridx
            gridy = cell.gridy - self.gridy
            deltay = self.xcells - 1 - gridx - gridy
            deltax = gridy - gridx
            cell.move_it(deltax, deltay)

    def handle_keyboard_event(self, event):
        """handle_keyboard_event should process the keyboard event given.
        """
        if not self.allow_key_handle:
            return
        self.gravity_step = False
        if event.key == pygame.K_LEFT:
            self.move_it(-1, 0)
        if event.key == pygame.K_RIGHT:
            self.move_it(1, 0)
        if event.key == pygame.K_UP:
            self.move_it(0, -1)
        if event.key == pygame.K_DOWN:
            self.move_it(0, 1)
        if event.key == pygame.K_SPACE:
            self.rotate_clockwise()

    def gravity_move(self, steps):
        """gravity_move represents a gravity movement down the board for the
        given number of steps. This movement can be called only one time for
        every tick.
        """
        if not self.gravity_step:
            self.gravity_step = True
            self.move_it(0, steps)

    def handle_custom_event(self, event):
        """handle_custom_event should process pygame custom event given.
        Any object in the game, like, scene, graphic objects, ... can post
        customs events, and those should be handled at this time.
        """
        if self.gravity and event.type == GridEvent.GRAVITY:
            self.gravity_move(1)

    def get_collision_box(self):
        """get_collision_box retrieves collision box for all cells containes
        in the shape.
        """
        collision_box = CollisionBox()
        for cell in self.cells:
            collision_box.update(cell.get_collision_box())
        return collision_box

    def out_of_bounds_x_response(self):
        """out_of_bounds_x_response takes action when the graphical object is
        out of bound at the X-axis.
        Return True if objects is lost out of bound or False if object should
        be in bounds.
        """
        return self.out_of_bounds_response()

    def out_of_bounds_y_response(self):
        """out_of_bounds_x_response takes action when the graphical object is
        out of bound at the X-axis.
        Return True if objects is lost out of bound or False if object should
        be in bounds.
        """
        return self.out_of_bounds_response()

    def out_of_bounds_response(self):
        """out_of_bounds_x_response takes action when the graphical object is
        out of bound at the X-axis or Y-axis
        Return True if objects is lost out of bound or False if object should
        be in bounds.
        """
        for cell in self.cells:
            cell.back_it()

    def collide_with(self, other, collision):
        """collide_with processes a collision with other object.
        """
        for cell in self.cells:
            cell.back_it()

    def update(self, surface, **kwargs):
        """update provides any functionality to be done every tick.
        """
        for cell in self.cells:
            cell.update(surface, **kwargs)

    def render(self, surface, **kwargs):
        """render should draws the instance on the given surface.
        """
        self.gravity_step = False
        for cell in self.cells:
            cell.render(surface, **kwargs)
