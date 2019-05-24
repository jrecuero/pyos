from typing import List, Any
import curses
from engine import (
    # log,
    EVT,
    Handler,
    Scene,
    String,
    XString,
    Formatted,
    Block,
    Box,
    BoxGrid,
    BoxText,
    FlashText,
    TimeUpdater,
    Caller,
    Input,
    Selector,
    ScrollSelector,
    Menu,
    KeyHandler,
    Event,
    EventNextScene,
    EventPrevScene,
    EventFirstScene,
    EventLastScene,
    update_scene,
)

c_marked = curses.A_BOLD | curses.A_UNDERLINE
c_normal = curses.A_NORMAL


class SceneMain(Scene):
    def __init__(self):
        super(SceneMain, self).__init__("Main")

    def setup(self, screen: Any):
        self.fname: List[str] = []
        self.lname: List[str] = []
        self.add_object(Input(10, 2, "First Name: ", self.fname))
        # self.add_object(Input(11, 2, "Last Name: ", self.lname))
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
                if self.fname:
                    self.add_object(
                        String(12, 2, "Your first name is {} ".format(self.fname[0]))
                    )
                if self.lname:
                    self.add_object(
                        String(13, 2, "Your last name is {} ".format(self.lname[0]))
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
