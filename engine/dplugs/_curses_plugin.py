import curses


class CursesPlugin:
    def __init__(self):
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

    def nodelay(self, screen, flag):
        screen.nodelay(flag)

    def border(self, screen, *args):
        screen.border(*args)

    def erase(self, screen):
        screen.erase()

    def colors(self, color_pairs):
        for index, (fg, bg) in enumerate(color_pairs):
            curses.init_pair(index + 1, fg, bg)

    def get_ch(self, screen) -> int:
        key: int = screen.getch()
        curses.flushinp()
        return key

    def restore_screen(self, screen):
        curses.nocbreak()
        screen.keypad(False)
        curses.echo()
        curses.curs_set(1)
        curses.endwin()

    def wait(self, tick_time):
        curses.napms(tick_time)

    def cursor(self, flag):
        curses.curs_set(flag)

    def doupdate(self):
        curses.doupdate()

    def refresh_screen(self, screen):
        screen.noutrefresh()

    def key(self, k: str):
        return getattr(curses, k)

    def key_left(self):
        return curses.KEY_LEFT

    def key_right(self):
        return curses.KEY_RIGHT

    def key_up(self):
        return curses.KEY_UP

    def key_down(self):
        return curses.KEY_DOWN

    def default_fmt(self):
        return curses.A_NORMAL

    def fmt(self, f: str):
        return getattr(curses, f)

    def fmt_bold(self):
        return curses.A_BOLD

    def fmt_underline(self):
        return curses.A_UNDERLINE

    def fmt_reverse(self):
        return curses.A_REVERSE

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
