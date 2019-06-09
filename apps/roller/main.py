from typing import Any, List
# import random
import curses
from engine import (
    # log,
    EVT,
    Handler,
    Scene,
    Event,
    TextInput,
    String,
    Box,
    BoxText,
    # Caller,
    KeyHandler,
    update_scene,
    # render_scene,
    # update_nobj,
    # render_nobj,
)


class RollerScene(Scene):
    def __init__(self):
        super(RollerScene, self).__init__("Roller Scene")
        self.border = False
        self.max_y: int = curses.LINES - 2
        self.max_x: int = curses.COLS - 1

    def user_input(self, inputa):
        if inputa:
            self.user_input.set_text("You selected '{}'".format(inputa))
            self.prompt.clear()
            self.prompt.set_capture()
        else:
            self.del_object(self.prompt)
            self.user_input.set_text("You didn't select anything")

    def setup(self, screen: Any):
        self.add_object(BoxText(self.max_y - 2, 0, "Talk\tMove\tLook", 2, self.max_x))
        self.add_object(Box(self.max_y - 8, 0, 8, self.max_x))
        self.add_object(Box(0, 0, self.max_y, self.max_x))
        self.prompt = TextInput(self.max_y - 7, 1, "> ", self.user_input)
        self.add_object(self.prompt)
        self.user_input = String(self.max_y - 6, 1, "")
        self.add_object(self.user_input)
        self.kh = KeyHandler({})
        self.kh.register("x", lambda: exit(0))

    @update_scene
    def update(self, screen: Any, *events: Event) -> List[Event]:
        event_to_return: List[Event] = []
        for event in events:
            if event.evt == EVT.ENG.KEY:
                event_to_return.extend(self.kh.update(event))
        return event_to_return


if __name__ == "__main__":
    h = Handler()
    roller_scene = RollerScene()
    h.add_scene(roller_scene)
    h.run()
