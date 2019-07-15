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
    Arena,
    Point,
    BB,
    Move,
)
from engine.physic import ShooterShape, BulletShape


class GameHandler(Arena):
    def __init__(self, y: int, x: int, max_y: int, max_x: int, **kwargs):
        super(GameHandler, self).__init__(x, y, max_y, max_x)

    def eventor(self, event, **kwargs):
        if event == "shoot":
            actor = kwargs.get("actor", None)
            self.add_shape(BulletShape(parent=actor, move=Move.UP), relative=False)
        elif event == "delete":
            actor = kwargs.get("actor", None)
            self.shapes.remove(actor)


class AlienScene(Scene):
    def __init__(self):
        super(AlienScene, self).__init__("Rupper Scene")
        self.max_y: int = curses.LINES - 2
        self.max_x: int = curses.COLS - 1
        if self.max_x < 100:
            raise Exception("Window Too Small X-Axis")
        if self.max_y < 20:
            raise Exception("Window Too Small Y-Axis")

    def setup(self, screen: Any):
        self.ghandler = GameHandler(2, 2, self.max_y - 4, self.max_x - 4)
        self.ship = ShooterShape(timeout=3)
        self.ship.append(
            BB(
                "A",
                pos=Point(self.ghandler.dy - 2, 5),
                move=Move.NONE,
                fmt=curses.color_pair(2),
            )
        )
        self.ghandler.add_shape(self.ship)
        self.add_object(self.ghandler)
        self.kh = ArrowKeyHandler(
            left=self.ship.move(Move.LEFT),
            right=self.ship.move(Move.RIGHT),
            space=self.ship.shoot(),
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
        return super(AlienScene, self).render(screen)


if __name__ == "__main__":
    h = Handler()
    try:
        alien_scene = AlienScene()
        alien_scene.colors(
            [
                (curses.COLOR_RED, curses.COLOR_BLACK),
                (curses.COLOR_YELLOW, curses.COLOR_BLACK),
                (curses.COLOR_BLACK, curses.COLOR_WHITE),
            ]
        )
        h.add_scene(alien_scene)
    except Exception:
        h.restore_screen()
        raise
    h.run()
