from typing import Optional, Any, List, Dict

# from collections import OrderedDict
import curses
from ._event import Event, EventInput, EventSelected, Timer, EVT

from ._loggar import log


c_marked = curses.A_BOLD | curses.A_UNDERLINE


def pinput(f):
    """pinput method decorates any nobject process input method,
    calling the process input method only if the nobject is enabled.
    """

    def _pinput(self: "NObject", screen: Any, keys: List[int]) -> List[Event]:
        if self.enable:
            result = f(self, screen, keys)
            if result is not None:
                return result
        return []

    return _pinput


def update(f):
    """update method decorates any nobject update method, calling the update
    method only if the nobject is enabled.
    """

    def _update(self: "NObject", *events: Event) -> List[Event]:
        if self.enable:
            result = f(self, *events)
            if result is not None:
                return result
        return []

    return _update


def render(f):
    """render method decorates any nobject render method. calling the render
    method only if the nobject is visible.
    """

    def _render(self: "NObject", screen: Any) -> List[Event]:
        if self.visible:
            result = f(self, screen)
            if result is not None:
                return result
        return []

    return _render


def draw_box(screen: Any, y: int, x: int, dy: int, dx: int):
    for _x in range(1, dx):
        screen.addch(y, x + _x, chr(9473))
    for _x in range(1, dx):
        screen.addch(y + dy, x + _x, chr(9473))
    for _y in range(1, dy):
        screen.addch(y + _y, x, chr(9475))
    for _y in range(1, dy):
        screen.addch(y + _y, x + dx - 1, chr(9475))
    screen.addch(y, x, chr(9487))
    screen.addch(y + dy, x, chr(9495))
    screen.addch(y, x + dx - 1, chr(9491))
    screen.addch(y + dy, x + dx - 1, chr(9499))


class NObject:
    """NObject class represents any object to be rendered.
    """

    def __init__(self, y: int, x: int, height: int, width: int):
        self.y: int = y
        self.x: int = x
        self.dy: int = height
        self.dx: int = width
        self.enable: bool = True
        self.visible: bool = True
        self.text_data: str = ""

    def activate(self):
        """activate sets the nobject as enabled and visible.
        """
        self.enable = True
        self.visible = True

    def deactivate(self):
        """deactivate sets the nobject as disabled and not visible.
        """
        self.enable = False
        self.visible = False

    @pinput
    def pinput(self, screen, keys) -> List[Event]:
        """pinput abstact method allows to process input for  nobject.
        """
        return []

    @update
    def update(self, *events: Event) -> List[Event]:
        """update abstract method allows to update the nobject.
        """
        return []

    @render
    def render(self, screen) -> List[Event]:
        """render abstact method allows to render the nobject.
        """
        return []

    def set_cursor(self) -> Optional[List[int]]:
        """set_cursor returns the position the cursor has to be set
        for the given object.
        """
        return None


class Char(NObject):
    """Char class identifies a character nobject.
    """

    def __init__(self, y: int, x: int, text_data: str):
        super(Char, self).__init__(y, x, 1, 1)
        self.text_data = text_data

    @render
    def render(self, screen) -> List[Event]:
        """render renders an string nobject.
        """
        screen.addch(self.y, self.x, self.text_data)
        return []


class XChar(Char):
    """XChar class identifies a formatted character nobject.
    """

    def __init__(self, y: int, x: int, text_data: str, fmt: Optional[Any] = None):
        super(XChar, self).__init__(y, x, text_data)
        self.fmt: Any = fmt if fmt is not None else curses.A_NORMAL

    @render
    def render(self, screen) -> List[Event]:
        """render renders an string nobject.
        """
        screen.addstr(self.y, self.x, self.text_data, self.fmt)
        return []


class String(NObject):
    """String class identifies an string nobject.
    """

    def __init__(self, y: int, x: int, text_data: str):
        super(String, self).__init__(y, x, 1, len(text_data))
        self.text_data = text_data

    @render
    def render(self, screen) -> List[Event]:
        """render renders an string nobject.
        """
        screen.addnstr(self.y, self.x, self.text_data, len(self.text_data))
        return []


class XString(String):
    """XString class identifies a formatted string nobject.
    """

    def __init__(self, y: int, x: int, text_data: str, fmt: Optional[Any] = None):
        super(XString, self).__init__(y, x, text_data)
        self.fmt: Any = fmt if fmt is not None else curses.A_NORMAL

    @render
    def render(self, screen) -> List[Event]:
        """render renders an string nobject.
        """
        screen.addstr(self.y, self.x, self.text_data, self.fmt)
        return []


