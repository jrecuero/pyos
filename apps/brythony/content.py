class Content:
    def __init__(self, dx, dy, style):
        self.dx = dx
        self.dy = dy
        self.style = style
        self._enable = True

    def enable(self):
        self._enable = True

    def disable(self):
        self._enable = False

    def is_enable(self):
        return self._enable

    def render_at(self, ctx, x, y, **kwargs):
        if self.is_enable():
            ctx.beginPath()
            ctx.fillStyle = self.style
            ctx.rect(x, y, self.dx, self.dy)
            ctx.closePath()
            ctx.fill()
