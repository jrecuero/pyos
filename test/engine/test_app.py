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
from engine.nobject import String, Gauge, Spinner, SpinnerScroll, Input

c_marked = curses.A_BOLD | curses.A_UNDERLINE
c_normal = curses.A_NORMAL


class SceneTwo(Scene):
    def __init__(self):
        super(SceneTwo, self).__init__("Main")

    def setup(self, screen: Any):
        self.name: List[str] = []
        self.add_object(Input(2, 5, "Name: ", self.name))
        self.add_object(Spinner(4, 5, 0, 10, 5))
        self.add_object(SpinnerScroll(5, 5, 0, 100, 50, 5))
        self.add_object(Gauge(10, 5, 1, -1, self.new_timer(50), 20, 7))
        self.g1 = Gauge(11, 5, 1, -1, None, 20, 7)
        self.g1_counter = 0
        self.add_object(self.g1)
        self.kh = KeyHandler({})
        self.kh.register("x", lambda: exit(0))

    @update_scene
    def update(self, screen: Any, *events: Event) -> List[Event]:
        event_to_return: List[Event] = []
        for event in events:
            if event.evt == EVT.ENG.KEY:
                self.g1.call(inc=1)
                event_to_return.extend(self.kh.update(event))
            elif event.evt == EVT.ENG.INPUT:
                # msg = event.get_input()
                if self.name:
                    self.add_object(
                        String(3, 5, "Your name is {} ".format(self.name[0]))
                    )
                self.g1.call(inc=10)
            else:
                event_to_return.append(event)
        return event_to_return


if __name__ == "__main__":
    h = Handler()
    scene_two = SceneTwo()
    scene_two.colors(
        [
            (curses.COLOR_RED, curses.COLOR_BLACK),
            (curses.COLOR_YELLOW, curses.COLOR_BLACK),
        ]
    )
    h.add_scene(scene_two)
    h.run()
