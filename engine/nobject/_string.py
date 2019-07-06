from typing import List, Any, Optional
import curses
from .._nobject import draw_box, NObject, pinput, update, render
from .._event import Event, EventInput, Timer, EVT
from .._loggar import log


class TextData(NObject):
    """TextData class identifies all object that have to render some string.
    """

    def __init__(
        self, y: int, x: int, dy: int, dx: int, text_data: str, fmt=curses.A_NORMAL
    ):
        super(TextData, self).__init__(y, x, dy, dx, fmt)
        self.text_data = text_data

    def set_text(self, text_data: str):
        """set_text updates the text to be displayed.
        """
        self.text_data = text_data


class Char(TextData):
    """Char class identifies a formatted character nobject.
    """

    def __init__(self, y: int, x: int, text_data: str, fmt=curses.A_NORMAL):
        super(Char, self).__init__(y, x, 1, 1, text_data, fmt)

    @render
    def render(self, screen) -> List[Event]:
        """render renders an string nobject.
        """
        screen.addstr(self.y, self.x, self.text_data, self.fmt)
        return []


class String(TextData):
    """String class identifies a formatted string nobject.
    """

    def __init__(self, y: int, x: int, text_data: str, fmt=curses.A_NORMAL):
        super(String, self).__init__(y, x, 1, len(text_data), text_data, fmt)

    @render
    def render(self, screen) -> List[Event]:
        """render renders an string nobject.
        """
        screen.addstr(self.y, self.x, self.text_data, self.fmt)
        return []


class Formatted(NObject):
    """Formatted class identifies a formatted nobject.
    """

    __slots__ = ["data"]

    def __init__(self, y: int, x: int, data: List[List[Any]], fmt=curses.A_NORMAL):
        super(Formatted, self).__init__(y, x, 1, -1, fmt)
        self.data = data

    @render
    def render(self, screen) -> List[Event]:
        """render renders an string nobject.
        """
        x = self.x
        for entry in self.data:
            st, fmt = entry if len(entry) == 2 else (entry[0], self.fmt)
            screen.addstr(self.y, x, st, fmt)
            x += len(st)
        return []


class Block(TextData):
    """Block class identifies a block of strings nobject.
    """

    def __init__(self, y: int, x: int, text_data: str, fmt=curses.A_NORMAL):
        super(Block, self).__init__(y, x, 0, 0, text_data, fmt)

    @render
    def render(self, screen) -> List[Event]:
        """render renders a block of strings nobject.
        """
        tokens = self.text_data.split("\n")
        for y, tok in enumerate(tokens):
            screen.addnstr(self.y + y, self.x, tok, len(tok), self.fmt)
        return []


class Box(NObject):
    """Box class identifies a bordered box nobject.
    """

    def __init__(self, y: int, x: int, dy: int, dx: int, fmt=curses.A_NORMAL):
        super(Box, self).__init__(y, x, dy, dx, fmt)

    @render
    def render(self, screen) -> List[Event]:
        """render renders a bordered box nobject.
        """
        self.box(screen, self.fmt)
        return []


class BoxGrid(NObject):
    """BoxGrid identifies a grid of bordered objects.
    """

    __slots__ = ["ynbr", "xnbr"]

    def __init__(
        self,
        y: int,
        x: int,
        dy: int,
        dx: int,
        ynbr: int,
        xnbr: int,
        fmt=curses.A_NORMAL,
    ):
        super(BoxGrid, self).__init__(y, x, dy, dx, fmt)
        self.ynbr: int = ynbr
        self.xnbr: int = xnbr

    @render
    def render(self, screen: Any) -> List[Event]:
        """render renders a bordered box nobject.
        """
        y: int = self.y
        x: int = self.x
        for ynbr in range(1, self.ynbr + 1):
            for xnbr in range(1, self.xnbr + 1):
                draw_box(screen, y, x, self.dy, self.dx, self.fmt)
                x += self.dx + 1
            x = self.x
            y += self.dy + 1


class BoxText(TextData):
    """BoxText class identifies a bordered box containing a block of strings
    nobject.
    """

    __slots__ = ["cfmt"]

    def __init__(
        self,
        y: int,
        x: int,
        text_data: str,
        dy: int = -1,
        dx: int = -1,
        fmt=curses.A_NORMAL,
        cfmt=curses.A_NORMAL,
    ):
        super(BoxText, self).__init__(y, x, dy, dx, text_data, fmt)
        tokens = self.text_data.split("\n")
        if self.dy == -1:
            self.dy = len(tokens) + 1
        if self.dx == -1:
            for t in tokens:
                if len(t) > self.dx:
                    self.dx = len(t)
            self.dx += 2
        self.cfmt = cfmt

    @render
    def render(self, screen) -> List[Event]:
        """render renders a bordered box containing a block of strings
        nobject.
        """
        self.box(screen, self.fmt)
        tokens = self.text_data.split("\n")
        for y, tok in enumerate(tokens):
            screen.addnstr(self.y + 1 + y, self.x + 1, tok, len(tok), self.cfmt)
        return []


