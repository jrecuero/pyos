from typing import Any, List, Optional
import curses
import time
from ._event import EVT, Timer, Event, EventKey, EventTimer
from ._scene import Scene


class Handler:
    """Handler class handles a full scene scenario.
    """

    def __init__(self, tick: float = 0.01):
        self.screen: Any = None
        self.scenes: List[Scene] = []
        self.iscene: int = -1
        self.key: int = -1
        self.tick: float = tick
        self.timers: List[Timer] = []
        self.render_events: List[Event] = []

    def run(self):
        """run runs all scenes.
        """
        curses.wrapper(self.__main)

    def __loop(self) -> int:
        """__loop is an internal method that loops for any user input key
        being entered.
        """
        time.sleep(self.tick)
        self.key = self.screen.getch()
        curses.flushinp()
        return self.key

    def __main(self, screen: Any):
        """__main is an internal method that implements the handler main
        loop functionality.
        """
        self.screen = screen
        self.screen.nodelay(True)
        curses.start_color()
        curses.curs_set(False)
        while True:
            self.screen.erase()
            self.update()
            self.render()
            self.__loop()

    def new_timer(self, timeout: int, enable: bool = True) -> Timer:
        """new_timer creates and adds a timer event to the handler.
        """
        t = Timer(timeout, enable)
        return self.add_timer(t)

    def add_timer(self, t: Timer) -> Timer:
        """add_timer adds a timer event to the handler.
        """
        self.timers.append(t)
        return t

    def del_timer(self, t: Timer) -> None:
        """del_timer deletes a timer event from the handler.
        """
        self.timers.remove(t)

    def new_scene(self) -> Scene:
        """new_scene creates and add a new scene to the handler.
        """
        scn = Scene()
        return self.add_scene(scn)

    def add_scene(self, scn: Scene) -> Scene:
        """add_scene adds a scene to the handler.
        """
        scn.setup()
        self.scenes.append(scn)
        if self.iscene == -1:
            self.iscene = len(self.scenes) - 1
        return scn

    def del_scene(self, scn: Scene) -> None:
        """del_scene deletes an scene from the handler.
        """
        self.scenes.remove(scn)

    def get_scene(self) -> Optional[Scene]:
        """get_scene gets the current scene.
        """
        if self.iscene != -1:
            return self.scenes[self.iscene]
        return None

    def _move_to_scene(self, iscene: int) -> int:
        """_move_to_scene moves the handler to the given scene.
        """
        if self.iscene != -1:
            old_scene = self.scenes[self.iscene]
            old_scene.deactivate()
        self.iscene = iscene
        new_scene = self.scenes[self.iscene]
        new_scene.activate()
        return self.iscene

    def set_iscene(self, iscene: int = 0) -> Optional[Scene]:
        """set_iscene sets the handler scene to the given index scene.
        """
        self.iscene = iscene
        return self.scenes[self.iscene]

    def set_scene(self, scn: Scene) -> Optional[Scene]:
        """set_scene sets the handler to the given scene.
        """
        for i, s in enumerate(self.scenes):
            if s == scn:
                self._move_to_scene(i)
                return s
        return None

    def next_scene(self) -> int:
        """next_scene moves the handler to the next scene.
        """
        return self._move_to_scene(self.iscene + 1)

    def prev_scene(self) -> int:
        """next_scene moves the handler to the previous scene.
        """
        return self._move_to_scene(self.iscene - 1)

    def set_scene_first(self) -> Optional[Scene]:
        """set_scene_first sets the handler scene to be the first.
        """
        return self.set_iscene()

    def set_scene_last(self) -> Optional[Scene]:
        """set_scene_last sets the handler scene to be the last.
        """
        last = len(self.scenes) - 1
        return self.set_iscene(last)

    def setup(self):
        """setup is the abtract method that setups the handler.
        """
        pass

    def update(self):
        """update updates scenes, events and nobject in the handler.
        """
        if self.iscene != -1:
            events = []
            events.extend(self.render_events)
            if self.key != -1:
                events.append(EventKey(self.key))
                self.key = -1
            for t in self.timers:
                if t.inc():
                    events.append(EventTimer(t))
            update_events = self.scenes[self.iscene].update(*events)
            for upd_event in update_events:
                if upd_event.evt == EVT.SCN.ISCENE:
                    self.set_iscene(upd_event.get_iscene())
                elif upd_event.evt == EVT.SCN.NEXT_SCENE:
                    self.next_scene()
                elif upd_event.evt == EVT.SCN.PREV_SCENE:
                    self.prev_scene()
                elif upd_event.evt == EVT.SCN.FIRST_SCENE:
                    self.first_scene()
                elif upd_event.evt == EVT.SCN.LAST_SCENE:
                    self.last_scene()

    def render(self):
        """render renders all scenes, events and nobject in the handler.
        """
        if self.iscene != -1:
            self.render_events = self.scenes[self.iscene].render(self.screen)
