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
    def __init__(self, xsize, ysize, gsize):
        super(BoardBO, self).__init__(0, 0, xsize, ysize)
        self.gsize = gsize
        self.pos = []
        for y in range(self.dy):
            self.pos.append(Point(0, y))
            self.pos.append(Point(self.dx - 1, y))

    def add_pos(self, pos):
        self.pos.extend(pos)

    def get_collision_box(self):
        collision_box = CollisionBox()
        for p in self.pos:
            collision_box.add(p)
        # for y in range(self.dy):
        #     collision_box.add(Point(0, y))
        #     collision_box.add(Point(self.dx - 1, y))
        # for x in range(self.dx):
        #     collision_box.add(Point(x * self.gsize, self.gsize * (self.dy - 1)))
        return collision_box

    def render(self, ctx, events, **kwargs):
        ctx.beginPath()
        ctx.fillStyle = "red"
        for p in self.pos:
            ctx.rect(p.x * self.gsize, p.y * self.gsize, self.gsize, self.gsize)
        # for y in range(self.dy):
        #     ctx.rect(0, y * self.gsize, self.gsize, self.gsize)
        #     ctx.rect(self.gsize * (self.dx - 1), y * self.gsize, self.gsize, self.gsize)
        # for x in range(self.dx):
        #     ctx.rect(x * self.gsize, self.gsize * (self.dy - 1), self.gsize, self.gsize)
        ctx.closePath()
        ctx.fill()


class FloorBO(BryObject):
    def __init__(self, xsize, ysize, gsize):
        super(BoardBO, self).__init__(0, 0, xsize, ysize)
        self.gsize = gsize
        self.floor = True
        self.pos = []
        for x in range(self.dx):
            self.pos.append(Point(x, self.dy - 1))

    def add_pos(self, pos):
        self.pos.extend(pos)

    def get_collision_box(self):
        collision_box = CollisionBox()
        for p in self.pos:
            collision_box.add(p)
        # for x in range(self.dx):
        #     collision_box.add(Point(x, self.dy - 1))
        return collision_box

    def render(self, ctx, events, **kwargs):
        ctx.beginPath()
        ctx.fillStyle = "red"
        for p in self.pos:
            ctx.rect(
                p.x * self.gsize, self.gsize * (self.dy - 1), self.gsize, self.gsize
            )
        # for x in range(self.dx):
        #     ctx.rect(x * self.gsize, self.gsize * (self.dy - 1), self.gsize, self.gsize)
        ctx.closePath()
        ctx.fill()
