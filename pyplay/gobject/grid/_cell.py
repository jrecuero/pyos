import pygame
from ..._move import Move
from ..._color import Color
from ._collision_box import CollisionBox


class Cell(pygame.rect.Rect):
    """Cell represents every entry in the graphical grid.
    """

    def __init__(self, name, x, y, dx, dy, **kwargs):
        super(Cell, self).__init__(x, y, dx, dy)
        self.name = name
        # self.x = x
        # self.y = y
        self.z = kwargs.get("z", 0)
        # self.dx = dx
        # self.dy = dy
        self.gridx = x
        self.gridy = y
        self.image = None
        # self.rect = pygame.rect.Rect(x, y, dx, dy)
        self.move = kwargs.get("move", Move())
        self.pushed = kwargs.get("pushed", None)
        self.enable = kwargs.get("enable", True)
        self.visible = kwargs.get("visible", True)
        self.solid = kwargs.get("solid", True)
        self.color = kwargs.get("color", Color.BLACK)
        self.outline = kwargs.get("outline", 0)
        self.content = kwargs.get("content", None)
        self.stepx = None
        self.stepy = None
        self.dx_move = dx
        self.dy_move = dy

    # @property
    # def x(self):
    #     return self.rect.x
    #
    # @x.setter
    # def x(self, val):
    #     self.rect.x = val
    #
    # @property
    # def y(self):
    #     return self.rect.y
    #
    # @y.setter
    # def y(self, val):
    #     self.rect.y = val
    #
    # @property
    # def dx(self):
    #     return self.rect.width
    #
    # @property
    # def dy(self):
    #     return self.rect.height

    def __str__(self):
        return f"{self.__class__.__name__} | {self.x} {self.y} {self.width} {self.height} {self.gridx} {self.gridy}"

    def incr_xy(self, dx=0, dy=0):
        """incr_xy increases values properly for x and gridx, y and gridy with
        the given increments.
        """
        self.x += dx
        self.gridx += dx
        self.y += dy
        self.gridy += dy

    def get_collision_box(self):
        """get_collision_box retrieves grid cells that can collide with any
        other cell.
        """
        collision_box = CollisionBox()
        collision_box.add(self.gridx, self.gridy)
        return collision_box

    def move_it(self, dx=0, dy=0):
        """move_it moves a cell the given X and Y offsets. Grid position and
        graphical position are stored and move delta is stored.
        """
        self.gridx += dx
        self.gridy += dy
        self.x += dx * self.width
        self.y += dy * self.height
        self.stepx = dx
        self.stepy = dy

    def back_it(self):
        """back_it moves back last cell move. It is basically the reverse
        operation for move_it().
        """
        if self.stepx is not None and self.stepy is not None:
            result = self.stepx, self.stepy
            self.gridx -= self.stepx
            self.gridy -= self.stepy
            self.x -= self.stepx * self.width
            self.y -= self.stepy * self.height
            self.stepx = None
            self.stepy = None
            return result
        return 0, 0

    def update(self, surface, **kwargs):
        """update provides any functionality to be done every tick.
        """
        # dx_move and dy_move are required in order to sync non-grid
        # movement with grid positioning. That allows objects to move any
        # distance but keep proper position in the grid.
        if self.move.x:
            self.x += self.move.x
            self.dx_move += abs(self.move.x)
            if self.dx_move > self.width:
                self.dx_move -= self.width
                if self.move.is_right():
                    self.gridx += 1
                if self.move.is_left():
                    self.gridx -= 1
        if self.move.y:
            self.y += self.move.y
            self.dy_move += abs(self.move.y)
            if self.dy_move > self.height:
                self.dy_move -= self.height
                if self.move.is_down():
                    self.gridy += 1
                if self.move.is_up():
                    self.gridy -= 1

    def render(self, surface, **kwargs):
        """render should draws the instance on the given surface.
        """
        # pygame.draw.rect(
        #     surface, self.color, (self.x, self.y, self.rect.width, self.rect.height)
        # )
        pygame.draw.rect(surface, self.color, self)
