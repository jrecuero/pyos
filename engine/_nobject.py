from typing import Optional, Any, List

from ._event import Event
from ._dplug import get_plugin


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

    def _update(self: "NObject", screen: Any, *events: Event) -> List[Event]:
        if self.enable:
            result = f(self, screen, *events)
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


def draw_box(screen: Any, y: int, x: int, dy: int, dx: int, fmt):
    get_plugin().draw_rectangle(screen, y, x, dy, dx, fmt)


class NObject(object):
    """NObject class represents any object to be rendered.
    """

    __slots__ = ["y", "x", "dx", "dy", "enable", "visible", "text_data", "fmt"]

    def __init__(self, y: int, x: int, height: int, width: int, fmt=None):
        self.y: int = y
        self.x: int = x
        self.dy: int = height
        self.dx: int = width
        self.enable: bool = True
        self.visible: bool = True
        self.text_data: str = ""
        self.fmt = fmt if fmt is not None else get_plugin().default_fmt()

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

    def call(self, **kwargs):
        """call abstract method that allows to update widget attributes.
        """
        pass

    def box(self, screen: Any, fmt=None):
        fmt = fmt if fmt else self.fmt
        draw_box(screen, self.y, self.x, self.dy, self.dx, fmt)

    @pinput
    def pinput(self, screen, keys) -> List[Event]:
        """pinput abstact method allows to process input for  nobject.
        """
        return []

    @update
    def update(self, screen: Any, *events: Event) -> List[Event]:
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


class Panel(NObject):
    """Panel class identifies all object grouped in a panel.
    """

    __slots__ = ["children", "_render_box"]

    def __init__(self, y: int, x: int, dy: int, dx: int, fmt):
        super(Panel, self).__init__(y, x, dy, dx, fmt)
        self.children: List[NObject] = []
        self._render_box: bool = True

    def add(self, obj: NObject) -> bool:
        obj.y += self.y
        obj.x += self.x
        self.children.append(obj)
        return True

    def remove(self, obj: NObject) -> bool:
        self.children.remove(obj)
        return True

    def clear(self) -> bool:
        self.children = []
        return True

    def render_box(self, flag: bool):
        self._render_box = flag

    @render
    def render(self, screen) -> List[Event]:
        if self._render_box:
            self.box(screen)
        return []
