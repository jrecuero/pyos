from typing import List, Any

# from ._loggar import log
from ._event import Event, Timer, EventTimer
from ._nobject import NObject


def update(f):
    """update method decorates any scene update method, calling any event
    updates present in the scene.
    """

    def _update(self: "Scene", *events: Event) -> List[Event]:
        if self.enable:
            new_events = list(events)
            for t in self.timers:
                if t.inc():
                    new_events.append(EventTimer(t))
            new_events.extend(self.update_objects(*new_events))
            result = f(self, *new_events)
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
            new_events = self.render_objects(screen)
            result = f(self, screen)
            if result is not None:
                new_events.extend(result)
            return new_events
        return []

    return _render


class Scene:
    """Scene class identifies any scene.
    """

    def __init__(self, name: str = ""):
        self.name: str = name
        self.nobjects: List[NObject] = []
        self.enable: bool = True
        self.visible: bool = True
        self.timers: List[Timer] = []
        self.capture_inputs: List[NObject] = []

    def activate(self):
        """activate sets the scene to be enabled and visible.
        """
        self.enable = True
        self.visible = True

    def deactivate(self):
        """deactivate sets the scene to be disabled and not visible.
        """
        self.enable = False
        self.visible = False

    def setup(self):
        """setup abstract method allows to setup the scene.
        """
        pass

    def update_objects(self, *events: Event) -> List[Event]:
        """update_objects updates all nobjects in a scene.
        """
        new_events: List[Event] = []
        if len(getattr(self, "capture_inputs", [])):
            new_events.extend(self.capture_inputs[-1].update(*events))
        else:
            for obj in self.nobjects:
                new_events.extend(obj.update(*events))
        return new_events

    def render_objects(self, screen: Any) -> List[Event]:
        """render_objects renders all nobjects in a scene.
        """
        events: List[Event] = []
        for obj in self.nobjects:
            events.extend(obj.render(screen))
        return events

    @update
    def update(self, *events: Event) -> List[Event]:
        """update calls all events updates methods a return a list with new
        events to be added to the scene.
        """
        return list(events)

    @render
    def render(self, screen: Any) -> List[Event]:
        """render calls all events renders methods and return a list with new
        events to be added to the scene.
        """
        return []

    def add_object(self, obj: NObject) -> bool:
        """add_object adds a new nobject to the scene.
        """
        self.nobjects.append(obj)
        if getattr(obj, "capture_input", None):
            self.capture_inputs.append(obj)
        return True

    def del_object(self, obj: NObject) -> bool:
        """del_object deletes an nobject from the scene.
        """
        self.nobjects.remove(obj)
        if getattr(obj, "capture_input", None):
            self.capture_inputs.remove(obj)
        return True

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
