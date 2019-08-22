from ._point import Point
from ._move import Move


class GObject:
    """GObject contains all information related with any object to be
    placed or used by the GHandler.
    """

    __GID = 0

    NONE = 0
    RECT = 1
    SHAPE = 2
    BOARD = 3
    IMAGE = 10
    TEXT = 20

    def __init__(self, name, **kwargs):
        GObject.__GID += 1
        self.__gid = GObject.__GID
        self.name = name
        self.content = kwargs.get("content", None)
        self.ctype = kwargs.get("ctype", GObject.NONE)
        self.pos = kwargs.get("pos", None)
        self.move = kwargs.get("move", Move())
        self.pushed = kwargs.get("pushed", None)
        self.enable = kwargs.get("enable", True)
        self.visible = kwargs.get("visible", True)
        self.solid = kwargs.get("solid", True)

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
        if self.pos is None:
            self.pos = Point(val, 0)
        else:
            self.pos.x = val

    @property
    def y(self):
        return self.pos.y if self.pos else None

    @y.setter
    def y(self, val):
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

    def update(self, surface, **kwargs):
        pass

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
