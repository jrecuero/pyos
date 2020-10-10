class Plugin:
    def __init__(self, **kwargs):
        pass

    def exception(self):
        assert False, "Not Implemented"

    def init(self):
        assert False, "Not Implemented"

    def restore_screen(self, screen):
        assert False, "Not Implemented"

    def erase(self, screen):
        assert False, "Not Implemented"

    def refresh_screen(self, screen):
        assert False, "Not Implemented"

    def doupdate(self):
        assert False, "Not Implemented"

    def wait(self, tick_time):
        assert False, "Not Implemented"

    def nodelay(self, screen, flag):
        assert False, "Not Implemented"

    def border(self, screen, *args):
        assert False, "Not Implemented"

    def colors(self, color_pairs):
        assert False, "Not Implemented"

    def get_ch(self, screen) -> int:
        assert False, "Not Implemented"

    def cursor(self, flag):
        assert False, "Not Implemented"

    def key(self, k: str):
        assert False, "Not Implemented"

    def default_fmt(self):
        assert False, "Not Implemented"

    def fmt(self, f: str):
        assert False, "Not Implemented"

    def draw_sprite(self, screen, sprite, y, x, dy, dx, fmt=None):
        assert False, "Not Implemented"

    def draw_rectangle(self, screen, y: int, x: int, dy: int, dx: int, fmt=None):
        assert False, "Not Implemented"
