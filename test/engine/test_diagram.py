from typing import List, Any
import curses
from engine import (
    # log,
    EVT,
    Handler,
    Scene,
    KeyHandler,
    Event,
    update_scene,
)

from engine.nobject import Histogram, HistoBar

c_marked = curses.A_BOLD | curses.A_UNDERLINE
c_normal = curses.A_NORMAL


class SceneOne(Scene):
    def __init__(self):
        super(SceneOne, self).__init__("Main")

    def histobar(self, screen: Any):
        data = [(y, 3 * y) for y in range(10)]
        data.extend([(18 - y, 30 + 3 * y) for y in range(10)])
        self.add_object(HistoBar(1, 1, 20, 200, data, x_width=2))

    def histogram(self, screen: Any):
        data = [5, 15, 10, 17, 11]
        bar_titles = ["ONE", "TWO", "THREE", "FOUR", "FIVE"]
        bar_colors = [curses.color_pair(x + 1) for x in range(4)]
        self.add_object(
            Histogram(
                1,
                1,
                20,
                200,
                data,
                x_width=10,
                bar_titles=bar_titles,
                bar_colors=bar_colors,
            )
        )

    def setup(self, screen: Any):
        # self.histobar(screen)
        self.histogram(screen)
        self.kh = KeyHandler({})
        self.kh.register("x", lambda: exit(0))

    @update_scene
    def update(self, screen: Any, *events: Event) -> List[Event]:
        event_to_return: List[Event] = []
        for event in events:
            if event.evt == EVT.ENG.KEY:
                event_to_return.extend(self.kh.update(event))
            else:
                event_to_return.append(event)
        return event_to_return


if __name__ == "__main__":
    h = Handler()
    scene_one = SceneOne()
    scene_one.colors(
        [
            (curses.COLOR_RED, curses.COLOR_BLACK),
            (curses.COLOR_YELLOW, curses.COLOR_BLACK),
            (curses.COLOR_BLUE, curses.COLOR_BLACK),
            (curses.COLOR_CYAN, curses.COLOR_BLACK),
        ]
    )
    h.add_scene(scene_one)
    h.run()