class Formatted(NObject):
    """Formatted class identifies a formatted nobject.
    """

    def __init__(self, y: int, x: int, data: List[List[Any]]):
        super(Formatted, self).__init__(y, x, 1, -1)
        self.data = data

    @render
    def render(self, screen) -> List[Event]:
        """render renders an string nobject.
        """
        x = self.x
        for entry in self.data:
            st, fmt = entry if len(entry) == 2 else (entry[0], curses.A_NORMAL)
            screen.addstr(self.y, x, st, fmt)
            x += len(st)
        return []


class Block(NObject):
    """Block class identifies a block of strings nobject.
    """

    def __init__(self, y: int, x: int, text_data: str):
        super(Block, self).__init__(y, x, 0, 0)
        self.text_data = text_data

    @render
    def render(self, screen) -> List[Event]:
        """render renders a block of strings nobject.
        """
        tokens = self.text_data.split("\n")
        for y, tok in enumerate(tokens):
            screen.addnstr(self.y + y, self.x, tok, len(tok))
        return []


class Box(NObject):
    """Box class identifies a bordered box nobject.
    """

    @render
    def render(self, screen) -> List[Event]:
        """render renders a bordered box nobject.
        """
        draw_box(screen, self.y, self.x, self.dy, self.dx)
        return []


class BoxGrid(NObject):
    """BoxGrid identifies a grid of bordered objects.
    """

    def __init__(self, y: int, x: int, dy: int, dx: int, ynbr: int, xnbr: int):
        super(BoxGrid, self).__init__(y, x, dy, dx)
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
                draw_box(screen, y, x, self.dy, self.dx)
                x += self.dx + 1
            x = self.x
            y += self.dy + 1


class BoxText(NObject):
    """BoxText class identifies a bordered box containing a block of strings
    nobject.
    """

    def __init__(self, y: int, x: int, text_data: str, dy: int = -1, dx: int = -1):
        super(BoxText, self).__init__(y, x, dy, dx)
        self.text_data: str = text_data
        tokens = self.text_data.split("\n")
        if self.dy == -1:
            self.dy = len(tokens) + 1
        if self.dx == -1:
            for t in tokens:
                if len(t) > self.dx:
                    self.dx = len(t)
            self.dx += 2

    @render
    def render(self, screen) -> List[Event]:
        """render renders a bordered box containing a block of strings
        nobject.
        """
        for x in range(1, self.dx):
            screen.addch(self.y, self.x + x, chr(9473))
        for x in range(1, self.dx):
            screen.addch(self.y + self.dy, self.x + x, chr(9473))
        for y in range(1, self.dy):
            screen.addch(self.y + y, self.x, chr(9475))
        for y in range(1, self.dy):
            screen.addch(self.y + y, self.x + self.dx - 1, chr(9475))
        screen.addch(self.y, self.x, chr(9487))
        screen.addch(self.y + self.dy, self.x, chr(9495))
        screen.addch(self.y, self.x + self.dx - 1, chr(9491))
        screen.addch(self.y + self.dy, self.x + self.dx - 1, chr(9499))
        tokens = self.text_data.split("\n")
        for y, tok in enumerate(tokens):
            screen.addnstr(self.y + 1 + y, self.x + 1, tok, len(tok))
        return []


class FlashText(String):
    """FlasText class identifies a flashing block of strings nobject.
    """

    def __init__(self, y: int, x: int, msg: str, t: Timer, on: int = 1, off: int = 1):
        super(FlashText, self).__init__(y, x, msg)
        self.__timer = t
        self.__shadow = msg
        self.__on = on
        self.__on_counter = 0
        self.__off = off
        self.__off_counter = 0

    @update
    def update(self, *events: Event) -> List[Event]:
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


class TimeUpdater(String):
    """TimeUpdater class identifies a timer nobject.
    """

    def __init__(self, y: int, x: int, msg: str, t: Timer, caller: Any):
        super(TimeUpdater, self).__init__(y, x, msg)
        self.__timer = t
        self.__caller = caller

    @update
    def update(self, *events: Event) -> List[Event]:
        """update updates a timer nobject.
        """
        for event in events:
            if event.evt == EVT.ENG.TIMER:
                if event.get_timer() == self.__timer:
                    self.text_data = self.__caller(self.text_data)
        return []


