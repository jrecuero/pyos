from browser import document, timer
from bevent import move_bevent
from cell import Cell

KEY_LEFT = 37
KEY_UP = 38
KEY_RIGHT = 39
KEY_DOWN = 40
KEY_SPACE = 32


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
        for i, fill in enumerate(self.matrix):
            if fill:
                ctx.rect(x, y, self.dx, self.dy)
            if i % 3 == 2:
                y += self.dy
                x = self.x
            else:
                x += self.dx
        # ctx.endPath()
        # ctx.stroke()
        ctx.fill()


class SpriteBO(BryObject):
    def __init__(self, x, y, dx, dy, sprite, **kwargs):
        super(SpriteBO, self).__init__(x, y, dx, dy)
        self.sprite = sprite


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
        # self.gindex += 1
        # if self.gindex == self.gravity:
        #     self.gindex = 0
        #     self.bobject.y += 10

        for evt in events:
            if evt.system == "update" and evt.dest == "playable":
                if evt.event == "move":
                    self.bobject.x += evt.evargs["x"]
                    self.bobject.y += evt.evargs["y"]
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

    def controller(self, evt):
        move = 10
        if evt.keyCode == KEY_LEFT:
            self.move(-1 * move, 0)
        elif evt.keyCode == KEY_UP:
            self.move(0, -1 * move)
        elif evt.keyCode == KEY_RIGHT:
            self.move(move, 0)
        elif evt.keyCode == KEY_DOWN:
            self.move(0, move)
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


class BrythonCanvas:
    def __init__(self, canvas):
        self.canvas = canvas
        self.ctx = self.canvas.getContext("2d")
        self.x, self.y = 10, 10
        self.dx, self.dy = 0, 0
        self.bobjects = []
        self.movil = None

    def clear(self):
        self.ctx.clearRect(0, 0, self.canvas.width, self.canvas.height)

    def string(self, message, x, y, font="12px Arial", style="black"):
        self.ctx.font = font
        self.ctx.fillStyle = style
        self.ctx.fillText(message, x, y)

    def box(self, x, y, dx, dy, width="1", style="black"):
        self.ctx.beginPath()
        self.ctx.lineWidth = width
        self.ctx.strokeStyle = style
        self.ctx.rect(x, y, dx, dy)
        self.ctx.stroke()

    def key_press(self, evt):
        self.clear()
        self.string(chr(evt.charCode), 10, 40)

    def render(self):
        # self.x += self.dx
        # self.y += self.dy
        # self.clear()
        # self.ctx.beginPath()
        # self.ctx.lineWidth = "10"
        # self.ctx.strokeStyle = "red"
        # self.ctx.rect(self.x, self.y, 10, 10)
        # self.ctx.stroke()
        self.clear()
        for bobj in self.bobjects:
            bobj.render(self.ctx),

    def move(self, x, y):
        # self.x += x
        # self.y += y
        self.dx = x
        self.dy = y
        self.movil.x += x
        self.movil.y += y

    def key_down(self, evt):
        move = 5
        if evt.keyCode == 37:
            self.move(-1 * move, 0)
        elif evt.keyCode == 38:
            self.move(0, -1 * move)
        elif evt.keyCode == 39:
            self.move(move, 0)
        elif evt.keyCode == 40:
            self.move(0, move)
        elif evt.keyCode == 32:
            self.move(0, 0)


# canvas = BrythonCanvas(document["the_canvas"])
# canvas.movil = RectBO(20, 20, 10, 10, style="blue")
# canvas.bobjects.append(TextBO("Jose Carlos", 10, 10))
# canvas.bobjects.append(canvas.movil)
# canvas.clear()
# canvas.render()
# timer.set_interval(canvas.render, 60)
# # canvas.box(0, 0, 200, 100)
# # canvas.string("Hello World", 10, 20, font="14px Times New Roman")
# # canvas.string("This is a python canvas", 10, 40, style="red")
# # document.bind("keypress", canvas.key_press)
# document.bind("keydown", canvas.key_down)
canvas = document["the_canvas"]
scene = BryScene(0, 0, canvas.width, canvas.height)
# actor = Player("me", RectBO(20, 20, 20, 20, style="red"))
# actor = Player("me", PieceBO(20, 20, 20, 20, [1, 0, 1, 0, 1, 0, 1, 0, 1], style="blue"))
actor = Player("me", PieceBO(20, 20, 20, 20, [1, 0, 0, 1, 0, 0, 1, 1, 1], style="blue"))
scene.add_actor(actor)
handler = BryHandler(canvas)
handler.add_scene(scene)
handler.active_scene = scene
document.bind("keydown", scene.controller)
timer.set_interval(handler.run, 60)
