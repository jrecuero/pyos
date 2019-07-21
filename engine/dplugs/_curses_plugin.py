import curses
from ._plugin import Plugin


class CursesPlugin(Plugin):
    def __init__(self, **kwargs):
        pass

    def exception(self):
        return curses.error

    def init(self):
        screen = curses.initscr()
        curses.cbreak()
        curses.start_color()
        curses.noecho()
        screen.keypad(True)
        return screen

    def restore_screen(self, screen):
        curses.nocbreak()
        screen.keypad(False)
        curses.echo()
        curses.curs_set(1)
        curses.endwin()

    def erase(self, screen):
        screen.erase()

    def refresh_screen(self, screen):
        screen.noutrefresh()

    def doupdate(self):
        curses.doupdate()

    def wait(self, tick_time):
        curses.napms(tick_time)

    def nodelay(self, screen, flag):
        screen.nodelay(flag)

    def border(self, screen, *args):
        screen.border(*args)

    def colors(self, color_pairs):
        for index, (fg, bg) in enumerate(color_pairs):
            curses.init_pair(index + 1, fg, bg)

    def get_ch(self, screen) -> int:
        key: int = screen.getch()
        curses.flushinp()
        return key

    def cursor(self, flag):
        curses.curs_set(flag)

    def key(self, k: str):
        return getattr(curses, k)

    def default_fmt(self):
        return curses.A_NORMAL

    def fmt(self, f: str):
        return getattr(curses, f)

    def draw_sprite(self, screen, sprite, y, x, dy, dx, fmt=curses.A_NORMAL):
        screen.addnstr(y, x, sprite, dx, fmt)

    def draw_rectangle(
        self, screen, y: int, x: int, dy: int, dx: int, fmt=curses.A_NORMAL
    ):
        for _x in range(1, dx):
            screen.addnstr(y, x + _x, chr(9473), 1, fmt)
        for _x in range(1, dx):
            screen.addnstr(y + dy, x + _x, chr(9473), 1, fmt)
        for _y in range(1, dy):
            screen.addnstr(y + _y, x, chr(9475), 1, fmt)
        for _y in range(1, dy):
            screen.addnstr(y + _y, x + dx, chr(9475), 1, fmt)
        screen.addnstr(y, x, chr(9487), 1, fmt)
        screen.addnstr(y + dy, x, chr(9495), 1, fmt)
        screen.addnstr(y, x + dx, chr(9491), 1, fmt)
        screen.addnstr(y + dy, x + dx, chr(9499), 1, fmt)