class Gauge(String):
    """Gauge class identifies a gauge that grows with time.
    """

    def __init__(
        self, y: int, x: int, dy: int, dx: int, t: Timer, total: int, sections: int
    ):
        super(Gauge, self).__init__(y, x, "[{}]".format(" " * sections))
        self.timer: Timer = t
        self.total: int = total
        self.total_sections: int = sections
        self.counter_per_section: int = self.total / self.total_sections
        self.counter: int = 0
        self.sections: int = 0
        self.active: bool = True

    @update
    def update(self, *events: Event) -> List[Event]:
        """update updates a timer nobject.
        """
        for event in events:
            if event.evt == EVT.ENG.TIMER:
                if self.active and event.get_timer() == self.timer:
                    self.counter += 1
                    self.sections = int(self.counter / self.counter_per_section)
                    self.text_data = "[{}{}]".format(
                        chr(9608) * self.sections,
                        " " * (self.total_sections - self.sections),
                    )
                    log.Gauge(
                        "counter: {} sections: {} [{}]".format(
                            self.counter, self.sections, self.text_data
                        )
                    ).call()
                    if self.counter == self.total:
                        self.active = False


class Spinner(String):
    """Spinner class identifies a spinner that changes with left and right
    clicks.
    """

    def __init__(
        self, y: int, x: int, mini: int, maxi: int, defaulti: int, delta: int = 1
    ):
        super(Spinner, self).__init__(
            y, x, "{}{}{}".format(chr(9664), defaulti, chr(9654))
        )
        self.min: int = mini
        self.max: int = maxi
        self.default: int = defaulti
        self.value: int = self.default
        self.delta: int = delta
        self.capture_input: bool = True

    @pinput
    def pinput(self, screen: Any, keys: List) -> List[Event]:
        if self.capture_input and len(keys):
            key = keys.pop()
            if curses.KEY_LEFT == key:
                self.value = (self.value - 1) if self.value > self.min else self.value
                self.text_data = "{}{}{}".format(chr(9664), self.value, chr(9654))
            elif curses.KEY_RIGHT == key:
                self.value = (self.value + 1) if self.value < self.max else self.value
                self.text_data = "{}{}{}".format(chr(9664), self.value, chr(9654))
            elif "\n" == chr(key):
                self.capture_input = False
                self.text_data = "[{}]".format(self.value)
        return []


class Caller(NObject):
    """Caller class identifies a callback nobject.
    """

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


class Input(NObject):
    """Input class identifies an input string nobject.
    """

    def __init__(self, y: int, x: int, text_data: str, text_output: List[str]):
        super(Input, self).__init__(y, x, 1, len(text_data))
        self.text_data: str = text_data
        self.input_str: str = ""
        self.text_output: List[str] = text_output
        self.capture_input = True

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


class Selector(NObject):
    """Selector class identifies a list of tokens that are highlighted and
    can be selected using cursor movement.
    """

    def __init__(
        self,
        y: int,
        x: int,
        tokens: List[str],
        selected: int = 0,
        dy: int = -1,
        dx: int = -1,
        horizontal: bool = True,
    ):
        dy = 1 if dy == -1 else dy
        dx = sum([len(t) for t in tokens]) if dx == -1 else dx
        super(Selector, self).__init__(y, x, dy, dx)
        self.tokens: List[str] = tokens
        self.capture_input = True
        self.selected: int = selected
        self.horizontal: bool = horizontal

    @pinput
    def pinput(self, screen, keys) -> List[Event]:
        if self.capture_input and len(keys):
            key = keys.pop()
            if curses.KEY_LEFT == key and self.horizontal:
                selected = self.selected - 1
            elif curses.KEY_RIGHT == key and self.horizontal:
                selected = self.selected + 1
            if curses.KEY_UP == key and not self.horizontal:
                selected = self.selected - 1
            elif curses.KEY_DOWN == key and not self.horizontal:
                selected = self.selected + 1
            elif "\n" == chr(key):
                self.capture_input = False
                return [EventSelected(self.selected, self.tokens[self.selected])]
            if 0 <= selected < len(self.tokens):
                self.selected = selected
        return []

    @update
    def update(self, *events: Event) -> List[Event]:
        """update updates a selector nobject.
        """
        return []

    @render
    def render(self, screen) -> List[Event]:
        """render renders an string nobject.
        """
        ypos, xpos = self.y, self.x
        for index, token in enumerate(self.tokens):
            screen.addstr(
                ypos,
                xpos,
                token,
                curses.A_REVERSE if self.selected == index else len(token),
            )
            if self.horizontal:
                xpos += len(token) + 1
            else:
                ypos += 1
        return []


