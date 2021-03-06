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
    Point,
    BB,
    Move,
    Arena,
)
from engine.nobject import String
from engine.physic import StaticShape, ShooterShape, BulletShape, BreakableShape


class GameHandler(Arena):
    def __init__(self, y: int, x: int, max_y: int, max_x: int, **kwargs):
        super(GameHandler, self).__init__(x, y, max_y, max_x)

    def eventor(self, event, **kwargs):
        if event == "shoot":
            actor = kwargs.get("actor", None)
            self.add_shape(BulletShape(parent=actor), relative=False)
        elif event == "delete":
            actor = kwargs.get("actor", None)
            self.shapes.remove(actor)


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
        self.actor = ShooterShape(timeout=1)
        phead = Point(1, 5)
        # self.actor.append(BB("#", pos=phead, move=Move.RIGHT, fmt=curses.color_pair(1)))
        self.actor.append(
            # BB(chr(9819), pos=phead, move=Move.RIGHT, fmt=curses.color_pair(1))
            BB("x", pos=phead, move=Move.RIGHT, fmt=curses.color_pair(1))
        )
        trees: List[StaticShape] = []
        mounts: List[StaticShape] = []
        dummies: List[StaticShape] = []
        targets: List[BreakableShape] = []
        for y, x in [(_y, _x) for _y in range(3) for _x in range(6)]:
            trees.append(StaticShape().append(BB("Y", pos=Point(5 + y, 25 + y + x))))
        for y, x in [(_y, _x) for _y in range(5) for _x in range(5)]:
            mounts.append(StaticShape().append(BB("A", pos=Point(10 + y, 10 + y + x))))
        for y, x in [(_y, _x) for _y in range(2) for _x in range(2)]:
            targets.append(BreakableShape().append(BB("T", pos=Point(15 + y, 75 + x))))
        dummies.append(
            StaticShape().append(BB("D", pos=Point(15, 50), fmt=curses.color_pair(2)))
        )
        dummies.append(
            StaticShape().append(BB("D", pos=Point(10, 100), fmt=curses.color_pair(2)))
        )
        self.ghandler.add_shape(self.actor)
        self.ghandler.add_shapes(trees)
        self.ghandler.add_shapes(mounts)
        self.ghandler.add_shapes(targets)
        self.ghandler.add_shapes(dummies)
        self.add_object(self.ghandler)
        self.actor_pos = String(
            self.max_y + 1, self.max_x - 15, "[ {} ]".format(self.actor.head.pos)
        )
        self.add_object(self.actor_pos)

        self.kh = ArrowKeyHandler(
            left=self.actor.move(Move.LEFT),
            right=self.actor.move(Move.RIGHT),
            up=self.actor.move(Move.UP),
            down=self.actor.move(Move.DOWN),
            space=self.actor.shoot(),
        )

    @update_scene
    def update(self, screen: Any, *events: Event) -> List[Event]:
        self.actor_pos.set_text("[ {} ]".format(self.actor.head.pos))
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
