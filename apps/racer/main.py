from typing import List, Any
import curses
import random
from engine import (
    # log,
    EVT,
    Handler,
    Scene,
    Event,
    update_scene,
    update_nobj,
    KeyHandler,
)
from engine.nobject import String, HorizontalPath, TimerText, BoxText


course: List[int] = [
    0,
    0,
    0,
    0,
    0,
    0,
    1,
    1,
    1,
    2,
    2,
    2,
    3,
    3,
    3,
    2,
    2,
    2,
    1,
    1,
    1,
    1,
    0,
    0,
    0,
    0,
    1,
    2,
    3,
    4,
    5,
    4,
    3,
    2,
    1,
    0,
    -1,
    -2,
    -3,
    -2,
    -1,
    0,
    0,
    0,
    1,
    1,
    0,
    0,
    -1,
    -1,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
]


class Dice(BoxText):
    def __init__(
        self, y: int, x: int, value: int, fmt=curses.A_NORMAL, cfmt=curses.A_NORMAL
    ):
        super(Dice, self).__init__(y, x, "", dy=4, dx=4, fmt=fmt, cfmt=cfmt)
        self.__dice = [
            "   \n   \n   ",
            "   \n * \n   ",
            "*  \n   \n  *",
            "*  \n * \n  *",
            "* *\n   \n* *",
            "* *\n * \n* *",
            "* *\n* *\n* *",
            "* *\n***\n* *",
            "***\n* *\n***",
            "***\n***\n***",
        ]
        self.__value: int = 0
        self.set(value)
        self.__rolling: bool = False
        self.__counter: int = 0
        self.__speed: int = 10

    def set(self, value: int):
        assert 0 <= value <= 9, "Invalid Value: 0 <= x <= 9"
        self.__value = value
        self.text_data = self.__dice[self.__value]

    def start(self, speed: int = None):
        self.__rolling = True
        self.__counter = 0
        self.__speed = speed if speed else self.__speed
        return []

    def stop(self):
        self.__rolling = False
        return []

    def get(self) -> int:
        return self.__value

    def roll(self):
        self.set(random.randint(0, 9))

    @update_nobj
    def update(self, screen: Any, *events: Event) -> List[Event]:
        if self.__rolling and self.__counter == self.__speed:
            self.__counter = 0
            self.roll()
        self.__counter += 1
        return super(Dice, self).update(screen, *events)


class BoardScene(Scene):
    def __init__(self):
        super(BoardScene, self).__init__("Racer")
        self.border = False

    def setup(self, screen):
        color_1 = curses.color_pair(1)
        color_2 = curses.color_pair(2)
        dice = Dice(1, 5, 0, fmt=color_2)

        def updater(_course: List[int], start_y: int, start_x: int, limit: int):
            _index: int = 0
            _pindex: int = 0
            _rolling: bool = False

            def _updater(y: int, x: int, message: str, fmt) -> str:
                nonlocal _index, _pindex, _rolling
                if _rolling:
                    _rolling = False
                    _pindex = _index
                    _index += dice.get()
                    if _index >= limit:
                        _index = 0
                        _pindex = 0
                        return (start_y, start_x, message, fmt)
                    delta = _course[_index] - _course[_pindex]
                    dice.stop()
                    return (y - delta, x + dice.get(), message, fmt)
                else:
                    _rolling = True
                    dice.start()
                    return (y, x, message, fmt)

            return _updater

        def number(x: int):
            if x > 0:
                return "+{}".format(x)
            elif x < 0:
                return "{}".format(x)
            return "{} ".format(x)

        self.add_object(dice)

        y: int = 25
        x: int = 1
        dy: int = 5
        self.add_object(HorizontalPath(y, x, dy, course[:53], color_1))

        self.add_object(String(30, 1, "".join([number(x)[0] for x in course[:53]])))
        self.add_object(String(31, 1, "".join([number(x)[1] for x in course[:53]])))
        mobile = "A"
        # self.add_object(
        #     TimerText(24, 1, mobile, self.new_timer(100), updater(course, 24, 1, 52))
        # )
        self.add_object(
            TimerText(21, 1, mobile, self.new_timer(100), updater(course, 21, 1, 52))
        )

        self.kh = KeyHandler({})
        self.kh.register("x", lambda: exit(0))
        self.kh.register("r", lambda: dice.start())
        self.kh.register("s", lambda: dice.stop())

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
            (curses.COLOR_RED, curses.COLOR_BLUE),
            (curses.COLOR_BLACK, curses.COLOR_WHITE),
        ]
    )
    h.add_scene(board_scene)
    h.run()
