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
from engine.physic import ShooterShape, BulletShape


class GameHandler(Arena):
    def __init__(self, y: int, x: int, max_y: int, max_x: int, **kwargs):
        super(GameHandler, self).__init__(x, y, max_y, max_x)

    def eventor(self, event, **kwargs):
        if event == "shoot":
            actor = kwargs.get("actor", None)
            self.add_shape(BulletShape(parent=actor), relative=False)
            pass
        elif event == "delete":
            actor = kwargs.get("actor", None)
            self.shapes.remove(actor)
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
        actor = ShooterShape(timeout=1)
        phead = Point(1, 5)
        # actor.append(BB("#", pos=phead, move=Move.RIGHT, fmt=curses.color_pair(1)))
        actor.append(
            BB(chr(9819), pos=phead, move=Move.RIGHT, fmt=curses.color_pair(1))
        )
        self.ghandler.add_shape(actor)
        self.add_object(self.ghandler)

        self.kh = ArrowKeyHandler(
            left=actor.move(Move.LEFT),
            right=actor.move(Move.RIGHT),
            up=actor.move(Move.UP),
            down=actor.move(Move.DOWN),
            space=actor.shoot(),
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
