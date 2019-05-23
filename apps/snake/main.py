from typing import List, Any
import curses
import random


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

    def tick(self):
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

    def wall_collision(self, screen) -> bool:
        max_y, max_x = screen.getmaxyx()
        if (self.head.move == Move.UP) and (self.head.y == 1):
            if self.head.x == 1:
                self.move_to(Move.RIGHT)
            else:
                self.move_to(Move.LEFT)
            return True
        if (self.head.move == Move.DOWN) and (self.head.y == max_y - 3):
            if self.head.x == 1:
                self.move_to(Move.RIGHT)
            else:
                self.move_to(Move.LEFT)
            return True
        if (self.head.move == Move.LEFT) and (self.head.x == 1):
            if self.head.y == 1:
                self.move_to(Move.DOWN)
            else:
                self.move_to(Move.UP)
            return True
        if (self.head.move == Move.RIGHT) and (self.head.x == max_x - 2):
            if self.head.y == 1:
                self.move_to(Move.DOWN)
            else:
                self.move_to(Move.UP)
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


if __name__ == "__main__":
    screen = curses.initscr()
    curses.cbreak()
    curses.noecho()
    curses.curs_set(0)
    screen.keypad(True)
    screen.nodelay(True)
    max_y, max_x = screen.getmaxyx()
    patterns = {"*": 10, "$": 20, "%": 30}
    obj = [
        random.randint(2, max_y - 3),
        random.randint(2, max_x - 2),
        random.choice(list(patterns.keys())),
    ]
    try:
        score = 0
        tick_time = 50
        snake = Chain(1, "#")
        snake.start_at(Move.RIGHT, [5, 15])
        while True:
            screen.erase()
            # screen.border(0)
            draw_box(screen, 0, 0, max_y - 2, max_x)
            screen.addstr(0, 2, "[ Score: {} ]".format(score))
            screen.addstr(
                max_y - 1, max_x - 10, "{}, {}".format(max_y, max_x), curses.A_BOLD
            )
            screen.addstr(max_y - 1, 2, "{}, {}".format(snake.head.y, snake.head.x))
            screen.addstr(obj[0], obj[1], obj[2], curses.A_BOLD)
            key = screen.getch()
            if key != -1:
                if "x" == chr(key):
                    break
                elif curses.KEY_LEFT == key:
                    snake.move_to(Move.LEFT)
                elif curses.KEY_RIGHT == key:
                    snake.move_to(Move.RIGHT)
                elif curses.KEY_UP == key:
                    snake.move_to(Move.UP)
                elif curses.KEY_DOWN == key:
                    snake.move_to(Move.DOWN)
            snake.tick()
            snake.wall_collision(screen)
            hit = snake.check_collision(screen, list(patterns.keys()))
            if hit is not None:
                score += patterns[hit]
                obj = [
                    random.randint(2, max_y - 3),
                    random.randint(2, max_x - 2),
                    random.choice(list(patterns.keys())),
                ]
            snake.draw(screen)
            screen.refresh()
            curses.napms(tick_time)
    except KeyboardInterrupt:
        pass
    except curses.error as ex:
        curses.nocbreak()
        screen.keypad(False)
        curses.echo()
        curses.endwin()
        curses.curs_set(1)
        print(ex)
    finally:
        curses.nocbreak()
        screen.keypad(False)
        curses.echo()
        curses.endwin()
        curses.curs_set(1)
        # sys.exit(1)