class FlashText(String):
    """FlasText class identifies a flashing block of strings nobject.
    """

    __slots__ = [
        "__timer",
        "__shadow",
        "__on",
        "__on_counter",
        "__off",
        "__off_counter",
    ]

    def __init__(
        self,
        y: int,
        x: int,
        msg: str,
        t: Timer,
        on: int = 1,
        off: int = 1,
        fmt=curses.A_NORMAL,
    ):
        super(FlashText, self).__init__(y, x, msg, fmt)
        self.__timer = t
        self.__shadow = msg
        self.__on = on
        self.__on_counter = 0
        self.__off = off
        self.__off_counter = 0

    @update
    def update(self, screen: Any, *events: Event) -> List[Event]:
        """update updates a flashing block of strings nobject.
        """
        for event in events:
            if event.evt == EVT.ENG.TIMER:
                if event.get_timer() == self.__timer:
                    if self.text_data == "":
                        self.__off_counter += 1
                        if self.__off_counter == self.__off:
                            self.__off_counter = 0
                            self.text_data = self.__shadow
                    else:
                        self.__on_counter += 1
                        if self.__on_counter == self.__on:
                            self.__on_counter = 0
                            self.text_data = ""
        return []


class TimerText(String):
    """TimerText class identifies a timer nobject.
    """

    __slots__ = ["__timer", "__calleer"]

    def __init__(
        self, y: int, x: int, msg: str, t: Timer, caller: Any, fmt=curses.A_NORMAL
    ):
        super(TimerText, self).__init__(y, x, msg, fmt)
        self.__timer = t
        self.__caller = caller

    @update
    def update(self, screen: Any, *events: Event) -> List[Event]:
        """update updates a timer nobject.
        """
        for event in events:
            if event.evt == EVT.ENG.TIMER:
                if event.get_timer() == self.__timer:
                    self.y, self.x, self.text_data, self.fmt = self.__caller(
                        self.y, self.x, self.text_data, self.fmt
                    )
        return []


class Caller(NObject):
    """Caller class identifies a callback nobject.
    """

    __slots__ = ["caller"]

    def __init__(self, y: int, x: int, caller: Any):
        super(Caller, self).__init__(y, x, -1, -1)
        self.caller = caller

    @render
    def render(self, screen) -> List[Event]:
        """render renders a callback nobject.
        """
        tokens = self.caller()
        for y, x, tok in tokens:
            for i, t in enumerate(str(tok).split("\n")):
                screen.addnstr(y + i, x, t, len(tok))
        return []


class Capture(object):
    """Capture class identifies any object that has to receive input from the
    user.
    """

    # TODO: To be included in all derived classes.
    # __slots__ = ["capture_input"]

    def __init__(self):
        self.capture_input = True

    def set_capture(self, capture_input: bool = True):
        self.capture_input = capture_input


class Input(TextData, Capture):
    """Input class identifies an input string nobject.
    """

    __slots__ = ["input_str", "text_output", "capture_input"]

    def __init__(
        self,
        y: int,
        x: int,
        text_data: str,
        text_output: List[str],
        fmt=curses.A_NORMAL,
    ):
        TextData.__init__(self, y, x, 1, len(text_data), text_data, fmt)
        Capture.__init__(self)
        self.input_str: str = ""
        self.text_output: List[str] = text_output

    def clear(self):
        self.input_str = ""

    @pinput
    def pinput(self, screen, keys) -> List[Event]:
        if self.capture_input and len(keys):
            key = keys.pop()
            log.Input("Key: {}".format(key)).call()
            if key == 10:  # return carrier
                self.capture_input = False
                self.text_output.append(self.input_str)
                return [EventInput(self.input_str)]
            elif key == 127:  # backspace
                self.input_str = self.input_str[:-1]
            else:
                self.input_str += chr(key)
        return []

    @render
    def render(self, screen) -> List[Event]:
        """render renders an input string nobject.
        """
        screen.addstr(self.y, self.x, self.text_data + self.input_str)
        return []

    def set_cursor(self) -> Optional[List[int]]:
        if self.capture_input:
            return [self.y, self.x + len(self.text_data + self.input_str)]
        return None


class TextInput(TextData, Capture):
    """TextInput class identifies a text input string nobject.
    """

    __slots__ = ["in_cb", "capture_input"]

    def __init__(self, y: int, x: int, text_data: str, in_cb, fmt=curses.A_NORMAL):
        TextData.__init__(self, y, x, 1, len(text_data), text_data, fmt)
        Capture.__init__(self)
        self.text_data: str = text_data
        self.input_str: str = ""
        self.in_cb = in_cb

    def clear(self):
        self.input_str = ""

    @pinput
    def pinput(self, screen, keys) -> List[Event]:
        if self.capture_input and len(keys):
            key = keys.pop()
            if key == 10:  # return carrier
                self.capture_input = False
                self.in_cb(self.input_str)
                return [EventInput(self.input_str)]
            elif key == 127:  # backspace
                self.input_str = self.input_str[:-1]
            else:
                self.input_str += chr(key)
        return []

    @render
    def render(self, screen) -> List[Event]:
        """render renders an input string nobject.
        """
        screen.addstr(self.y, self.x, self.text_data + self.input_str)
        return []

    def set_cursor(self) -> Optional[List[int]]:
        if self.capture_input:
            return [self.y, self.x + len(self.text_data + self.input_str)]
        return None
