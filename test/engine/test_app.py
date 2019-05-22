from typing import List
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

    def setup(self):
        def updater(message: str) -> str:
            # log.Scene("SceneMain").Method("updater").call()
            if message == "@copyright":
                return "by jose carlos"
            elif message == "by jose carlos":
                return "San Jose, 2018"
            elif message == "San Jose, 2018":
                return ""
            else:
                return "@copyright"

        def caller():
            fname = self.fname[0] if self.fname else ""
            lname = self.lname[0] if self.lname else ""
            return "You are {} {}".format(fname, lname)

        self.add_object(XString(2, 4, "E", c_marked))
        self.add_object(XString(2, 5, "ngine", curses.color_pair(1)))
        self.add_object(XString(2, 11, "Example:", c_marked | curses.color_pair(2)))
        self.add_object(
            Formatted(2, 20, [["I", c_marked], ["nput "], ["E", c_marked], ["xit"]])
        )
        self.add_object(Block(3, 4, "python curses engine\n@2019"))
        self.add_object(Box(1, 2, 4, 32))
        self.add_object(BoxText(6, 2, "User Data\n---------"))
        self.fname: List[str] = []
        self.lname: List[str] = []
        self.add_object(Input(10, 2, "First Name: ", self.fname))
        self.add_object(Input(11, 2, "Last Name: ", self.lname))
        self.add_object(
            FlashText(14, 2, "press any key", self.new_timer(50), on=1, off=1)
        )
        self.add_object(TimeUpdater(15, 2, "@copyright", self.new_timer(100), updater))
        self.add_object(Caller(16, 2, caller))
        self.add_object(Selector(17, 2, ["Yes", "No", "Cancel"], selected=2))
        self.add_object(ScrollSelector(19, 2, ["Yes", "No", "Cancel"], selected=1))
        # self.kh = KeyHandler({"x": lambda: exit(0), "n": lambda: [EventNextScene()]})
        self.kh = KeyHandler({})
        self.kh.register("x", lambda: exit(0))
        self.kh.register("n", lambda: [EventNextScene()])
        self.kh.register("l", lambda: [EventLastScene()])

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
            elif event.evt == EVT.ENG.SELECT:
                msg = event.get_selected_data()
                self.add_object(String(18, 2, "Selected: {}".format(msg)))
            else:
                event_to_return.append(event)
        return event_to_return


class SceneKeyHandler(Scene):
    @update_scene
    def update(self, *events: Event) -> List[Event]:
        event_to_return: List[Event] = []
        for event in events:
            # event.exit_on_key("x")
            if event.evt == EVT.ENG.KEY:
                event_to_return.extend(self.kh.update(event))
        return event_to_return


class SceneSecond(SceneKeyHandler):
    def __init__(self):
        super(SceneSecond, self).__init__("Second")

    def setup(self):
        self.screen = curses.newwin(20, 40, 10, 10)
        self.add_object(BoxText(4, 2, "SECOND PAGE"))
        self.kh = KeyHandler({})
        self.kh.register("x", lambda: exit(0))
        self.kh.register("n", lambda: [EventNextScene()])
        self.kh.register("p", lambda: [EventPrevScene()])
        self.kh.register("f", lambda: [EventFirstScene()])


class SceneThird(SceneKeyHandler):
    def __init__(self):
        super(SceneThird, self).__init__("Second")

    def setup(self):
        self.add_object(BoxText(1, 1, "THIRD PAGE"))
        self.add_object(
            Menu(
                5,
                2,
                (
                    (
                        "^File",
                        (
                            ("^Open", None),
                            ("^Save", (("^Text", None), ("^Html", None))),
                            ("^Close", None),
                        ),
                    ),
                    ("^Action", (("^Execute", None), ("^Terminate", None))),
                    ("^Exit", None),
                ),
                dx=40,
            )
        )
        self.kh = KeyHandler({})
        self.kh.register("x", lambda: exit(0))
        self.kh.register("n", lambda: [EventNextScene()])
        self.kh.register("p", lambda: [EventPrevScene()])
        self.kh.register("f", lambda: [EventFirstScene()])


class SceneLast(SceneKeyHandler):
    def __init__(self):
        super(SceneLast, self).__init__("Last")

    def setup(self):
        self.screen = curses.newwin(40, 40, 5, 5)
        self.add_object(String(2, 2, "This is the last page"))
        self.add_object(BoxText(4, 2, "This is the last page"))
        # self.add_object(String(11, 3, "1234567890"))
        # self.add_object(Box(10, 2, 2, 12))
        # self.add_object(Box(10, 15, 2, 12))
        self.add_object(BoxGrid(10, 2, 2, 4, 4, 4))
        self.kh = KeyHandler({})
        self.kh.register("x", lambda: exit(0))
        self.kh.register("p", lambda: [EventPrevScene()])
        self.kh.register("n", lambda: [EventFirstScene()])


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
    h.add_scene(SceneSecond())
    h.add_scene(SceneThird())
    h.add_scene(SceneLast())
    h.run()
