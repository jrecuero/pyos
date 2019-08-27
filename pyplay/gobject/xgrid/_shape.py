import pygame
from ..._gid import new_gid
from ._cell import Cell
from ._collision_box import CollisionBox


class Shape:
    """Shape represents a collection of cells to be displayed in a grid board.
    """

    def __init__(self, name, cells=None, **kwargs):
        self.__gid = new_gid()
        self.name = name
        self.cells = cells if cells else []

    @property
    def gid(self):
        return self.__gid

    def add_cell(self, cell):
        """add_cell add a new cell to the shape.
        """
        self.cells.append(cell)

    def del_cell(self, cell):
        """del_cell deletes a cell from the shape.
        """
        if cell in self.cells:
            self.cells.remove(cell)

    def move_it(self, dx, dy):
        """move_it moves a shape the given X and Y offsets. Grid position
        and graphical position are stored and move delta is stored.
        """
        for cell in self.cells:
            cell.move_it(dx, dy)

    def handle_keyboard_event(self, event):
        """handle_keyboard_event should process the keyboard event given.
        """
        if event.key == pygame.K_LEFT:
            self.move_it(-1, 0)
        if event.key == pygame.K_RIGHT:
            self.move_it(1, 0)
        if event.key == pygame.K_UP:
            self.move_it(0, -1)
        if event.key == pygame.K_DOWN:
            self.move_it(0, 1)

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
        for cell in self.cells:
            cell.back_it()

    def out_of_bounds_y_response(self):
        """out_of_bounds_x_response takes action when the graphical object is
        out of bound at the X-axis.
        Return True if objects is lost out of bound or False if object should
        be in bounds.
        """
        for cell in self.cells:
            cell.back_it()

    def update(self, surface, **kwargs):
        for cell in self.cells:
            cell.update(surface, **kwargs)

    def render(self, surface, **kwargs):
        for cell in self.cells:
            cell.render(surface, **kwargs)
