from typing import List, Any, Dict

import curses
import random
from engine import (
    # log,
    EVT,
    Handler,
    Scene,
    Event,
    NObject,
    # Char,
    # String,
    Box,
    Caller,
    KeyHandler,
    update_scene,
    render_scene,
    update_nobj,
    render_nobj,
)


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

    def dec(self, y: int = None, x: int = None):
        self._y = self.y if y is None else (self.y - y)
        self._x = self.x if x is None else (self.x - x)

    def get(self):
        return (self.y, self.x)

    def __eq__(self, other: "Point") -> bool:
        return (self.x == other.x) and (self.y == other.y)

    def __ne__(self, other: "Point") -> bool:
        return (self.x != other.x) or (self.y != other.y)


class Move(object):

    NONE: int = 0
    UP: int = 1
    DOWN: int = 2
    RIGHT: int = 3
    LEFT: int = 4

    @staticmethod
    def allowed(move: int, to_move: int):
        if (move in [Move.UP, Move.DOWN]) and (to_move in [Move.UP, Move.DOWN]):
            return False
        elif (move in [Move.LEFT, Move.RIGHT]) and (to_move in [Move.LEFT, Move.RIGHT]):
            return False
        return True

    @staticmethod
    def left_or_right():
        return random.choice([Move.RIGHT, Move.LEFT])

    @staticmethod
    def up_or_down():
        return random.choice([Move.DOWN, Move.UP])

    @staticmethod
    def any():
        return random.choice([Move.DOWN, Move.UP, Move.LEFT, Move.RIGHT])


class Link(object):
    def __init__(
        self,
        sprite: str,
        pos: Point = None,
        move: int = Move.NONE,
        pushed: bool = False,
    ):
        self.sprite: str = sprite
        self.move: int = move
        self.pushed: bool = pushed
        self.pos: Point = Point(0, 0) if pos is None else pos

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

    def draw(self):
        return [self.y, self.x, self.sprite]


class Entity(object):
    def __init__(self):
        self.shape: List[Link] = []
        self.timeout: int = 0

    @property
    def head(self) -> Link:
        if len(self.shape):
            return self.shape[0]
        return None

    def update(self, timeout: int = 0) -> bool:
        if timeout:
            self.timeout += 1
            if timeout > self.timeout:
                return False
            self.timeout = 0
        return True

    def draw(self):
        result: List = []
        for link in self.shape:
            result.append(link.draw())
        return result


class Chain(object):
    def __init__(self, length: int, sprite: str):
        self.timeout: int = 0
        self.shape: List[Link] = []
        for _ in range(length):
            self.shape.append(Link(sprite))

    @property
    def head(self) -> Link:
        if len(self.shape):
            return self.shape[0]
        return None

    def start_at(self, move: int, start_pos: Point):
        for link in self.shape:
            link.pos = start_pos
            link.move = move
            link.pushed = False
            start_pos.x -= 1

    def add_link(self, sprite: str):
        new_link = Link(sprite)
        last_link = self.shape[-1]
        new_link.move = last_link.move
        if new_link.move == Move.UP:
            new_link.pos = Point(last_link.y + 1, last_link.x)
        elif new_link.move == Move.DOWN:
            new_link.pos = Point(last_link.y - 1, last_link.x)
        elif new_link.move == Move.RIGHT:
            new_link.pos = Point(last_link.y, last_link.x - 1)
        elif new_link.move == Move.LEFT:
            new_link.pos = Point(last_link.y, last_link.x + 1)
        self.shape.append(new_link)

    def update(self, timeout: int = 0):
        if timeout:
            self.timeout += 1
            if timeout > self.timeout:
                return
            self.timeout = 0
        pushed: bool = False
        pushed_move: int = Move.NONE
        next_pushed: bool = False
        next_pushed_move: int = Move.NONE
        for link in self.shape:
            if link.move == Move.UP:
                link.y = link.y - 1
            elif link.move == Move.DOWN:
                link.y = link.y + 1
            elif link.move == Move.RIGHT:
                link.x = link.x + 1
            elif link.move == Move.LEFT:
                link.x = link.x - 1
            else:
                pass
            if link.pushed:
                next_pushed = link.pushed
                next_pushed_move = link.move
            else:
                next_pushed = False
                next_pushed_move = Move.NONE
            if pushed:
                link.pushed = True
                link.move = pushed_move
            else:
                link.pushed = False
            pushed = next_pushed
            pushed_move = next_pushed_move

    def move_to(self, move: int):
        # head = self.shape[0]
        if Move.allowed(self.head.move, move):
            self.head.pushed = True
            self.head.move = move

    def wall_collision(self, max_y: int, max_x: int) -> bool:
        if (self.head.move == Move.UP) and (self.head.y == 1):
            if self.head.x == 1:
                self.move_to(Move.RIGHT)
            else:
                self.move_to(Move.left_or_right())
            return True
        elif (self.head.move == Move.DOWN) and (self.head.y == max_y - 2):
            if self.head.x == 1:
                self.move_to(Move.RIGHT)
            else:
                self.move_to(Move.left_or_right())
            return True
        elif (self.head.move == Move.LEFT) and (self.head.x == 1):
            if self.head.y == 1:
                self.move_to(Move.DOWN)
            else:
                self.move_to(Move.up_or_down())
            return True
        elif (self.head.move == Move.RIGHT) and (self.head.x == max_x - 2):
            if self.head.y == 1:
                self.move_to(Move.DOWN)
            else:
                self.move_to(Move.up_or_down())
            return True
        return False

    def check_collision(self, screen, collisions: str) -> str:
        # if chr(screen.inch(self.shape[0].pos[0], self.shape[0].pos[1]) & 255) == "*":
        obj = chr(screen.inch(self.head.y, self.head.x) & 255)
        if obj in collisions:
            self.add_link("#")
            return obj
        return None

    def draw(self):
        result: List = []
        for link in self.shape:
            result.append(link.draw())
        return result


