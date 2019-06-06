from typing import List, Any, Set
import random
import curses

# from ._loggar import log
from ._event import Event
from ._nobject import NObject, pinput, update, render


class Point(object):
    def __init__(self, y: int, x: int):
        self._y: int = y
        self._x: int = x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, val):
        self._y = val

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, val):
        self._x = val

    def set(self, y: int = None, x: int = None):
        self._y = self.y if y is None else y
        self._x = self.x if x is None else x

    def inc(self, y: int = None, x: int = None):
        self._y = self.y if y is None else (self.y + y)
        self._x = self.x if x is None else (self.x + x)

    def incr(self, y: int = None, x: int = None):
        y = self.y if y is None else (self.y + y)
        x = self.x if x is None else (self.x + x)
        return Point(y, x)

    def dec(self, y: int = None, x: int = None):
        self._y = self.y if y is None else (self.y - y)
        self._x = self.x if x is None else (self.x - x)

    def decr(self, y: int = None, x: int = None):
        y = self.y if y is None else (self.y - y)
        x = self.x if x is None else (self.x - x)
        return Point(y, x)

    def __add__(self, other):
        p = Point(self.y, self.x)
        if isinstance(other, int):
            p = Point(self.y + other, self.x + other)
        elif isinstance(self, Point):
            p = Point(self.y + other.y, self.x + other.x)
        return p

    def __sub__(self, other):
        p = Point(self.y, self.x)
        if isinstance(other, int):
            p = Point(self.y - other, self.x - other)
        elif isinstance(self, Point):
            p = Point(self.y - other.y, self.x - other.x)
        return p

    def __mul__(self, other):
        p = Point(self.y, self.x)
        if isinstance(other, int):
            p = Point(self.y * other, self.x * other)
        elif isinstance(self, Point):
            p = Point(self.y * other.y, self.x * other.x)
        return p

    def get(self):
        return (self.y, self.x)

    def __eq__(self, other: "Point") -> bool:
        return (self.x == other.x) and (self.y == other.y)

    def __ne__(self, other: "Point") -> bool:
        return (self.x != other.x) or (self.y != other.y)

    def inside(self, y: int, x: int, max_y: int, max_x: int) -> bool:
        return (y < self.y < y + max_y) and (x < self.x < x + max_x)

    def __str__(self):
        return "({}, {})".format(self.y, self.x)

    def hash(self):
        return (self.y, self.x)


class Move(object):

    NONE: int = 0
    UP: int = 1
    DOWN: int = 2
    RIGHT: int = 3
    LEFT: int = 4

    @staticmethod
    def to_string(move: int):
        _to_string = {
            Move.NONE: "none",
            Move.UP: "up",
            Move.DOWN: "down",
            Move.LEFT: "left",
            Move.RIGHT: "right",
        }
        return _to_string.get(move, "none")

    @staticmethod
    def left_or_right():
        return random.choice([Move.RIGHT, Move.LEFT])

    @staticmethod
    def up_or_down():
        return random.choice([Move.DOWN, Move.UP])

    @staticmethod
    def any():
        return random.choice([Move.DOWN, Move.UP, Move.LEFT, Move.RIGHT])


class BB(object):
    """BB class is the building block for any physic shape.
    """

    def __init__(self, sprite: str, **kwargs):
        self.sprite: str = sprite
        self.pos: Point = kwargs.get("pos", Point(0, 0))
        self.pushed: bool = kwargs.get("pushed", False)
        self.move: int = kwargs.get("move", Move.NONE)
        self.fmt = kwargs.get("fmt", curses.A_NORMAL)
        self.solid: bool = kwargs.get("solid", True)
        self.visible: bool = kwargs.get("visible", True)
        self.prev_pos: Point = self.pos

    @property
    def y(self):
        return self.pos.y

    @y.setter
    def y(self, val):
        self.pos.y = val

    @property
    def x(self):
        return self.pos.x

    @x.setter
    def x(self, val):
        self.pos.x = val

    def next(self, pos: Point):
        self.prev_pos = Point(self.pos.y, self.pos.x)
        self.pos = pos

    def back(self):
        self.pos = self.prev_pos

    def draw(self):
        return [self.y, self.x, self.sprite]

    def render(self, screen: Any) -> List[Event]:
        screen.addnstr(self.y, self.x, self.sprite, 1, self.fmt)
        return []


