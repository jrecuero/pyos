from typing import List
from engine import (
    EVT,
    Handler,
    Scene,
    String,
    Block,
    Box,
    BoxText,
    FlashText,
    TimeUpdater,
    Caller,
    Input,
    Selector,
    ScrollSelector,
    KeyHandler,
    Event,
    EventNextScene,
    update_scene,
)


class SceneMain(Scene):
    def __init__(self):
        super(SceneMain, self).__init__()

    def setup(self):
        def updater(message: str) -> str:
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

        st = "Engine Example"
        self.add_object(String(1, 1, st))
        self.add_object(Block(2, 1, "python curses engine\n@2019"))
        self.add_object(Box(0, 0, 4, 32))
        self.add_object(BoxText(5, 0, "User Data\n---------"))
        self.fname: List[str] = []
        self.lname: List[str] = []
        self.add_object(Input(9, 0, "First Name: ", self.fname))
        self.add_object(Input(10, 0, "Last Name: ", self.lname))
        self.add_object(
            FlashText(13, 0, "press any key", self.new_timer(50), on=1, off=1)
        )
        self.add_object(TimeUpdater(14, 0, "@copyright", self.new_timer(100), updater))
        self.add_object(Caller(15, 0, caller))
        self.add_object(Selector(16, 0, ["Yes", "No", "Cancel"], selected=2))
        self.add_object(ScrollSelector(18, 0, ["Yes", "No", "Cancel"], selected=1))
        # self.kh = KeyHandler({"x": lambda: exit(0), "n": lambda: [EventNextScene()]})
        self.kh = KeyHandler({})
        self.kh.register("x", lambda: exit(0))
        self.kh.register("n", lambda: [EventNextScene()])

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
                        String(11, 0, "Your first name is {} ".format(self.fname[0]))
                    )
                if self.lname:
                    self.add_object(
                        String(12, 0, "Your last name is {} ".format(self.lname[0]))
                    )
            elif event.evt == EVT.ENG.SELECT:
                msg = event.get_selected_data()
                self.add_object(String(17, 0, "Selected: {}".format(msg)))
            else:
                event_to_return.append(event)
        return event_to_return


class SceneLast(Scene):
    def setup(self):
        self.add_object(String(10, 0, "This is the last page"))
        self.add_object(BoxText(12, 0, "This is the last page"))

    @update_scene
    def update(self, *events: Event) -> List[Event]:
        event_to_return: List[Event] = []
        for event in events:
            event.exit_on_key("x")
        return event_to_return


if __name__ == "__main__":
    h = Handler()
    h.add_scene(SceneMain())
    h.add_scene(SceneLast())
    h.run()
