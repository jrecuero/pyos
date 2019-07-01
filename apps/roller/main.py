from typing import Any, List

# import random
import curses
from engine import (
    # log,
    EVT,
    Handler,
    Scene,
    Event,
    KeyHandler,
    Panel,
    update_scene,
    render_scene,
)
from engine.nobject import TextInput, String, Box, BoxText


class RollerScene(Scene):
    def __init__(self):
        super(RollerScene, self).__init__("Roller Scene")
        self.border = False
        self.max_y: int = curses.LINES - 2
        self.max_x: int = curses.COLS - 1
        self.dialog_screen = {
            "y": 0,
            "x": 0,
            # "dy": int(self.max_y / 2) + 1,
            "dy": self.max_y - 8,
            "dx": int(3 * self.max_x / 4),
        }
        self.infoma_screen = {
            "y": 0,
            "x": int(3 * self.max_x / 4) + 1,
            # "dy": int(self.max_y / 2) + 1,
            "dy": self.max_y - 8,
            "dx": int(self.max_x / 4),
        }
        self.prompt_screen = {
            # "y": int(self.max_y / 2) + 1,
            "y": self.max_y - 7,
            "x": 0,
            # "dy": int(self.max_y / 2) - 2,
            "dy": 4,
            "dx": self.max_x,
        }
        self.status_screen = {"y": self.max_y - 2, "x": 0, "dy": 2, "dx": self.max_x}
        self.stage: str = "CONFIG"
        from grafo.cli import Builder
        import os

        subdir = "commands"
        path = os.path.join(os.path.dirname(__file__), subdir)
        self.builder = Builder()
        self.builder.create_grafo(path)
        self.actions_conf: List[str] = ["first:<str>", "last:<str>", "done"]
        self.actions_work: List[str] = ["talk", "move", "look", "exit"]

    def user_input(self, inputa):
        if self.stage == "WORK":
            if inputa and inputa == "exit":
                self.del_object(self.prompt)
                exit(0)
            elif inputa and inputa in self.actions_work:
                self.user_input.set_text("Action:  '{}'".format(inputa))
            else:
                self.user_input.set_text("Action not available")
        elif self.stage == "CONFIG":
            result = self.builder.handler.run(inputa)
            self.user_input.set_text("{}".format(result))
            # if inputa and inputa == "done":
            #     self.status_textbox.set_text("\t".join(self.actions_work))
            #     self.stage = "WORK"
            # else:
            #     user_input = inputa.split(":")
            #     if inputa and user_input[0] == "first":
            #         self.first_name.set_text(user_input[1])
            #     elif inputa and user_input[0] == "last":
            #         self.last_name.set_text(user_input[1])
            #     else:
            #         self.user_input.set_text("Action not available")
        self.prompt.clear()
        self.prompt.set_capture()

    def setup(self, screen: Any):
        self.status_textbox = BoxText(
            self.status_screen["y"],
            self.status_screen["x"],
            "\t".join(self.actions_conf),
            self.status_screen["dy"],
            self.status_screen["dx"],
        )
        self.add_object(self.status_textbox)
        self.prompt_panel = Panel(
            self.prompt_screen["y"],
            self.prompt_screen["x"],
            self.prompt_screen["dy"],
            self.prompt_screen["dx"],
        )
        self.add_object(self.prompt_panel)
        self.add_object(
            Box(
                self.dialog_screen["y"],
                self.dialog_screen["x"],
                self.dialog_screen["dy"],
                self.dialog_screen["dx"],
            )
        )
        self.infoma_panel = Panel(
            self.infoma_screen["y"],
            self.infoma_screen["x"],
            self.infoma_screen["dy"],
            self.infoma_screen["dx"],
        )
        self.add_object(self.infoma_panel)
        # self.add_object(Box(0, 0, self.max_y, self.max_x))
        self.prompt = TextInput(1, 1, "> ", self.user_input)
        self.add_to_panel(self.prompt_panel, self.prompt)
        self.user_input = String(2, 1, "")
        self.add_to_panel(self.prompt_panel, self.user_input)
        self.first_name = String(1, 1, "First Name")
        self.last_name = String(2, 1, "Last Name")
        self.add_to_panel(self.infoma_panel, self.first_name)
        self.add_to_panel(self.infoma_panel, self.last_name)
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
