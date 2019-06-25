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
    String,
    BoxText,
    # Caller,
    # TimerText,
    # ArrowKeyHandler,
    update_scene,
    # render_scene,
    KeyHandler,
    # Path,
    HPath,
    HPathCover,
    VPath,
    VPathCover,
    HorizontalPath,
    VerticalPath,
)


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

    def draw_segment(
        self, y: int, x: int, dy: int, _prev: int, _now: int, _next: int, fmt
    ) -> int:
        if _prev == _now == _next:
            self.add_object(Char(y, x, chr(9473), fmt))
            self.add_object(Char(y + dy, x, chr(9473), fmt))
            return y
        elif _next > _now:
            self.add_object(Char(y - 1, x, chr(9487), fmt))
            self.add_object(Char(y, x, chr(9499), fmt))
            if _prev == _now:
                self.add_object(Char(y + dy, x, chr(9473), fmt))
            else:
                self.add_object(Char(y + dy, x, chr(9487), fmt))
                self.add_object(Char(y + dy + 1, x, chr(9499), fmt))
            return y - 1
        elif _next < _now:
            if _prev == _now:
                self.add_object(Char(y, x, chr(9473), fmt))
            else:
                self.add_object(Char(y - 1, x, chr(9491), fmt))
                self.add_object(Char(y, x, chr(9495), fmt))
            self.add_object(Char(y + dy, x, chr(9491), fmt))
            self.add_object(Char(y + dy + 1, x, chr(9495), fmt))
            return y + 1
        elif _prev < _now:
            self.add_object(Char(y, x, chr(9473), fmt))
            self.add_object(Char(y + dy, x, chr(9487), fmt))
            self.add_object(Char(y + dy + 1, x, chr(9499), fmt))
            return y
        elif _prev > _now:
            self.add_object(Char(y - 1, x, chr(9491), fmt))
            self.add_object(Char(y, x, chr(9495), fmt))
            self.add_object(Char(y + dy, x, chr(9473), fmt))
            return y
        return y

    def setup(self, screen):
        def updater(_course: List[int], start_y: int, start_x: int, limit: int):
            _index: int = 0

            def _updater(y: int, x: int, message: str, fmt) -> str:
                nonlocal _index
                _index += 1
                if _index >= limit:
                    _index = 0
                    return (start_y, start_x, message, fmt)
                else:
                    delta = _course[_index] - _course[_index - 1]
                    return (y - delta, x + 1, message, fmt)

            return _updater

        def number(x: int):
            if x > 0:
                return "+{}".format(x)
            elif x < 0:
                return "{}".format(x)
            return "{} ".format(x)

        color_1 = curses.color_pair(1)
        color_2 = curses.color_pair(2)
        # d1 = "   \n * \n   "
        # d2 = "*  \n   \n  *"
        # d3 = "*  \n * \n  *"
        # d4 = "* *\n   \n* *"
        # d5 = "* *\n * \n* *"
        # d6 = "* *\n* *\n* *"
        # dice_1 = BoxText(1, 0, d1, dy=4, dx=4, fmt=color_2, cfmt=color_1)
        # dice_2 = BoxText(1, 5, d2, dy=4, dx=4, fmt=color_2, cfmt=color_1)
        # dice_3 = BoxText(1, 10, d3, dy=4, dx=4, fmt=color_2, cfmt=color_1)
        # dice_4 = BoxText(1, 15, d4, dy=4, dx=4, fmt=color_2, cfmt=color_1)
        # dice_5 = BoxText(1, 20, d5, dy=4, dx=4, fmt=color_2, cfmt=color_1)
        # dice_6 = BoxText(1, 25, d6, dy=4, dx=4, fmt=color_2, cfmt=color_1)
        # self.add_object(dice_1)
        # self.add_object(dice_2)
        # self.add_object(dice_3)
        # self.add_object(dice_4)
        # self.add_object(dice_5)
        # self.add_object(dice_6)
        # lista_1 = [0, 0, 0, 1, 1, 1, 2, 2, 2, 1, 1, 0, 0, -1, -1, -2, -2, -1, -1, 0]
        lista_1 = [
            0,
            0,
            0,
            2,
            2,
            5,
            5,
            0,
            0,
            -2,
            -2,
            -5,
            -5,
            0,
            0,
            1,
            2,
            3,
            4,
            0,
            1,
            2,
            3,
            2,
            1,
            0,
            9,
            0,
            0,
            -5,
            -2,
            0,
            1,
            9,
            0,
        ]
        # self.add_object(String(21, 10, "".join([number(x)[0] for x in lista_1])))
        # self.add_object(String(22, 10, "".join([number(x)[1] for x in lista_1])))
        # self.add_object(HPath(20, 10, lista_1, color_1))
        # self.add_object(HPathCover(18, 10, lista_1, color_1))
        # self.add_object(HorizontalPath(20, 10, 5, lista_1, color_1))
        # for i, v in enumerate(lista_1):
        #     self.add_object(String(19 - v, 10 + i, str(abs(v)), color_2))

        # self.add_object(VPath(2, 10, lista_1, color_1))
        # self.add_object(VPathCover(2, 12, lista_1, color_1))
        self.add_object(VerticalPath(2, 10, 5, lista_1, color_1))
        for i, v in enumerate(lista_1):
            self.add_object(String(2 + i, 11 + v, str(abs(v)), color_2))

        # y: int = 20
        # x: int = 1
        # dy: int = 5
        # self.add_object(Path(y, x, dy, course[:53], color_1))
        # self.add_object(HPath(40, x, course[:53], color_1))

        # self.add_object(String(35, 1, "".join([number(x)[0] for x in course[:53]])))
        # self.add_object(String(36, 1, "".join([number(x)[1] for x in course[:53]])))
        # mobile = "A"
        # self.add_object(
        #     TimerText(24, 1, mobile, self.new_timer(50), updater(course, 24, 1, 52))
        # )
        # self.add_object(
        #     TimerText(21, 1, mobile, self.new_timer(50), updater(course, 21, 1, 52))
        # )

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
            (curses.COLOR_RED, curses.COLOR_BLUE),
            (curses.COLOR_BLACK, curses.COLOR_WHITE),
        ]
    )
    h.add_scene(board_scene)
    h.run()
