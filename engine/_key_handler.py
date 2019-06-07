import curses
from ._event import KeyHandler


KEY_SPACE = " "
KEY_EXIT = "x"


class ArrowKeyHandler(KeyHandler):
    def __init__(self, **kwargs):
        super(ArrowKeyHandler, self).__init__()
        self.register(KEY_EXIT, lambda: exit(0))
        self.register(chr(curses.KEY_LEFT), kwargs.get("left", None))
        self.register(chr(curses.KEY_RIGHT), kwargs.get("right", None))
        self.register(chr(curses.KEY_UP), kwargs.get("up", None))
        self.register(chr(curses.KEY_DOWN), kwargs.get("down", None))
        self.register(KEY_SPACE, kwargs.get("space", None))
