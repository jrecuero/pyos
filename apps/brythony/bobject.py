from collision import CollisionBox
from point import Point

STEP = 20


class BryObject:
    def __init__(self, x, y, dx, dy, **kwargs):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.floor = False

    def get_collision_box(self):
        collision_box = CollisionBox()
        return collision_box

    def update(self, ctx, events, **kwargs):
        pass

    def render(self, ctx, events, **kwargs):
        pass


class TextBO(BryObject):
    def __init__(self, x, y, texto, **kwargs):
        super(TextBO, self).__init__(x, y, None, None, **kwargs)
        self.texto = texto
        self.font = kwargs.get("font", "12px Arial")
        self.style = kwargs.get("style", "black")

    def render(self, ctx, events, **kwargs):
        ctx.font = self.font
        ctx.fillStyle = self.style
        ctx.fillText(self.texto, self.x, self.y)


class RectBO(BryObject):
    def __init__(self, x, y, dx, dy, **kwargs):
        super(RectBO, self).__init__(x, y, dx, dy, **kwargs)
        self.lwidth = kwargs.get("lwidth", 5)
        self.style = kwargs.get("style", "black")

    def render(self, ctx, events, **kwargs):
        ctx.beginPath()
        ctx.lineWidth = self.lwidth
        ctx.strokeStyle = self.style
        ctx.fillStyle = self.style
        ctx.rect(self.x, self.y, self.dx, self.dy)
        ctx.closePath()
        # ctx.stroke()
        ctx.fill()


class PieceBO(BryObject):
    def __init__(self, x, y, dx, dy, matrix, **kwargs):
        super(PieceBO, self).__init__(x, y, dx, dy, **kwargs)
        self.matrix = matrix
        self.lwidth = kwargs.get("lwidth", 1)
        self.style = kwargs.get("style", "black")

    def get_collision_box(self):
        return self.matrix.get_collision_box()

    def render(self, ctx, events, **kwargs):
        self.matrix.render(ctx, **kwargs)


class SpriteBO(BryObject):
    def __init__(self, x, y, dx, dy, sprite, **kwargs):
        super(SpriteBO, self).__init__(x, y, dx, dy)
        self.sprite = sprite


class BoardBO(BryObject):
    def __init__(self, xsize, ysize):
        super(BoardBO, self).__init__(0, 0, STEP * xsize, STEP * ysize)
        self.xsize = xsize
        self.ysize = ysize

    def get_collision_box(self):
        collision_box = CollisionBox()
        for y in range(self.ysize):
            collision_box.add(Point(0, y * STEP))
            collision_box.add(Point(STEP * (self.xsize - 1), y * STEP))
        # for x in range(self.xsize):
        #     collision_box.add(Point(x * STEP, STEP * (self.ysize - 1)))
        return collision_box

    def render(self, ctx, events, **kwargs):
        ctx.beginPath()
        ctx.fillStyle = "red"
        for y in range(self.ysize):
            ctx.rect(0, y * STEP, STEP, STEP)
            ctx.rect(STEP * (self.xsize - 1), y * STEP, STEP, STEP)
        # for x in range(self.xsize):
        #     ctx.rect(x * STEP, STEP * (self.ysize - 1), STEP, STEP)
        ctx.closePath()
        ctx.fill()


class FloorBO(BryObject):
    def __init__(self, xsize, ysize):
        super(BoardBO, self).__init__(0, 0, STEP * xsize, STEP * ysize)
        self.xsize = xsize
        self.ysize = ysize
        self.floor = True

    def get_collision_box(self):
        collision_box = CollisionBox()
        for x in range(self.xsize):
            collision_box.add(Point(x * STEP, STEP * (self.ysize - 1)))
        return collision_box

    def render(self, ctx, events, **kwargs):
        ctx.beginPath()
        ctx.fillStyle = "red"
        for x in range(self.xsize):
            ctx.rect(x * STEP, STEP * (self.ysize - 1), STEP, STEP)
        ctx.closePath()
        ctx.fill()
