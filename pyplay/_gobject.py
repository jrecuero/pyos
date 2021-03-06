import pygame

# from ._loggar import log
from ._gid import new_gid
from ._move import Move
from ._color import Color


class GObject(pygame.sprite.Sprite):
    """GObject contains all information related with any object to be
    placed or used by the GHandler.
    """

    NONE = 0
    RECT = 1
    CIRCLE = 2
    SHAPE = 3
    BOARD = 4
    POLYGON = 5
    IMAGE = 10
    TEXT = 20

    def __init__(self, name, x, y, dx, dy, **kwargs):
        super(GObject, self).__init__()
        self.__gid = new_gid()
        self.name = name
        self._x = x
        self._y = y
        self._dx = dx
        self._dy = dy
        self.image = pygame.Surface((dx, dy), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.ctype = kwargs.get("ctype", GObject.NONE)
        self.z = kwargs.get("z", 0)
        self.move = kwargs.get("move", Move())
        self.pushed = kwargs.get("pushed", None)
        self.enable = kwargs.get("enable", True)
        self.visible = kwargs.get("visible", True)
        self.solid = kwargs.get("solid", True)
        self.color = kwargs.get("color", Color.BLACK)
        self.outline = kwargs.get("outline", 0)
        self.catch_keyboard = kwargs.get("keyboard", False)
        self.content = kwargs.get("content", None)

    @property
    def gid(self):
        """gid property returns the graphical id.
        """
        return self.__gid

    @property
    def x(self):
        """x property returns the graphical object position in the X-axis.
        """
        return self._x

    @x.setter
    def x(self, val):
        """x setter sets the graphical object position in the X-axis and sync
        that with the rectangle that contains the object.
        """
        self._x = int(val)
        self.rect.x = self._x

    @property
    def y(self):
        """y property returns the graphical object position in the y-axis.
        """
        return self._y

    @y.setter
    def y(self, val):
        """y setter sets the graphical object position in the Y-axis and sync
        that with the rectangle that contains the object.
        """
        self._y = int(val)
        self.rect.y = self._y

    @property
    def dx(self):
        """dx property returns the graphical object width or X-axis size.
        """
        return self._dx

    @property
    def dy(self):
        """dy property returns the graphical object height or Y-axis size.
        """
        return self._dy

    def dxdy(self, dx=None, dy=None):
        """dxdy allows to set the graphical object width and height at the
        same time, X-axis and Y-axis dimensions.
        """
        self._dx = int(dx) if dx is not None else self._dx
        self._dy = int(dy) if dy is not None else self._dy
        self.image = pygame.transform.scale(self.image, (self._dx, self._dy))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def __str__(self):
        return f"[{self.gid}] : {self.__class__.__name__}@{self.name} | {self.x} {self.y} {self.dx} {self.dy} {self.ctype}"

    def reverse(self):
        """reverse inverts movement with the same speed value.
        """
        return self.move.reverse()

    def bounce_x(self):
        """bounce_x bounces against an X-plane, it means y-component will
        be reversed.
        """
        return self.move.bounce_x()

    def bounce_y(self):
        """bounce_y bounces against an Y-plane, it means x-component will
        be reversed.
        """
        return self.move.bounce_y()

    def move_inc(self, inc_x, inc_y):
        """move_inc moves the grafical object by the given x and y components.
        """
        self.x += inc_x
        self.y += inc_y

    def move_to(self, x, y):
        """move_to moves the grafical object to the given position.
        """
        self.x = x
        self.y = y

    def scale(self, dx, dy):
        """scale transfor the graphical object based on given x and y
        percentages.
        """
        self.dxdy(dx, dy)

    def start_tick(self):
        """start_tick should set all elements ready for a new tick.
        """
        pass

    def end_tick(self):
        """end_tick shoudl set all elements ready for the end of a tick. Any
        structure to be clean up can be done at this point.
        """
        pass

    def handle_keyboard_event(self, event):
        """handle_keyboard_event should process the keyboard event given.
        """
        return True

    def handle_custom_event(self, event):
        """handle_custom_event should process pygame custom event given.
        Any object in the game, like, scene, graphic objects, ... can post
        customs events, and those should be handled at this time.
        """
        return True

    def out_of_bounds_x_response(self):
        """out_of_bounds_x_response takes action when the graphical object is
        out of bound at the X-axis.
        Return True if objects is lost out of bound or False if object should
        be in bounds.
        """
        self.bounce_x()
        return False

    def handle_mouse_event(self, event):
        """handle_mouse_event should process the mouse event given.
        Mouse events are passed to the active scene to be handle.
        """
        pass

    def out_of_bounds_y_response(self):
        """out_of_bounds_x_response takes action when the graphical object is
        out of bound at the X-axis.
        Return True if objects is lost out of bound or False if object should
        be in bounds.
        """
        self.bounce_y()
        return False

    def collide_with(self, other):
        """collide_with processes a collision with other object.
        """
        pass

    def mouse_over(self, mouse_pos):
        """mouse_over is called when mouse is over the graphical object.
        """
        print(f"mouse {mouse_pos} is over me {self}")

    def update(self, surface, **kwargs):
        """update updates x and y compoments based on the move attribute
        x and y components.
        """
        self.move_inc(self.move.x, self.move.y)

    def render(self, surface, **kwargs):
        """render should draws the instance on the given surface.
        """
        pass
