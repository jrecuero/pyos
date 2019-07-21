from ._plugin import Plugin
import time


class BrythonPlugin(Plugin):
    def __init__(self, kwargs):
        self.canvas = kwargs.get("canvas", None)
        assert self.canvas, f"Invalid canvas {self.canvas}"

    def exception(self):
        return Exception

    def init(self):
        self.ctx = self.canvas.getContext("2d")
        self.x, self.y = 0, 0
        self.dx, self.dy = self.canvas.width, self.canvas.height
        return self.canvas

    def restore_screen(self, canvas):
        pass

    def erase(self, canvas):
        canvas.clearRect(self.x, self.y, self.width, self.height)

    def refresh_screen(self, canvas):
        pass

    def doupdate(self):
        pass

    def wait(self, tick_time):
        time.sleep(float(tick_time / 1000))

    def nodelay(self, canvas, flag):
        pass

    def border(self, canvas, *args):
        self.ctx.beginPath()
        self.ctx.rect(self.x, self.y, self.width, self.height)
        self.ctx.stroke()

    def colors(self, color_pairs):
        pass

    def get_ch(self, canvas) -> int:
        pass

    def cursor(self, flag):
        pass

    def key(self, k: str):
        pass

    def default_fmt(self):
        pass

    def fmt(self, f: str):
        pass

    def draw_sprite(self, canvas, sprite, y, x, dy, dx, fmt=None):
        self.ctx.font = "20px Arial"
        self.fillText(sprite, x, y)

    def draw_rectangle(self, canvas, y: int, x: int, dy: int, dx: int, fmt=None):
        self.ctx.beginPath()
        self.ctx.rect(x, y, dx, dy)
        self.ctx.stroke()
