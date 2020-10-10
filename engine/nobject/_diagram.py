from typing import List, Any
from .._nobject import NObject, render
from .._event import Event
from .._dplug import get_plugin


class Diagram(NObject):
    """Diagram class identifies any generic diagram to be created.
    """

    __slots__ = [
        "data",
        "title",
        "subtitle",
        "y_title",
        "x_title",
        "y_scale",
        "x_scale",
        "x_width",
        "style",
    ]

    def __init__(self, y: int, x: int, dy: int, dx: int, data: List, **kwargs):
        super(Diagram, self).__init__(
            y, x, dy, dx, kwargs.get("fmt", get_plugin().default_fmt())
        )
        self.data: List = data
        self.title: str = kwargs.get("title", "")
        self.subtitle: str = kwargs.get("subtitle", "")
        self.y_title: str = kwargs.get("y_title", "Y")
        self.x_title: str = kwargs.get("x_title", "X")
        self.y_scale: int = kwargs.get("y_scale", 1)
        self.x_scale: int = kwargs.get("x_scale", 1)
        self.x_width: int = kwargs.get("x_width", 1)
        self.style: str = kwargs.get("style", "bar")


class HistoBar(Diagram):
    """HistoBar class represents an HistoBar diagram.
    """

    def __init__(self, y: int, x: int, dy: int, dx: int, data: List, **kwargs):
        super(HistoBar, self).__init__(y, x, dy, dx, data, **kwargs)

    @render
    def render(self, screen: Any) -> List[Event]:
        self.box(screen)
        y: int = 0
        x: int = 0
        for index, (ypos, xpos) in enumerate(self.data):
            if self.style == "bar":
                x = self.x + xpos + (self.x_width - 1) * index
                for _y in range(ypos):
                    y = self.y + self.dy - _y - 1
                    for _x in range(self.x_width):
                        get_plugin().draw_sprite(
                            screen, chr(9608), y, x + _x, None, 1, self.fmt
                        )
            else:
                x = self.x + xpos
                y = self.y + self.dy - ypos
                char = chr(9608) if self.style == "plot" else self.style
                get_plugin().draw_sprite(screen, char, y, x, None, 1, self.fmt)
        return []


class Histogram(Diagram):
    """Histogram class represents a bars histogram diagram.
    """

    __slots__ = ["bar_titles", "bar_colors"]

    def __init__(self, y: int, x: int, dy: int, dx: int, data: List, **kwargs):
        super(Histogram, self).__init__(y, x, dy, dx, data, **kwargs)
        self.bar_titles: List[str] = kwargs.get("bar_titles", [])
        self.bar_colors: List[Any] = kwargs.get("bar_colors", [])
        if len(self.bar_colors) < len(self.data):
            for _ in range(len(self.bar_colors), len(self.data)):
                self.bar_colors.append(self.fmt)

    def draw_bar(self, screen: Any, y: int, x: int, width: int, char: str, fmt=None):
        fmt = fmt if fmt is not None else get_plugin().default_fmt()
        for _y in range(y):
            __y: int = self.y + self.dy - _y - 1
            for _x in range(width):
                get_plugin().draw_sprite(screen, char, __y, x + _x, None, 1, fmt)

    @render
    def render(self, screen: Any) -> List[Event]:
        self.box(screen)
        for index, y in enumerate(self.data):
            x: int = self.x + self.x_width * (1 + index)
            self.draw_bar(screen, y, x, self.x_width, chr(9608), self.bar_colors[index])
            get_plugin().draw_sprite(
                screen, self.bar_titles[index], self.y + self.dy + 1, x + 1, None, 1
            )
