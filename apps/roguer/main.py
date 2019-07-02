from typing import Any, List
import curses
from engine import (
    Handler,
    Scene,
    ArrowKeyHandler,
    update_scene,
    render_scene,
    Event,
    EVT,
    Shape,
    Point,
    BB,
    Move,
    Arena,
)


class MoveShape(Shape):
    def __init__(self, **kwargs):
        super(MoveShape, self).__init__(**kwargs)

    def next_position(self, bb: BB):
        new_pos: Point = Point(bb.y, bb.x)
        if bb.move == Move.UP:
            new_pos.y = bb.y - 1
        elif bb.move == Move.DOWN:
            new_pos.y = bb.y + 1
        elif bb.move == Move.RIGHT:
            new_pos.x = bb.x + 1
        elif bb.move == Move.LEFT:
            new_pos.x = bb.x - 1
        else:
            pass
        return new_pos


class ActorShape(MoveShape):
    def __init__(self, **kwargs):
        super(ActorShape, self).__init__(**kwargs)
        self.name = "Actor"
        self.moved: bool = False

    def append(self, bb):
        if len(self):
            last_bb = self[-1]
            bb.move = last_bb.move
        return super(ActorShape, self).append(bb)

    def update(self, screen: Any) -> List[Event]:
        result: List[Event] = []
        if self.movable and self.moved and self._update():
            for bb in self.shape:
                bb.next(self.next_position(bb))
            self.moved = False
        return result

    def move(self, move_to: int):
        def _move():
            self.head.pushed = True
            self.head.move = move_to
            self.moved = True
            return []

        return _move

    def shoot(self):
        def _shoot():
            self.eventor("shoot", actor=self)
            return []

        return _shoot

    def out_of_bounds(self, y: int, x: int, max_y: int, max_x: int) -> bool:
        super(ActorShape, self).out_of_bounds(y, x, max_y, max_x)


class GameHandler(Arena):
    def __init__(self, y: int, x: int, max_y: int, max_x: int, **kwargs):
        super(GameHandler, self).__init__(x, y, max_y, max_x)

    def eventor(self, event, **kwargs):
        if event == "shoot":
            # actor = kwargs.get("actor", None)
            # self.add_shape(BulletShape(parent=actor), relative=False)
            pass
        elif event == "delete":
            # actor = kwargs.get("actor", None)
            # self.shapes.remove(actor)
            pass


class RupperScene(Scene):
    def __init__(self):
        super(RupperScene, self).__init__("Rupper Scene")
        # self.border = False
        self.max_y: int = curses.LINES - 2
        self.max_x: int = curses.COLS - 1

    def setup(self, screen: Any):
        self.ghandler = GameHandler(2, 2, self.max_y - 4, self.max_x - 4)
        # self.board_panel = Panel(1, 10, 10, 80)
        # self.add_object(self.board_panel)
        actor = ActorShape(timeout=1)
        phead = Point(1, 5)
        actor.append(BB("#", pos=phead, move=Move.RIGHT, fmt=curses.color_pair(1)))
        self.ghandler.add_shape(actor)
        self.add_object(self.ghandler)

        self.kh = ArrowKeyHandler(
            left=actor.move(Move.LEFT),
            right=actor.move(Move.RIGHT),
            up=actor.move(Move.UP),
            down=actor.move(Move.DOWN),
            # space=shape.shoot(),
        )

    @update_scene
    def update(self, screen: Any, *events: Event) -> List[Event]:
        event_to_return: List[Event] = []
        for event in events:
            if event.evt == EVT.ENG.KEY:
                event_to_return.extend(self.kh.update(event))
        return event_to_return

    @render_scene
    def render(self, screen: Any) -> List[Event]:
        return super(RupperScene, self).render(screen)


if __name__ == "__main__":
    h = Handler()
    rupper_scene = RupperScene()
    rupper_scene.colors(
        [
            (curses.COLOR_RED, curses.COLOR_BLACK),
            (curses.COLOR_YELLOW, curses.COLOR_BLACK),
            (curses.COLOR_BLACK, curses.COLOR_WHITE),
        ]
    )
    h.add_scene(rupper_scene)
    h.run()
