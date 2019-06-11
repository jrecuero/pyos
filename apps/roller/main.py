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
    Panel,
    # update_nobj,
    # render_nobj,
    update_scene,
    render_scene,
)


class RollerScene(Scene):
    def __init__(self):
        super(RollerScene, self).__init__("Roller Scene")
        self.border = False
        self.max_y: int = curses.LINES - 2
        self.max_x: int = curses.COLS - 1
        self.dialog_screen = {
            "y": 0,
            "x": 0,
            "dy": int(self.max_y / 2) + 1,
            "dx": self.max_x,
        }
        self.prompt_screen = {
            "y": int(self.max_y / 2) + 1,
            "x": 0,
            "dy": int(self.max_y / 2) - 2,
            "dx": self.max_x,
        }
        self.status_screen = {"y": self.max_y - 2, "x": 0, "dy": 2, "dx": self.max_x}
        self.actions = ["talk", "move", "look", "exit"]

    def user_input(self, inputa):
        if inputa and inputa == "exit":
            self.del_object(self.prompt)
            exit(0)
        elif inputa and inputa in self.actions:
            self.user_input.set_text("Action:  '{}'".format(inputa))
        else:
            self.user_input.set_text("Action not available")
        self.prompt.clear()
        self.prompt.set_capture()

    def setup(self, screen: Any):
        # self.add_object(BoxText(self.max_y - 2, 0, "Talk\tMove\tLook", 2, self.max_x))
        self.add_object(
            BoxText(
                self.status_screen["y"],
                self.status_screen["x"],
                "\t".join(self.actions),
                self.status_screen["dy"],
                self.status_screen["dx"],
            )
        )
        # self.add_object(Box(self.max_y - 8, 0, 8, self.max_x))
        # self.add_object(
        #     Box(
        #         self.prompt_screen["y"],
        #         self.prompt_screen["x"],
        #         self.prompt_screen["dy"],
        #         self.prompt_screen["dx"],
        #     )
        # )
        self.prompt_panel = Panel(
            self.prompt_screen["y"],
            self.prompt_screen["x"],
            self.prompt_screen["dy"],
            self.prompt_screen["dx"],
        )
        self.add_object(self.prompt_panel)
        # self.add_object(Box(0, 0, self.max_y, self.max_x))
        self.add_object(
            Box(
                self.dialog_screen["y"],
                self.dialog_screen["x"],
                self.dialog_screen["dy"],
                self.dialog_screen["dx"],
            )
        )
        self.add_object(Box(0, 0, self.max_y, self.max_x))
        # self.prompt = TextInput(self.max_y - 7, 1, "> ", self.user_input)
        # self.prompt = TextInput(
        #     self.prompt_screen["y"] + 1,
        #     self.prompt_screen["x"] + 1,
        #     "> ",
        #     self.user_input,
        # )
        # self.add_object(self.prompt)
        self.prompt = TextInput(1, 1, "> ", self.user_input)
        self.add_to_panel(self.prompt_panel, self.prompt)
        # self.user_input = String(self.max_y - 6, 1, "")
        # self.user_input = String(
        #     self.prompt_screen["y"] + 2, self.prompt_screen["x"] + 1, ""
        # )
        # self.add_object(self.user_input)
        self.user_input = String(2, 1, "")
        self.add_to_panel(self.prompt_panel, self.user_input)
        self.kh = KeyHandler({})
        self.kh.register("x", lambda: exit(0))

    @update_scene
    def update(self, screen: Any, *events: Event) -> List[Event]:
        event_to_return: List[Event] = []
        for event in events:
            if event.evt == EVT.ENG.KEY:
                event_to_return.extend(self.kh.update(event))
        return event_to_return

    @render_scene
    def render(self, screen: Any) -> List[Event]:
        event_to_return: List[Event] = []
        return event_to_return


if __name__ == "__main__":
    h = Handler()
    roller_scene = RollerScene()
    h.add_scene(roller_scene)
    h.run()
