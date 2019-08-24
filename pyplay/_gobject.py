# from ._loggar import log
from ._point import Point
from ._move import Move
from ._color import Color


class GObject:
    """GObject contains all information related with any object to be
    placed or used by the GHandler.
    """

    __GID = 0

    NONE = 0
    RECT = 1
    CIRCLE = 2
    SHAPE = 3
    BOARD = 4
    POLYGON = 5
    IMAGE = 10
    TEXT = 20

    def __init__(self, name, **kwargs):
        GObject.__GID += 1
        self.__gid = GObject.__GID
        self.name = name
        self.content = kwargs.get("content", None)
        self.ctype = kwargs.get("ctype", GObject.NONE)
        self.x = kwargs.get("x", None)
        self.y = kwargs.get("y", None)
        self.z = kwargs.get("z", 0)
        self.pos = kwargs.get("pos", None)
        self.move = kwargs.get("move", Move())
        self.pushed = kwargs.get("pushed", None)
        self.enable = kwargs.get("enable", True)
        self.visible = kwargs.get("visible", True)
        self.solid = kwargs.get("solid", True)
        self.color = kwargs.get("color", Color.BLACK)
        self.outline = kwargs.get("outline", 0)
        self.catch_keyboard = kwargs.get("keyboard", False)

    @property
    def gid(self):
        return self.__gid

    def __str__(self):
        return f"[{self.gid}] : {self.__class__.__name__}@{self.name} | {self.ctype}"

    @property
    def x(self):
        return self.pos.x if self.pos else None

    @x.setter
    def x(self, val):
        if val is not None:
            if self.pos is None:
                self.pos = Point(val, 0)
            else:
                self.pos.x = val

    @property
    def y(self):
        return self.pos.y if self.pos else None

    @y.setter
    def y(self, val):
        if val is not None:
            if self.pos is None:
                self.pos = Point(0, val)
            else:
                self.pos.y = val

    def bounds(self):
        """bounds should returns a rectangle that contains the whole
        graphical object.
        """
        pass

    def set_content(self, content, ctype):
        self.content = content
        self.ctype = ctype

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
        self.x += int(inc_x)
        self.y += int(inc_y)

    def move_to(self, x, y):
        """move_to moves the grafical object to the given position.
        """
        self.x = int(x)
        self.y = int(y)

    def scale(self, dx, dy):
        """scale transfor the graphical object based on given x and y
        percentages.
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

    def out_of_bounds_y_response(self):
        """out_of_bounds_y_response takes action when the graphical object is
        out of bound at the Y-axis.
        Return True if objects is lost out of bound or False if object should
        be in bounds.
        """
        self.bounce_y()
        return False

    def collide_with(self, other):
        """collide_with processes a collision with other object.
        """
        pass

    def update(self, surface, **kwargs):
        """update updates x and y compoments based on the move attribute
        x and y components.
        """
        self.move_inc(self.move.x, self.move.y)

    def render(self, surface, **kwargs):
        if self.ctype == GObject.NONE:
            pass
        elif self.ctype == GObject.RECT:
            pass
        elif self.ctype == GObject.SHAPE:
            pass
        elif self.ctype == GObject.IMAGE:
            pass
        elif self.ctype == GObject.TEXT:
            pass
        else:
            pass
