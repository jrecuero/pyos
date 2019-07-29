from browser import document, timer
from bevent import move_bevent, rotate_bevent
from point import Point
from cell import Cell
from content import Content
from matrix import Matrix
from bobject import PieceBO, BoardBO

KEY_LEFT = 37
KEY_UP = 38
KEY_RIGHT = 39
KEY_DOWN = 40
KEY_SPACE = 32

STEP = 20


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
                    # self.bobject.x += evt.evargs["x"]
                    # self.bobject.y += evt.evargs["y"]
                    self.bobject.matrix.move(evt.evargs["x"], evt.evargs["y"])
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
        # move = STEP
        if evt.keyCode == KEY_LEFT:
            # self.move(-1 * move, 0)
            self.move(-1, 0)
        elif evt.keyCode == KEY_UP:
            # self.move(0, -1 * move)
            self.rotate_right()
        elif evt.keyCode == KEY_RIGHT:
            # self.move(move, 0)
            self.move(1, 0)
        elif evt.keyCode == KEY_DOWN:
            # self.move(0, move)
            self.rotate_left()
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


def build_matrix_from_mat_at(x, y, dx, dy, mat):
    matrix = []
    xpos, ypos = x, y
    for row in mat:
        rows = []
        for col in row:
            content = Content(dx, dy, "blue")
            if not col:
                content.disable()
            cell = Cell(content)
            xpos += dx
            rows.append(cell)
        ypos += dy
        xpos = x
        matrix.append(rows)
    return matrix


canvas = document["the_canvas"]
scene = BryScene(0, 0, canvas.width, canvas.height)
# actor = Player("me", RectBO(20, 20, 20, 20, style="red"))
# actor = Player("me", PieceBO(20, 20, 20, 20, [1, 0, 1, 0, 1, 0, 1, 0, 1], style="blue"))
# actor = Player("me", PieceBO(20, 20, 20, 20, [1, 0, 0, 1, 0, 0, 1, 1, 1], style="blue"))
_mat = [[1, 0, 0], [1, 1, 0], [1, 0, 0]]
mat = build_matrix_from_mat_at(STEP * 2, STEP * 2, STEP, STEP, _mat)
piece = PieceBO(
    STEP * 2,
    STEP * 2,
    STEP,
    STEP,
    Matrix(mat, Point(STEP * 2, STEP * 2), STEP, STEP),
    style="blue",
)
actor = Player("me", piece)
scene.add_bobject(BoardBO(20, 20))
scene.add_actor(actor)
handler = BryHandler(canvas)
handler.add_scene(scene)
handler.active_scene = scene
document.bind("keydown", scene.controller)
timer.set_interval(handler.run, 60)
