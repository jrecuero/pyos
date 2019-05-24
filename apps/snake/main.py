from typing import List, Any, Dict

import curses
import random
from engine import (
    # log,
    EVT,
    Handler,
    Scene,
    Event,
    # Char,
    # String,
    Box,
    Caller,
    KeyHandler,
    update_scene,
    render_scene,
)


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
    def __init__(self, sprite: str, move: int = Move.NONE, pushed: bool = False):
        self.sprite: str = sprite
        self.move: int = move
        self.pushed: bool = pushed
        self.pos: List = [0, 0]

    @property
    def y(self):
        return self.pos[0]

    @y.setter
    def y(self, val):
        self.pos[0] = val

    @property
    def x(self):
        return self.pos[1]

    @x.setter
    def x(self, val):
        self.pos[1] = val


class Chain(object):
    def __init__(self, length: int, sprite: str):
        self._timeout: int = 0
        self.chain: List[Link] = []
        for _ in range(length):
            self.chain.append(Link(sprite))

    @property
    def head(self) -> Link:
        if len(self.chain):
            return self.chain[0]
        return None

    def start_at(self, move: int, start_pos: List):
        for link in self.chain:
            link.pos = list(start_pos)
            link.move = move
            link.pushed = False
            start_pos[1] -= 1

    def add_link(self, sprite: str):
        new_link = Link(sprite)
        last_link = self.chain[-1]
        new_link.move = last_link.move
        if new_link.move == Move.UP:
            new_link.pos = [last_link.y + 1, last_link.x]
        elif new_link.move == Move.DOWN:
            new_link.pos = [last_link.y - 1, last_link.x]
        elif new_link.move == Move.RIGHT:
            new_link.pos = [last_link.y, last_link.x - 1]
        elif new_link.move == Move.LEFT:
            new_link.pos = [last_link.y, last_link.x + 1]
        self.chain.append(new_link)

    def tick(self, timeout: int = 0):
        if timeout:
            self._timeout += 1
            if timeout > self._timeout:
                return
            self._timeout = 0
        pushed: bool = False
        pushed_move: int = Move.NONE
        next_pushed: bool = False
        next_pushed_move: int = Move.NONE
        for link in self.chain:
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
        # head = self.chain[0]
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
        # if chr(screen.inch(self.chain[0].pos[0], self.chain[0].pos[1]) & 255) == "*":
        obj = chr(screen.inch(self.head.y, self.head.x) & 255)
        if obj in collisions:
            self.add_link("#")
            return obj
        return None

    def draw(self, screen):
        for link in self.chain:
            screen.addstr(link.y, link.x, link.sprite)


def draw_box(screen: Any, y: int, x: int, dy: int, dx: int):
    for _x in range(1, dx):
        screen.addch(y, x + _x, chr(9473))
    for _x in range(1, dx):
        screen.addch(y + dy, x + _x, chr(9473))
    for _y in range(1, dy):
        screen.addch(y + _y, x, chr(9475))
    for _y in range(1, dy):
        screen.addch(y + _y, x + dx - 1, chr(9475))
    screen.addch(y, x, chr(9487))
    screen.addch(y + dy, x, chr(9495))
    screen.addch(y, x + dx - 1, chr(9491))
    screen.addch(y + dy, x + dx - 1, chr(9499))


class SnakeHandler(object):
    def __init__(self):
        self.snake: Chain = Chain(1, "#")
        self.snake.start_at(Move.any(), [15, 15])
        # self.patterns: Dict[str, int] = {"*": 10, "$": 20, "%": 30}
        self.patterns: Dict[str, int] = dict([(str(x), x) for x in range(1, 10)])
        self.colliders: List = []
        self.score: int = 0

    def _new_collider(self, max_y: int, max_x: int) -> List:
        obj = [
            random.randint(2, max_y - 3),
            random.randint(2, max_x - 2),
            random.choice(list(self.patterns.keys())),
        ]
        return obj

    def new_collider(self, max_y: int, max_x: int) -> List:
        self.colliders = []
        self.colliders.append(self._new_collider(max_y, max_x))


class BoardScene(Scene):
    def __init__(self, sh: SnakeHandler):
        super(BoardScene, self).__init__("Board Scene")
        self.border = False
        self.max_y: int = 0
        self.max_x: int = 0
        self.sh: SnakeHandler = sh

    def setup(self, screen: Any):
        def draw_snake():
            result: List = []
            for link in self.sh.snake.chain:
                result.append([link.y, link.x, link.sprite])
            return result

        def draw_collider():
            result: List = []
            for obj in self.sh.colliders:
                result.append([obj[0], obj[1], obj[2]])
            return result

        def draw_score():
            return [[0, 3, " [ Score: {} ] ".format(self.sh.score)]]

        def move_snake(move_to):
            def _move_snake():
                self.sh.snake.move_to(move_to)
                return []

            return _move_snake

        # self.max_x, self.max_y = screen.getmaxyx()
        self.max_y, self.max_x = curses.LINES - 1, curses.COLS - 1
        self.add_object(Box(0, 0, self.max_y - 1, self.max_x))
        self.add_object(Caller(-1, -1, draw_score))
        self.add_object(Caller(-1, -1, draw_snake))
        self.sh.new_collider(self.max_y, self.max_x)
        self.add_object(Caller(-1, -1, draw_collider))
        self.kh = KeyHandler({})
        self.kh.register("x", lambda: exit(0))
        self.kh.register(chr(curses.KEY_LEFT), move_snake(Move.LEFT))
        self.kh.register(chr(curses.KEY_RIGHT), move_snake(Move.RIGHT))
        self.kh.register(chr(curses.KEY_UP), move_snake(Move.UP))
        self.kh.register(chr(curses.KEY_DOWN), move_snake(Move.DOWN))

    @update_scene
    def update(self, *events: Event) -> List[Event]:
        event_to_return: List[Event] = []
        for event in events:
            if event.evt == EVT.ENG.KEY:
                event_to_return.extend(self.kh.update(event))
        self.sh.snake.tick(5)
        return event_to_return

    @render_scene
    def render(self, screen: Any) -> List[Event]:
        self.sh.snake.wall_collision(self.max_y, self.max_x)
        hit = self.sh.snake.check_collision(screen, list(self.sh.patterns.keys()))
        if hit is not None:
            self.sh.score += self.sh.patterns[hit]
            self.sh.new_collider(self.max_y, self.max_x)
        return super(BoardScene, self).render(screen)


if __name__ == "__main__":
    h = Handler()
    h.add_scene(BoardScene(SnakeHandler()))
    h.run()
