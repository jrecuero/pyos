from typing import List, Any

# from ._loggar import log
from ._event import Event, Timer, EventTimer
from ._nobject import NObject, Panel
from ._dplug import get_plugin


def pinput(f):
    """pinput method decorates any scene process input  method, calling any event
    to process input.
    """

    def _pinput(self: "Scene", screen: Any, keys: List[int]) -> List[Event]:
        if self.visible:
            screen = self.screen_to_use(screen)
            new_events = self.pinput_objects(screen, keys)
            result = f(self, screen, keys)
            if result is not None:
                new_events.extend(result)
            return new_events
        return []

    return _pinput


def update(f):
    """update method decorates any scene update method, calling any event
    updates present in the scene.
    """

    def _update(self: "Scene", screen: Any, *events: Event) -> List[Event]:
        if self.enable:
            screen = self.screen_to_use(screen)
            new_events = list(events)
            new_events.extend(self.update_timers(screen))
            new_events.extend(self.update_objects(screen, *new_events))
            result = f(self, screen, *new_events)
            if result is not None:
                return result
        return []

    return _update


def render(f):
    """render method decorates any scene render method, calling any event
    renders present in the scene.
    """

    def _render(self: "Scene", screen: Any) -> List[Event]:
        if self.visible:
            screen = self.screen_to_use(screen)
            new_events = self.render_objects(screen)
            self.set_cursor(screen)
            result = f(self, screen)
            if result is not None:
                new_events.extend(result)
            return new_events
        return []

    return _render


class Scene(object):
    """Scene class identifies any scene.
    """

    __slots__ = ["name", "nobjects", "enable", "visable", "timers", "boarder", "screen"]

    def __init__(self, name: str = ""):
        self.name: str = name
        self.nobjects: List[NObject] = []
        self.enable: bool = True
        self.visible: bool = True
        self.timers: List[Timer] = []
        self.border: bool = True
        self.screen: Any = None

    def __get_input(self, screen: Any) -> int:
        """__get_input is an internal method that loops for any user input key
        being entered.
        """
        return get_plugin().get_ch(screen)

    def get_input(self, screen: Any) -> int:
        screen = self.screen_to_use(screen)
        return self.__get_input(screen)

    def activate(self):
        """activate sets the scene to be enabled and visible.
        """
        self.enable = True
        self.visible = True
        for obj in self.nobjects:
            obj.activate()

    def deactivate(self):
        """deactivate sets the scene to be disabled and not visible.
        """
        self.enable = False
        self.visible = False
        for obj in self.nobjects:
            obj.deactivate()

    def screen_to_use(self, screen: Any) -> Any:
        """screen_to_use returns the screen to be used by the scene.
        """
        return self.screen if self.screen else screen

    def setup(self, screen: Any):
        """setup abstract method allows to setup the scene.
        """
        pass

    def pinput_objects(self, screen: Any, keys: List[Event]) -> List[Event]:
        """pinput_objects process input for all nobjects in a scene.
        """
        events: List[Event] = []
        for obj in self.nobjects:
            events.extend(obj.pinput(screen, keys))
        return events

    def update_timers(self, screen: Any):
        """update_timers proceeds to update all scene timers.
        """
        events = []
        for t in self.timers:
            if t.inc():
                events.append(EventTimer(t))
        return events

    def update_objects(self, screen: Any, *events: Event) -> List[Event]:
        """update_objects updates all nobjects in a scene.
        """
        new_events: List[Event] = []
        for obj in self.nobjects:
            new_events.extend(obj.update(screen, *events))
        return new_events

    def render_objects(self, screen: Any) -> List[Event]:
        """render_objects renders all nobjects in a scene.
        """
        if self.border:
            get_plugin().border(screen, 0)
        events: List[Event] = []
        for obj in self.nobjects:
            events.extend(obj.render(screen))
        return events

    def set_cursor(self, screen: Any):
        """set_cursor sets the cursor position to the object that requires
        user input.
        """
        for obj in self.nobjects:
            cursor_pos = obj.set_cursor()
            if cursor_pos:
                get_plugin().cursor(True)
                get_plugin().draw_sprite(
                    screen, "", cursor_pos[0], cursor_pos[1], "", None, None
                )
                return
        get_plugin().cursor(False)

    def colors(self, color_pairs):
        """colors setups for using given list of color pairs.
        """
        get_plugin().colors(color_pairs)

    def screen_erase(self, screen: Any):
        """screen_erase proceeds to erase scene screen.
        """
        screen = self.screen_to_use(screen)
        get_plugin().erase(screen)

    @pinput
    def pinput(self, screen: Any, keys: List[int]) -> List[int]:
        return []

    @update
    def update(self, screen: Any, *events: Event) -> List[Event]:
        """update calls all events updates methods a return a list with new
        events to be added to the scene.
        """
        return list(events)

    @render
    def render(self, screen: Any) -> List[Event]:
        """render calls all events renders methods and return a list with new
        events to be added to the scene.
        """
        get_plugin().refresh_screen(self.screen_to_use(screen))
        return []

    def add_object(self, obj: NObject) -> bool:
        """add_object adds a new nobject to the scene.
        """
        self.nobjects.append(obj)
        return True

    def del_object(self, obj: NObject) -> bool:
        """del_object deletes an nobject from the scene.
        """
        self.nobjects.remove(obj)
        return True

    def add_to_panel(self, panel: Panel, obj: NObject) -> bool:
        if panel.add(obj):
            return self.add_object(obj)
        return False

    def remove_from_panel(self, panel: Panel, obj: NObject) -> bool:
        if panel.remove(obj):
            return self.del_object(obj)
        return False

    def new_timer(self, timeout: int, enable: bool = True) -> Timer:
        """new_timer creates and adds a timer event to the scene.
        """
        t = Timer(timeout, enable)
        return self.add_timer(t)

    def add_timer(self, t: Timer) -> Timer:
        """add_timer adds a timer event to the scene.
        """
        self.timers.append(t)
        return t

    def del_timer(self, t: Timer) -> None:
        """del_timer deletes a timer event to the scene.
        """
        self.timers.remove(t)
