from typing import List
from engine import (
    EVT,
    Handler,
    Scene,
    Box,
    String,
    Input,
    BoxText,
    KeyHandler,
    Event,
    FlashText,
    TimeUpdater,
    EventNextScene,
    update_scene,
    Selector,
)


class SceneMain(Scene):
    def __init__(self):
        super(SceneMain, self).__init__()
        self.select_obj = None
        self.input_obj = None
        self.timer = None
        self.t_counter = 0

    def setup(self):
        def handle_t():
            self.timer.enable = not self.timer.enable
            return []

        def handle_z():
            self.enable = False
            return []

        def handle_n():
            return [EventNextScene()]

        st = " Engine Example "
        self.add_object(Box(0, 0, 2, len(st) + 2))
        self.add_object(String(1, 1, st))
        self.select_obj = Selector(3, 0, ["Yes", "No", "Cancel"], selected=2)
        self.add_object(self.select_obj)
        self.input_obj = Input(5, 0, "Name: ")
        self.add_object(self.input_obj)
        self.kh = KeyHandler(
            {
                "x": lambda: exit(0),
                "t": handle_t,
                "z": handle_z,
                "n": lambda: [EventNextScene()],
            }
        )

    @update_scene
    def update(self, *events: Event) -> List[Event]:
        event_to_return: List[Event] = []
        for event in events:
            if event.evt == EVT.ENG.KEY:
                event_to_return.extend(self.kh.update(event))
            elif event.evt == EVT.ENG.TIMER:
                if event.get_timer() == self.timer:
                    self.t_counter += 1
                    self.add_object(
                        String(11, 0, "Timeout expired: {}".format(self.t_counter))
                    )
                    if self.t_counter == 10:
                        event_to_return.append(EventNextScene())
            elif event.evt == EVT.ENG.INPUT:
                msg = event.get_input()
                self.add_object(BoxText(5, 0, " Your name is {} ".format(msg)))
                self.del_object(self.input_obj)
                self.input_obj = None
                self.timer = self.new_timer(100)
            elif event.evt == EVT.ENG.SELECT:
                msg = event.get_selected_data()
                self.add_object(BoxText(8, 0, " Data {} ".format(msg)))
                self.del_object(self.select_obj)
                self.select_obj = None
            else:
                event_to_return.append(event)
        return event_to_return


class SceneLast(Scene):
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

        self.add_object(FlashText(0, 0, "last page", self.new_timer(50), on=1, off=1))
        self.add_object(TimeUpdater(1, 0, "@copyright", self.new_timer(100), updater))

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
