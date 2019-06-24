from typing import List, Any
import curses
from engine import (
    # log,
    EVT,
    Handler,
    Scene,
    Event,
    # NObject,
    Char,
    # String,
    BoxText,
    # Caller,
    # ArrowKeyHandler,
    update_scene,
    # render_scene,
    KeyHandler,
)


class Dice(object):
    def __init__(self, y: int, x: int, value: int):
        self.__dice = [
            "   \n   \n   ",
            "   \n * \n   ",
            "*  \n   \n  *",
            "*  \n * \n  *",
            "* *\n   \n* *",
            "* *\n * \n* *",
            "* *\n* *\n* *",
        ]
        self.dice = self.__dices[value]

    def nobject(self):
        pass


class BoardScene(Scene):
    def __init__(self):
        super(BoardScene, self).__init__("Racer")
        self.border = False

    def setup(self, screen):
        color_1 = curses.color_pair(1)
        color_2 = curses.color_pair(2)
        d1 = "   \n * \n   "
        d2 = "*  \n   \n  *"
        d3 = "*  \n * \n  *"
        d4 = "* *\n   \n* *"
        d5 = "* *\n * \n* *"
        d6 = "* *\n* *\n* *"
        dice_1 = BoxText(1, 0, d1, dy=4, dx=4, fmt=color_2, cfmt=color_1)
        dice_2 = BoxText(1, 5, d2, dy=4, dx=4, fmt=color_2, cfmt=color_1)
        dice_3 = BoxText(1, 10, d3, dy=4, dx=4, fmt=color_2, cfmt=color_1)
        dice_4 = BoxText(1, 15, d4, dy=4, dx=4, fmt=color_2, cfmt=color_1)
        dice_5 = BoxText(1, 20, d5, dy=4, dx=4, fmt=color_2, cfmt=color_1)
        dice_6 = BoxText(1, 25, d6, dy=4, dx=4, fmt=color_2, cfmt=color_1)
        self.add_object(dice_1)
        self.add_object(dice_2)
        self.add_object(dice_3)
        self.add_object(dice_4)
        self.add_object(dice_5)
        self.add_object(dice_6)
        mobile = "*"
        for i in range(5):
            self.add_object(Char(20, 10 + i, chr(9473), color_1))
            self.add_object(Char(21, 10 + i, mobile))
            self.add_object(Char(22, 10 + i, mobile))
            self.add_object(Char(23, 10 + i, mobile))
            self.add_object(Char(24, 10 + i, mobile))
            self.add_object(Char(25, 10 + i, chr(9473), color_1))

        self.add_object(Char(19, 15, chr(9487), color_1))
        self.add_object(Char(20, 15, chr(9499), color_1))
        self.add_object(Char(21, 15, mobile))
        self.add_object(Char(22, 15, mobile))
        self.add_object(Char(23, 15, mobile))
        self.add_object(Char(24, 15, mobile))
        self.add_object(Char(25, 15, chr(9473), color_1))

        self.add_object(Char(19, 16, chr(9473), color_1))
        self.add_object(Char(20, 16, mobile))
        self.add_object(Char(21, 16, mobile))
        self.add_object(Char(22, 16, mobile))
        self.add_object(Char(23, 16, mobile))
        self.add_object(Char(24, 16, chr(9487), color_1))
        self.add_object(Char(25, 16, chr(9499), color_1))

        for i in range(5):
            self.add_object(Char(19, 17 + i, chr(9473), color_1))
            self.add_object(Char(20, 17 + i, mobile))
            self.add_object(Char(21, 17 + i, mobile))
            self.add_object(Char(22, 17 + i, mobile))
            self.add_object(Char(23, 17 + i, mobile))
            self.add_object(Char(24, 17 + i, chr(9473), color_1))

        self.add_object(Char(18, 22, chr(9487), color_1))
        self.add_object(Char(19, 22, chr(9499), color_1))
        self.add_object(Char(20, 22, mobile))
        self.add_object(Char(21, 22, mobile))
        self.add_object(Char(22, 22, mobile))
        self.add_object(Char(23, 22, mobile))
        self.add_object(Char(24, 22, chr(9473), color_1))

        self.add_object(Char(18, 23, chr(9473), color_1))
        self.add_object(Char(19, 23, mobile))
        self.add_object(Char(20, 23, mobile))
        self.add_object(Char(21, 23, mobile))
        self.add_object(Char(22, 23, mobile))
        self.add_object(Char(23, 23, chr(9487), color_1))
        self.add_object(Char(24, 23, chr(9499), color_1))

        for i in range(5):
            self.add_object(Char(18, 24 + i, chr(9473), color_1))
            self.add_object(Char(19, 24 + i, mobile))
            self.add_object(Char(20, 24 + i, mobile))
            self.add_object(Char(21, 24 + i, mobile))
            self.add_object(Char(22, 24 + i, mobile))
            self.add_object(Char(23, 24 + i, chr(9473), color_1))

        self.add_object(Char(18, 29, chr(9473), color_1))
        self.add_object(Char(19, 29, mobile))
        self.add_object(Char(20, 29, mobile))
        self.add_object(Char(21, 29, mobile))
        self.add_object(Char(22, 29, mobile))
        self.add_object(Char(23, 29, chr(9491), color_1))
        self.add_object(Char(24, 29, chr(9495), color_1))

        self.add_object(Char(18, 30, chr(9491), color_1))
        self.add_object(Char(19, 30, chr(9495), color_1))
        self.add_object(Char(20, 30, mobile))
        self.add_object(Char(21, 30, mobile))
        self.add_object(Char(22, 30, mobile))
        self.add_object(Char(23, 30, mobile))
        self.add_object(Char(24, 30, chr(9473), color_1))

        for i in range(5):
            self.add_object(Char(19, 31 + i, chr(9473), color_1))
            self.add_object(Char(20, 31 + i, mobile))
            self.add_object(Char(21, 31 + i, mobile))
            self.add_object(Char(22, 31 + i, mobile))
            self.add_object(Char(23, 31 + i, mobile))
            self.add_object(Char(24, 31 + i, chr(9473), color_1))

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
    board_scene = BoardScene()
    board_scene.colors(
        [
            (curses.COLOR_RED, curses.COLOR_BLACK),
            (curses.COLOR_YELLOW, curses.COLOR_BLACK),
        ]
    )
    h.add_scene(board_scene)
    h.run()