class Octopus(Entity):
    def __init__(self, y: int, x: int, sprite: str):
        super(Octopus, self).__init__()
        self.shape.append(Link(sprite, pos=Point(y, x)))
        self.move_timeout: int = random.randint(1, 10)
        self.move_counter: int = 0
        self.atk_timeout: int = 10
        self.atk_life: int = 5
        self.atk_counter: int = 0
        self.head.move = Move.any()

    def update(self, timeout: int = 0) -> bool:
        if not super(Octopus, self).update(timeout):
            return False
        self.atk_counter += 1
        if self.atk_counter == self.atk_timeout:
            self.shape.append(
                Link(self.head.sprite, pos=Point(self.head.y, self.head.x - 1))
            )
            self.shape.append(
                Link(self.head.sprite, pos=Point(self.head.y, self.head.x + 1))
            )
            self.shape.append(
                Link(self.head.sprite, pos=Point(self.head.y - 1, self.head.x))
            )
            self.shape.append(
                Link(self.head.sprite, pos=Point(self.head.y + 1, self.head.x))
            )
            return True
        elif self.atk_timeout < self.atk_counter < (self.atk_timeout + self.atk_life):
            return True
        elif self.atk_counter == (self.atk_timeout + self.atk_life):
            self.shape = self.shape[:1]
            self.atk_counter = 0
            return True
        self.move_counter += 1
        if self.move_counter == self.move_timeout:
            self.head.move = Move.any()
            self.move_counter = 0
            self.move_timeout = random.randint(1, 10)
        if self.head.move == Move.UP:
            self.head.y -= 1
        elif self.head.move == Move.DOWN:
            self.head.y += 1
        elif self.head.move == Move.LEFT:
            self.head.x -= 1
        elif self.head.move == Move.RIGHT:
            self.head.x += 1
        return True

    def wall_collision(self, max_y: int, max_x: int):
        if self.head.y < 2:
            self.head.y = 2
        elif self.head.y > (max_y - 2):
            self.head.y = max_y - 2
        if self.head.x < 2:
            self.head.x = 2
        elif self.head.x > (max_x - 2):
            self.head.x = max_x - 2


class Stone(NObject):
    def __init__(
        self, y: int, x: int, sprite: str, timeout: int, max_y: int, max_x: int
    ):
        super(Stone, self).__init__(y, x, -1, -1)
        self.sprite: str = sprite
        self.timeout: int = timeout
        self.counter: int = 0
        self.max_y: int = max_y
        self.max_x: int = max_x

    def wall_collision(self, max_y: int, max_x: int):
        if self.y < 2:
            self.y = 2
        elif self.y > (max_y - 2):
            self.y = max_y - 2
        if self.x < 2:
            self.x = 2
        elif self.x > (max_x - 2):
            self.x = max_x - 2

    @update_nobj
    def update(self, screen: Any, *events: Event) -> List[Event]:
        self.counter += 1
        if self.counter > self.timeout:
            self.counter = 0
            self.x += random.randint(-1, 1)
            self.y += random.randint(-1, 1)
            self.wall_collision(self.max_y, self.max_x)
        return []

    @render_nobj
    def render(self, screen) -> List[Event]:
        screen.addch(self.y, self.x, self.sprite)
        return []


