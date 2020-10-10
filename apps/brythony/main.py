from browser import document, timer
from bevent import move_bevent, rotate_bevent
from point import Point
from cell import Cell
from content import Content
from matrix import Matrix
from bobject import PieceBO, BoardBO, FloorBO
from collision import CollisionBox

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

    def get_collision_box(self):
        return self.bobject.get_collision_box()


class Player(Actor):
    def __init__(self, name, bobject, **kwargs):
        super(Player, self).__init__(name, bobject, **kwargs)
        self.playable = True
        self.gravity = 10
        self.gindex = 0
        self.last_event = None

    def back(self, gravity=False):
        evt = self.last_event
        if evt.system == "update" and evt.dest == "playable":
            if evt.event == "move" and (gravity or evt.source != "gravity"):
                self.bobject.matrix.move(-1 * evt.evargs["x"], -1 * evt.evargs["y"])
            elif evt.event == "rotate" and evt.evargs["rotation"] == "right":
                self.bobject.matrix = self.bobject.matrix.rotate_anticlockwise()
            elif evt.event == "rotate" and evt.evargs["rotation"] == "left":
                self.bobject.matrix = self.bobject.matrix.rotate_clockwise()

    def update(self, ctx, events, **kwargs):
        self.gindex += 1
        if self.gindex == self.gravity:
            self.gindex = 0
            events.append(move_bevent("gravity", "playable", 0, 1))

        for evt in events:
            if evt.system == "update" and evt.dest == "playable":
                self.last_event = evt
                if evt.event == "move":
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
        self.board = None
        self.floor = None
        self.player = None

    def clear(self, ctx):
        ctx.clearRect(self.x, self.y, self.dx, self.dy)

    def add_bobject(self, bobject):
        self.bobjects.append(bobject)

    def add_actor(self, actor):
        self.actors.append(actor)

    def set_player(self, actor):
        if self.player and actor.playable:
            raise Exception("Scene already has playable actor")
        self.player = actor
        self.add_actor(actor)

    def set_board(self, bobject):
        if self.board:
            raise Exception("Scene already has board")
        self.board = bobject
        self.add_bobject(bobject)

    def set_floor(self, bobject):
        if self.floor:
            raise Exception("Scene already has floor")
        self.floor = bobject
        self.add_bobject(bobject)

    def check_collision(self):
        for actor in self.actors:
            actor_box = actor.get_collision_box()
            for bobj in self.bobjects:
                bobj_box = bobj.get_collision_box()
                collision = actor_box.collision_with(bobj_box)
                if collision:
                    if bobj.floor:
                        actor.back(gravity=True)
                        actor_box = actor.get_collision_box()
                        upper_box = CollisionBox()
                        for p_c in collision:
                            upper_box.add(Point(p_c.x, p_c.y - 1))
                        if actor_box.collision_with(upper_box):
                            self.player = None
                            self.actors.remove(actor)
                            pos_to_add = actor.bobject.matrix.get_pos()
                            self.board.add_pos(pos_to_add)
                            self.floor.add_pos(pos_to_add)
                            self.set_player(create_player())
                        return
                    else:
                        actor.back()
                        return

    def update(self, ctx, events, **kwargs):
        for bobj in self.bobjects:
            bobj.update(ctx, self.update_events, **kwargs)
        for actor in self.actors:
            actor.update(ctx, self.update_events, **kwargs)
        self.check_collision()
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


def create_player():
    _mat = [[1, 0, 0], [1, 1, 0], [1, 0, 0]]
    mat = build_matrix_from_mat_at(2, 2, STEP, STEP, _mat)
    piece = PieceBO(
        2, 2, STEP, STEP, Matrix(mat, Point(2, 2), STEP, STEP), style="blue"
    )
    player = Player("me", piece)
    return player


canvas = document["the_canvas"]
scene = BryScene(0, 0, canvas.width, canvas.height)
scene.set_floor(FloorBO(20, 20, STEP))
scene.set_board(BoardBO(20, 20, STEP))
scene.set_player(create_player())
handler = BryHandler(canvas)
handler.add_scene(scene)
handler.active_scene = scene
document.bind("keydown", scene.controller)
timer.set_interval(handler.run, 30)