class ScrollSelector(Selector):
    """ScrollSelector class identifies a list of tokens that are expanded
    to be selected.
    """

    def __init__(
        self,
        y: int,
        x: int,
        tokens: List[str],
        selected: int = 0,
        dy: int = -1,
        dx: int = -1,
    ):
        super(ScrollSelector, self).__init__(
            y, x, tokens, selected=selected, dy=dy, dx=dx, horizontal=False
        )
        self.expanded: bool = False
        self.box_height: int = len(self.tokens) + 1
        self.box_width: int = 0
        for t in self.tokens:
            if len(t) > self.box_width:
                self.box_width = len(t)
        self.box_width += 2
        # self.popup_screen: Any = None

    @pinput
    def pinput(self, screen, keys) -> List[Event]:
        selected = self.selected
        if self.capture_input and len(keys):
            key = keys.pop()
            if self.expanded and curses.KEY_UP == key:
                selected = self.selected - 1
            elif self.expanded and curses.KEY_DOWN == key:
                selected = self.selected + 1
            elif self.expanded and "\n" == chr(key):
                self.expanded = False
                self.capture_input = False
                return [EventSelected(self.selected, self.tokens[self.selected])]
            elif not self.expanded and "\n" == chr(key):
                selected = self.selected
                self.expanded = True
            if 0 <= selected < len(self.tokens):
                self.selected = selected
        return []

    @render
    def render(self, screen) -> List[Event]:
        """render renders an string nobject.
        """
        if self.expanded:
            draw_box(screen, self.y, self.x, self.box_height, self.box_width)
            ypos, xpos = self.y + 1, self.x + 1
            screen.addstr(ypos, xpos, " " * len(self.tokens[self.selected]))
            for index, token in enumerate(self.tokens):
                screen.addstr(
                    ypos,
                    xpos,
                    token,
                    curses.A_REVERSE if self.selected == index else len(token),
                )
                ypos += 1
        else:
            screen.addstr(self.y, self.x, self.tokens[self.selected], curses.A_REVERSE)
        return []


class Menu(NObject):
    """Menu class identifies a menu object.
    """

    def __init__(self, y: int, x: int, tokens: List, dy: int = 2, dx: int = -1):
        _dx: int = dx if dx != -1 else sum([len(t[0]) for t in tokens]) + 1
        super(Menu, self).__init__(y, x, dy, _dx)
        self.tokens: List = tokens
        self.menu_items: List = self.tokens
        self.selected_items: List = [
            {"pos": [self.y, self.x, self.dy, self.dx], "items": list(self.menu_items)}
        ]
        self.menu_pos: List = []
        self.shortcuts: List[str] = []
        self.capture_input: bool = True

    def _draw_menu_items(self, screen: Any, menu_items: Dict, top: bool):
        y, x, dy, dx = menu_items["pos"]
        items = menu_items["items"]
        draw_box(screen, y, x, dy, dx)
        y, x = y + 1, x + 1
        dx = max([len(t[0]) for t in items])
        self.shortcuts = []
        self.menu_pos = []
        for t, v in [x for x in items]:
            mark: int = t.find("^")
            dy = len(v) + 1 if v is not None else -1
            self.menu_pos.append([y + 1, x, dy, dx])
            screen.addstr(y, x, t[:mark])
            screen.addstr(y, x + mark, t[mark + 1], c_marked)
            screen.addstr(y, x + mark + 1, t[mark + 2 :])
            if top:
                x += len(t)
            else:
                y += 1
            self.shortcuts.append(t[t.find("^") + 1].upper())

    def activate(self):
        """activate sets the nobject as enabled and visible.
        """
        super(Menu, self).activate()
        self.capture_input = True

    @pinput
    def pinput(self, screen, keys) -> List[Event]:
        if self.capture_input and len(keys):
            key = keys.pop()
            log.Menu("Key {}".format(key)).call()
            if key == 27:  # escape
                log.Menu("Key ESCAPE").call()
            else:
                key = chr(key).upper()
            if key in self.shortcuts:
                index: int = self.shortcuts.index(key)
                selected_item = self.menu_items[index][1]
                if selected_item is None:
                    self.menu_items = self.tokens
                    self.selected_items = self.selected_items[:1]
                    self.capture_input = False
                else:
                    self.selected_items.append(
                        {"pos": self.menu_pos[index], "items": list(selected_item)}
                    )
                    self.menu_items = list(selected_item)
                    self.dx = sum([len(t[0]) for t in self.menu_items]) + 1
        return []

    @render
    def render(self, screen) -> List[Event]:
        for index, item in enumerate(self.selected_items):
            self._draw_menu_items(screen, item, index == 0)
        return []
