from typing import List
import curses
import time


class Move(object):

    NONE: int = 0
    UP: int = 1
    DOWN: int = 2
    RIGHT: int = 3
    LEFT: int = 4


class Link(object):
    def __init__(self, sprite: str, move: int = Move.NONE, pushed: bool = False):
        self.sprite: str = sprite
        self.move: int = move
        self.pushed: bool = pushed
        self.pos: List = [0, 0]


class Chain(object):
    def __init__(self, length: int, sprite: str):
        self.chain: List[Link] = []
        for _ in range(length):
            self.chain.append(Link(sprite))

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
            new_link.pos = [last_link.pos[0] + 1, last_link.pos[1]]
        elif new_link.move == Move.DOWN:
            new_link.pos = [last_link.pos[0] - 1, last_link.pos[1]]
        elif new_link.move == Move.RIGHT:
            new_link.pos = [last_link.pos[0], last_link.pos[1] - 1]
        elif new_link.move == Move.LEFT:
            new_link.pos = [last_link.pos[0], last_link.pos[1] + 1]
        self.chain.append(new_link)

    def tick(self):
        pushed: bool = False
        pushed_move: int = Move.NONE
        next_pushed: bool = False
        next_pushed_move: int = Move.NONE
        for index, link in enumerate(self.chain):
            if link.move == Move.UP:
                link.pos[0] -= 1
            elif link.move == Move.DOWN:
                link.pos[0] += 1
            elif link.move == Move.RIGHT:
                link.pos[1] += 1
            elif link.move == Move.LEFT:
                link.pos[1] -= 1
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
        head = self.chain[0]
        if head.move != move:
            head.pushed = True
            head.move = move

    def check_collision(self, screen) -> bool:
        if chr(screen.inch(self.chain[0].pos[0], self.chain[0].pos[1]) & 255) == "*":
            self.add_link("#")
            return True
        return False

    def draw(self, screen):
        for link in self.chain:
            screen.addstr(link.pos[0], link.pos[1], link.sprite)


if __name__ == "__main__":
    screen = curses.initscr()
    curses.cbreak()
    curses.noecho()
    curses.curs_set(0)
    screen.keypad(True)
    screen.nodelay(True)
    try:
        tick_time = 0.5
        snake = Chain(1, "#")
        snake.start_at(Move.RIGHT, [5, 15])
        while True:
            screen.clear()
            screen.border(0)
            screen.addstr(10, 10, "*", curses.A_BOLD)
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
            snake.draw(screen)
            screen.refresh()
            snake.tick()
            if snake.check_collision(screen):
                tick_time -= 0.05 if tick_time > 0.2 else 0
            time.sleep(tick_time)
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