class Shape(object):
    def __init__(self, **kwargs):
        super(Shape, self).__init__()
        self.__n = 0
        self.shape: List[BB] = []
        self._counter: int = 0
        self._timeout: int = kwargs.get("timeout", 0)
        self.visible: bool = kwargs.get("visible", True)
        self.solid: bool = kwargs.get("solid", True)
        self.movable: bool = kwargs.get("movable", True)
        self.layer: int = kwargs.get("layer", 0)
        # self.delta: Point = Point(1, 0)
        self.delta: Point = Point(0, 1)

    def __getitem__(self, i):
        if len(self.shape) > i:
            return self.shape[i]
        return None

    def __setitem__(self, i, v):
        if len(self.shape) > i:
            self.shape[i] = v

    def __len__(self):
        return len(self.shape)

    def __iter__(self):
        self.__n = 0
        return self

    def __next__(self):
        if self.__n < len(self.shape):
            result = self.shape[self.__n]
            self.__n += 1
            return result
        else:
            raise StopIteration

    def append(self, v):
        self.shape.append(v)
        return self

    @property
    def head(self) -> BB:
        return self[0]

    def back(self):
        for bb in self.shape:
            bb.back()
        self.delta = self.delta * -1

    def out_of_bounds(self, y: int, x: int, max_y: int, max_x: int) -> bool:
        for i, bb in enumerate(self.shape):
            if not bb.pos.inside(y, x, max_y, max_x):
                self.back()
                return True
        return False

    def collision_with(self, other: "Shape") -> bool:
        collision: Set = set()
        for bb in self.shape:
            collision.add(bb.pos.hash())
        for bb in other:
            collision.add(bb.pos.hash())
        return len(collision) < (len(self.shape) + len(other))

    def _update(self) -> bool:
        self._counter += 1
        if self._timeout > self._counter:
            return False
        self._counter = 0
        return True

    def update(self, screen: Any) -> List[Event]:
        result: List[Event] = []
        if self.movable and self._update():
            for bb in self.shape:
                bb.next(bb.pos + self.delta)
        return result

    def draw(self):
        result: List = []
        for bb in self.shape:
            result.append(bb.draw())
        return result

    def render(self, screen: Any) -> List[Event]:
        result: List[Event] = []
        for bb in self.shape:
            result.extend(bb.render(screen))
        return result


class Arena(NObject):
    def __init__(self, y: int, x: int, max_y: int, max_x: int, **kwargs):
        super(Arena, self).__init__(x, y, max_y, max_x)
        self.shapes: List[Shape] = []
        self._border_fmt = kwargs.get("border_fmt", curses.A_NORMAL)

    def add_shape(self, shape: Shape):
        for bb in shape:
            bb.y += self.y
            bb.x += self.x
        self.shapes.append(shape)

    def out_of_bounds(self):
        for shape in self.shapes:
            shape.out_of_bounds(self.y, self.x, self.dy, self.dx)

    def collision(self):
        for shape in [s for s in self.shapes if s.movable]:
            others = list(self.shapes)
            for other in [o for o in others if o != shape]:
                if shape.collision_with(other):
                    shape.back()
                    break

    @pinput
    def pinput(self, screen: Any, keys) -> List[Event]:
        return []

    @update
    def update(self, screen: Any, *events: Event) -> List[Event]:
        result: List[Event] = []
        for shape in self.shapes:
            result.extend(shape.update(screen))
            self.out_of_bounds()
            self.collision()
        return result

    @render
    def render(self, screen: Any) -> List[Event]:
        result: List[Event] = []
        self.box(screen, self._border_fmt)
        for shape in self.shapes:
            result.extend(shape.render(screen))
        return result