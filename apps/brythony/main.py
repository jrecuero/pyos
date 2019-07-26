from browser import document, timer
from bevent import move_bevent, rotate_bevent
from matrix import Matrix

KEY_LEFT = 37
KEY_UP = 38
KEY_RIGHT = 39
KEY_DOWN = 40
KEY_SPACE = 32

STEP = 20


class BryObject:
    def __init__(self, x, y, dx, dy, **kwargs):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

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

    def render(self, ctx, events, **kwargs):
        ctx.beginPath()
        ctx.lineWidth = self.lwidth
        ctx.strokeStyle = self.style
        ctx.fillStyle = self.style
        x = self.x
        y = self.y
        for row in self.matrix.get_mat():
            for col in row:
                if col:
                    ctx.rect(x, y, self.dx, self.dy)
                x += self.dx
            y += self.dy
            x = self.x

        ctx.closePath()
        # ctx.stroke()
        ctx.fill()


class SpriteBO(BryObject):
    def __init__(self, x, y, dx, dy, sprite, **kwargs):
        super(SpriteBO, self).__init__(x, y, dx, dy)
        self.sprite = sprite


class BoardBO(BryObject):
    def __init__(self, xsize, ysize):
        super(BoardBO, self).__init__(0, 0, STEP * xsize, STEP * ysize)
        self.xsize = xsize
        self.ysize = ysize

    def render(self, ctx, events, **kwargs):
        ctx.beginPath()
        ctx.fillStyle = "red"
        for y in range(self.ysize):
            ctx.rect(0, y * STEP, STEP, STEP)
            ctx.rect(STEP * (self.xsize - 1), y * STEP, STEP, STEP)
        for x in range(self.xsize):
            ctx.rect(x * STEP, STEP * (self.ysize - 1), STEP, STEP)
        ctx.closePath()
        ctx.fill()


class Actor:
    def __init__(self, name, bobject, **kwargs):
        self.name = name
        self.bobject = bobject
        self.playable = kwargs.get("playable", False)

    def update(self, ctx, events, **kwargs):
        return self.bobject.update(ctx, events, **kwargs)

    def render(self, ctx, events, **kwargs):
        return self.bobject.render(ctx, events, **kwargs)


class Player(Actor):
    def __init__(self, name, bobject, **kwargs):
        super(Player, self).__init__(name, bobject, **kwargs)
        self.playable = True
        self.gravity = 10
        self.gindex = 0

    def update(self, ctx, events, **kwargs):
        self.gindex += 1
        if self.gindex == self.gravity:
            self.gindex = 0
            self.bobject.y += STEP

        for evt in events:
            if evt.system == "update" and evt.dest == "playable":
                if evt.event == "move":
                    self.bobject.x += evt.evargs["x"]
                    self.bobject.y += evt.evargs["y"]
                elif evt.event == "rotate" and evt.evargs["rotation"] == "right":
                    self.bobject.matrix = self.bobject.matrix.rotate_clockwise()
                elif evt.event == "rotate" and evt.evargs["rotation"] == "left":
                    self.bobject.matrix = self.bobject.matrix.rotate_anticlockwise()
        return self.bobject.update(ctx, events, **kwargs)


class BryScene:
    def __init__(self, x, y, dx, dy, **kwargs):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.bobjects = []
        self.actors = []
        self.update_events = []

    @property
    def player(self):
        for actor in self.actors:
            if actor.playable:
                return actor
        return None

    def clear(self, ctx):
        ctx.clearRect(self.x, self.y, self.dx, self.dy)

    def add_bobject(self, bobject):
        self.bobjects.append(bobject)

    def add_actor(self, actor):
        if self.player and actor.playable:
            raise Exception("Scene already has playable actor")
        self.actors.append(actor)

    def update(self, ctx, events, **kwargs):
        for bobj in self.bobjects:
            bobj.update(ctx, self.update_events, **kwargs)
        for actor in self.actors:
            actor.update(ctx, self.update_events, **kwargs)
        self.update_events = []

    def render(self, ctx, events, **kwargs):
        self.clear(ctx)
        for bobj in self.bobjects:
            bobj.render(ctx, events, **kwargs)
        for actor in self.actors:
            actor.render(ctx, events, **kwargs)

    def move(self, x, y):
        self.update_events.append(move_bevent(None, "playable", x, y))

    def rotate_left(self):
        self.update_events.append(rotate_bevent(None, "playable", "left"))

    def rotate_right(self):
        self.update_events.append(rotate_bevent(None, "playable", "right"))

    def controller(self, evt):
        move = STEP
        if evt.keyCode == KEY_LEFT:
            self.move(-1 * move, 0)
        elif evt.keyCode == KEY_UP:
            # self.move(0, -1 * move)
            self.rotate_left()
        elif evt.keyCode == KEY_RIGHT:
            self.move(move, 0)
        elif evt.keyCode == KEY_DOWN:
            # self.move(0, move)
            self.rotate_right()
        elif evt.keyCode == KEY_SPACE:
            self.move(0, 0)


class BryHandler:
    def __init__(self, canvas, **kwargs):
        self.canvas = canvas
        self.ctx = self.canvas.getContext("2d")
        self.scenes = []
        self.active_scene = None

    def add_scene(self, scene):
        self.scenes.append(scene)

    def update(self, events):
        if self.active_scene:
            self.active_scene.update(self.ctx, events)

    def render(self, events):
        if self.active_scene:
            self.active_scene.render(self.ctx, events)

    def run(self):
        self.update(None)
        self.render(None)


canvas = document["the_canvas"]
scene = BryScene(0, 0, canvas.width, canvas.height)
# actor = Player("me", RectBO(20, 20, 20, 20, style="red"))
# actor = Player("me", PieceBO(20, 20, 20, 20, [1, 0, 1, 0, 1, 0, 1, 0, 1], style="blue"))
# actor = Player("me", PieceBO(20, 20, 20, 20, [1, 0, 0, 1, 0, 0, 1, 1, 1], style="blue"))
actor = Player(
    "me",
    PieceBO(
        STEP * 2,
        STEP * 2,
        STEP,
        STEP,
        Matrix([[1, 0, 0], [1, 1, 0], [1, 0, 0]]),
        style="blue",
    ),
)
scene.add_bobject(BoardBO(20, 20))
scene.add_actor(actor)
handler = BryHandler(canvas)
handler.add_scene(scene)
handler.active_scene = scene
document.bind("keydown", scene.controller)
timer.set_interval(handler.run, 60)
