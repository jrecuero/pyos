import curses
from engine import (
    set_plugin,
    Handler,
    Scene,
    Arena,
    ArrowKeyHandler,
    Move,
    BB,
    Point,
    update_scene,
    render_scene,
    EVT,
    log,
)
from engine.dplugs import CursesPlugin
from engine.physic import ShooterShape


class GameHandler(Arena):
    def __init__(self, y: int, x: int, max_y: int, max_x: int, **kwargs):
        super(GameHandler, self).__init__(x, y, max_y, max_x)


class SurviveScene(Scene):
    def __init__(self):
        super(SurviveScene, self).__init__("Survive Scene")
        self.min_y = 2
        self.min_x = 2
        self.max_y = curses.LINES - 2
        self.max_x = curses.COLS - 1

    def setup(self, screen):
        self.gh = GameHandler(self.min_y, self.min_y, self.max_y - 4, self.max_x - 4)
        self.ship = ShooterShape(timeout=0)
        self.ship.append(
            BB(
                "#",
                pos=Point(self.gh.dy - 2, 5),
                move=Move.NONE,
                fmt=curses.color_pair(2),
            )
        )
        self.gh.add_shape(self.ship)
        self.add_object(self.gh)
        self.kh = ArrowKeyHandler(
            left=self.ship.move(Move.LEFT),
            right=self.ship.move(Move.RIGHT),
            up=self.ship.move(Move.UP),
            down=self.ship.move(Move.DOWN),
        )

    @update_scene
    def update(self, scene, *events):
        event_to_return = []
        for event in events:
            if event.evt == EVT.ENG.KEY:
                log.KeyInput(chr(event.get_key())).info()
                event_to_return.extend(self.kh.update(event))
        return event_to_return

    @render_scene
    def render(self, screen):
        return super(SurviveScene, self).render(screen)


if __name__ == "__main__":
    set_plugin(CursesPlugin())
    h = Handler()
    try:
        survive_scene = SurviveScene()
        survive_scene.colors(
            [
                (curses.COLOR_RED, curses.COLOR_BLACK),
                (curses.COLOR_YELLOW, curses.COLOR_BLACK),
                (curses.COLOR_BLACK, curses.COLOR_WHITE),
            ]
        )
        h.add_scene(survive_scene)
    except Exception:
        h.restore_screen()
        raise
    h.run()