class BoardHandler(object):
    def __init__(self, max_y: int, max_x: int):
        self.max_y: int = max_y
        self.max_x: int = max_x
        self.board: List = [
            [None for x in range(self.max_x)] for y in range(self.max_y)
        ]
        self.snake: Chain = Chain(1, "#")
        self.snake.start_at(Move.any(), Point(15, 15))
        self.octopus: Octopus = Octopus(10, 10, "@")
        self.patterns: Dict[str, int] = dict([(str(x), x) for x in range(1, 10)])
        self.colliders: List = []
        self.score: int = 0

    def _new_collider(self, max_y: int, max_x: int) -> List:
        return Link(
            random.choice(list(self.patterns.keys())),
            pos=Point(random.randint(2, max_y - 3), random.randint(2, max_x - 2)),
        )

    def new_collider(self, max_y: int, max_x: int) -> List:
        self.colliders = []
        self.colliders.append(self._new_collider(max_y, max_x))

    def update(self):
        self.snake.update(5)
        self.octopus.update(20)

    def wall_collision(self, max_y: int, max_x: int):
        self.octopus.wall_collision(max_y, max_x)
        self.snake.wall_collision(max_y, max_x)

    def collision(self, screen: Any, max_y: int, max_x: int) -> bool:
        self.wall_collision(max_y, max_x)
        for hit in self.colliders:
            if hit.pos == self.snake.head.pos:
                self.score += self.patterns[hit.sprite]
                self.new_collider(max_y, max_x)
                return True
        return False

    def move_snake(self, move_to: int):
        def _move_snake():
            self.snake.move_to(move_to)
            return []

        return _move_snake

    def draw_score(self):
        return [[0, 3, " [ Score: {} ] ".format(self.score)]]

    def draw_collider(self):
        result: List = []
        for obj in self.colliders:
            result.append([obj.y, obj.x, obj.sprite])
        return result


class BoardScene(Scene):
    def __init__(self):
        super(BoardScene, self).__init__("Board Scene")
        self.border = False
        self.max_y: int = curses.LINES - 1
        self.max_x: int = curses.COLS - 1
        self.sh: BoardHandler = BoardHandler(self.max_y, self.max_x)

    def setup(self, screen: Any):

        # self.max_x, self.max_y = screen.getmaxyx()
        # self.max_y, self.max_x = curses.LINES - 1, curses.COLS - 1
        self.sh.new_collider(self.max_y, self.max_x)
        self.add_object(Box(0, 0, self.max_y - 1, self.max_x))
        self.add_object(Stone(10, 10, "S", 10, self.max_y, self.max_x))
        self.add_object(Caller(-1, -1, self.sh.draw_score))
        self.add_object(Caller(-1, -1, self.sh.snake.draw))
        self.add_object(Caller(-1, -1, self.sh.octopus.draw))
        self.add_object(Caller(-1, -1, self.sh.draw_collider))
        self.kh = KeyHandler({})
        self.kh.register("x", lambda: exit(0))
        self.kh.register(chr(curses.KEY_LEFT), self.sh.move_snake(Move.LEFT))
        self.kh.register(chr(curses.KEY_RIGHT), self.sh.move_snake(Move.RIGHT))
        self.kh.register(chr(curses.KEY_UP), self.sh.move_snake(Move.UP))
        self.kh.register(chr(curses.KEY_DOWN), self.sh.move_snake(Move.DOWN))

    @update_scene
    def update(self, screen: Any, *events: Event) -> List[Event]:
        event_to_return: List[Event] = []
        for event in events:
            if event.evt == EVT.ENG.KEY:
                event_to_return.extend(self.kh.update(event))
        self.sh.update()
        return event_to_return

    @render_scene
    def render(self, screen: Any) -> List[Event]:
        self.sh.collision(screen, self.max_y, self.max_x)
        return super(BoardScene, self).render(screen)


if __name__ == "__main__":
    h = Handler()
    h.add_scene(BoardScene())
    h.run()
