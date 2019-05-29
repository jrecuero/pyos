from typing import List, Any
import curses
from engine import (
    # log,
    EVT,
    Handler,
    Scene,
    String,
    # XString,
    # Formatted,
    # Block,
    # Box,
    # BoxGrid,
    # BoxText,
    # FlashText,
    Gauge,
    Spinner,
    SpinnerScroll,
    # Caller,
    Input,
    # Selector,
    # ScrollSelector,
    # Menu,
    KeyHandler,
    Event,
    # EventNextScene,
    # EventPrevScene,
    # EventFirstScene,
    # EventLastScene,
    update_scene,
)

c_marked = curses.A_BOLD | curses.A_UNDERLINE
c_normal = curses.A_NORMAL


class SceneMain(Scene):
    def __init__(self):
        super(SceneMain, self).__init__("Main")

    def setup(self, screen: Any):
        self.name: List[str] = []
        self.add_object(Input(2, 5, "Name: ", self.name))
        self.add_object(Spinner(4, 5, 0, 10, 5))
        self.add_object(SpinnerScroll(5, 5, 0, 100, 50, 5))
        self.add_object(Gauge(10, 5, 1, -1, self.new_timer(50), 20, 7))
        self.kh = KeyHandler({})
        self.kh.register("x", lambda: exit(0))

    @update_scene
    def update(self, *events: Event) -> List[Event]:
        event_to_return: List[Event] = []
        for event in events:
            if event.evt == EVT.ENG.KEY:
                event_to_return.extend(self.kh.update(event))
            elif event.evt == EVT.ENG.INPUT:
                # msg = event.get_input()
                if self.name:
                    self.add_object(
                        String(3, 5, "Your name is {} ".format(self.name[0]))
                    )
            else:
                event_to_return.append(event)
        return event_to_return


if __name__ == "__main__":
    h = Handler()
    main_scene = SceneMain()
    main_scene.colors(
        [
            (curses.COLOR_RED, curses.COLOR_BLACK),
            (curses.COLOR_YELLOW, curses.COLOR_BLACK),
        ]
    )
    h.add_scene(main_scene)
    h.run()
