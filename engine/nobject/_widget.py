from typing import List, Any, Dict
import curses
from .._nobject import draw_box, NObject, pinput, update, render
from .._event import Event, EventSelected, Timer, EVT
from .._loggar import log
from ._string import String, Capture


c_marked = curses.A_BOLD | curses.A_UNDERLINE


class Gauge(String):
    """Gauge class identifies a gauge that grows with time.
    """

    __slots__ = [
        "timer",
        "total",
        "tatal_sections",
        "counter_per_section",
        "counter",
        "sections",
        "active",
    ]

    def __init__(
        self,
        y: int,
        x: int,
        dy: int,
        dx: int,
        t: Timer,
        total: int,
        sections: int,
        fmt=curses.A_NORMAL,
    ):
        super(Gauge, self).__init__(y, x, "[{}]".format(" " * sections), fmt)
        self.timer: Timer = t
        self.total: int = total
        self.total_sections: int = sections
        self.counter_per_section: int = self.total / self.total_sections
        self.counter: int = 0
        self.sections: int = 0
        self.active: bool = True

    def _update(self, inc: int):
        self.counter += inc
        self.sections = int(self.counter / self.counter_per_section)
        self.text_data = "[{}{}]".format(
            chr(9608) * self.sections, " " * (self.total_sections - self.sections)
        )
        if self.counter == self.total:
            self.active = False

    def call(self, **kwargs):
        inc = kwargs.get("inc", 0)
        self._update(inc)

    @update
    def update(self, screen: Any, *events: Event) -> List[Event]:
        """update updates a timer nobject.
        """
        for event in events:
            if event.evt == EVT.ENG.TIMER:
                if self.active and event.get_timer() == self.timer:
                    self._update(1)


class Spinner(String, Capture):
    """Spinner class identifies a spinner that changes with left and right
    clicks.
    """

    __slots__ = ["min", "max", "default", "value", "delta"]

    def __init__(
        self,
        y: int,
        x: int,
        mini: int,
        maxi: int,
        defaulti: int,
        delta: int = 1,
        fmt=curses.A_NORMAL,
    ):
        self.pattern = "{0}{1}{2}"
        String.__init__(
            self,
            y,
            x,
            ("{}".format(self.pattern)).format(chr(9664), defaulti, chr(9654)),
            fmt,
        )
        Capture.__init__(self)
        self.min: int = mini
        self.max: int = maxi
        self.default: int = defaulti
        self.value: int = self.default
        self.delta: int = delta

    def _set(self, value: int):
        if self.min < value < self.max:
            self.value = value

    def _update(self, inc: int):
        value = self.value
        self.value = self.value + inc
        if (self.value < self.min) or (self.value > self.max):
            self.value = value

    def call(self, **kwargs):
        if kwargs.get("set", False):
            self._set(kwargs.get("value", self.value))
        elif kwargs.get("update", False):
            self._update(kwargs.get("inc", 0))
        self.text_data = ("{}".format(self.pattern)).format(
            chr(9664), self.value, chr(9654)
        )

    @pinput
    def pinput(self, screen: Any, keys: List) -> List[Event]:
        if self.capture_input and len(keys):
            key = keys.pop()
            if curses.KEY_LEFT == key:
                self._update(-self.delta)
                # self.value = (
                #     (self.value - self.delta) if self.value > self.min else self.value
                # )
            elif curses.KEY_RIGHT == key:
                self._update(self.delta)
                # self.value = (
                #     (self.value + self.delta) if self.value < self.max else self.value
                # )
            elif "\n" == chr(key):
                self.capture_input = False
                self.pattern = "[{1}]"
        self.text_data = ("{}".format(self.pattern)).format(
            chr(9664), self.value, chr(9654)
        )
        return []


class SpinnerScroll(Spinner):
    """SpinnerScroll class identifies a spinner that changes with left and right
    clicks.
    """

    __slots__ = ["patron", "pattern"]

    def __init__(
        self,
        y: int,
        x: int,
        mini: int,
        maxi: int,
        defaulti: int,
        delta: int = 1,
        fmt=curses.A_NORMAL,
    ):
        super(SpinnerScroll, self).__init__(y, x, mini, maxi, defaulti, delta, fmt)
        self.patron = "{0}{1}{2}"
        self.pattern = "[     {}     ]".format(self.patron)

    @render
    def render(self, screen: Any) -> List[Event]:
        """render renders a callback nobject.
        """
        if self.capture_input:
            gap: int = int((self.value * 10) / (self.max - self.min))
            self.pattern = "[{}{}{}]".format(" " * gap, self.patron, " " * (10 - gap))
        else:
            self.pattern = "[{1}]"
        return super(SpinnerScroll, self).render(screen)


class Selector(NObject, Capture):
    """Selector class identifies a list of tokens that are highlighted and
    can be selected using cursor movement.
    """

    __slots__ = ["tokens", "selected" "horizonta"]

    def __init__(
        self,
        y: int,
        x: int,
        tokens: List[str],
        selected: int = 0,
        dy: int = -1,
        dx: int = -1,
        horizontal: bool = True,
        fmt=curses.A_NORMAL,
    ):
        dy = 1 if dy == -1 else dy
        dx = sum([len(t) for t in tokens]) if dx == -1 else dx
        NObject.__init__(self, y, x, dy, dx, fmt)
        Capture.__init__(self)
        self.tokens: List[str] = tokens
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
    def update(self, screen: Any, *events: Event) -> List[Event]:
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

    __slots__ = ["expanded", "box_height", "box_width"]

    def __init__(
        self,
        y: int,
        x: int,
        tokens: List[str],
        selected: int = 0,
        dy: int = -1,
        dx: int = -1,
        fmt=curses.A_NORMAL,
    ):
        super(ScrollSelector, self).__init__(
            y, x, tokens, selected=selected, dy=dy, dx=dx, horizontal=False, fmt=fmt
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


class Menu(NObject, Capture):
    """Menu class identifies a menu object.
    """

    __slots__ = ["tokens" "menu_items", "selected_items", "menu_pos", "shortcuts"]

    def __init__(
        self,
        y: int,
        x: int,
        tokens: List,
        dy: int = 2,
        dx: int = -1,
        fmt=curses.A_NORMAL,
    ):
        _dx: int = dx if dx != -1 else sum([len(t[0]) for t in tokens]) + 1
        NObject.__init__(self, y, x, dy, _dx, fmt)
        Capture.__init__(self)
        self.tokens: List = tokens
        self.menu_items: List = self.tokens
        self.selected_items: List = [
            {"pos": [self.y, self.x, self.dy, self.dx], "items": list(self.menu_items)}
        ]
        self.menu_pos: List = []
        self.shortcuts: List[str] = []

    def _draw_menu_items(self, screen: Any, menu_items: Dict, top: bool):
        y, x, dy, dx = menu_items["pos"]
        items = menu_items["items"]
        # draw_box(screen, y, x, dy, dx)
        self.box(screen)
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
