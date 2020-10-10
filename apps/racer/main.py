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
from engine.nobject import String, HorizontalPath, TimerText, BoxText, ShapeFromPath


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
    1,
    2,
    2,
    2,
    2,
    3,
    3,
    3,
    3,
    3,
    2,
    2,
    2,
    2,
    2,
    1,
    1,
    1,
    1,
    1,
    0,
    0,
    0,
    0,
    0,
    -1,
    -1,
    -1,
    -1,
    -2,
    -2,
    -2,
    -2,
    -3,
    -3,
    -3,
    -3,
    -3,
    -2,
    -2,
    -2,
    -2,
    -2,
    -1,
    -1,
    -1,
    -1,
    -1,
    0,
    0,
    0,
    1,
    1,
    1,
    1,
    1,
    1,
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
        self,
        y: int,
        x: int,
        value: int = 0,
        _min: int = 1,
        _max: int = 2,
        _speed: int = 5,
        fmt=curses.A_NORMAL,
        cfmt=curses.A_NORMAL,
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
        self.__value: int = value if _min <= value <= _max else _min
        self.__min: int = _min
        self.__max: int = _max
        self.__rolling: bool = False
        self.__counter: int = 0
        self.__speed: int = _speed
        self.set(self.__value)

    def set(self, value: int):
        assert (
            self.__min <= value <= self.__max
        ), "Invalid Value: {} <= {} <= {}".format(self.__min, value, self.__max)
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
        self.set(random.randint(self.__min, self.__max))

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
        self.play: bool = True
        color_1 = curses.color_pair(1)
        # color_2 = curses.color_pair(2)
        dices = [Dice(1, 5), Dice(6, 5), Dice(1, 15), Dice(6, 15)]

        def play(flag: bool):
            self.play = flag
            return []

        def updater(_course: List[int], start_y: int, start_x: int, limit: int, dice):
            _index: int = 0
            _pindex: int = 0
            _rolling: bool = False

            def _updater(y: int, x: int, message: str, fmt) -> str:
                nonlocal _index, _pindex, _rolling
                if self.play:
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
                else:
                    dice.stop()
                    _rolling = False
                    return (y, x, message, fmt)

            return _updater

        def number(x: int):
            if x > 0:
                return "+{}".format(x)
            elif x < 0:
                return "{}".format(x)
            return "{} ".format(x)

        y: int = 10
        x: int = 30
        dy: int = 5
        self.add_object(HorizontalPath(y, x, dy, course[:-1], color_1))

        # self.add_object(String(30, 1, "".join([number(x)[0] for x in course[:53]])))
        # self.add_object(String(31, 1, "".join([number(x)[1] for x in course[:53]])))
        mobile = "A"
        for i, dice in enumerate(dices):
            self.add_object(ShapeFromPath(6 + i, x, course[1:-1], "."))
            self.add_object(dice)
            self.add_object(
                TimerText(
                    6 + i,
                    30,
                    mobile,
                    self.new_timer(100),
                    updater(course, 6 + i, 30, len(course) - 1, dice),
                )
            )

        self.kh = KeyHandler({})
        self.kh.register("x", lambda: exit(0))
        self.kh.register("p", lambda: play(True))
        self.kh.register("s", lambda: play(False))

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
