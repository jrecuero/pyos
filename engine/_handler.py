from typing import Any, List, Optional

import sys
import traceback

from ._event import EVT, Timer, Event, EventKey, EventTimer
from ._scene import Scene
from ._loggar import log
from ._dplug import get_plugin


def plug_exc(exit: bool = False):
    def _plug_exc(f):
        def __plug_exc(self, *args):
            try:
                return f(self, *args)
            except KeyboardInterrupt:
                self.restore_screen(self.screen)
                log.Error("KeyboardInterrupt").call()
            except get_plugin().exception() as ex:
                self.restore_screen(self.screen)
                log.Error({"display.plug.exception": "{}".format(ex)}).call()
                for l in traceback.format_exc().splitlines():
                    print(l)
            except Exception as ex:
                self.restore_screen(self.screen)
                log.Error({"Exception": "{}".format(ex)}).call()
                for l in traceback.format_exc().splitlines():
                    print(l)
            finally:
                if exit:
                    self.restore_screen(self.screen)
                    sys.exit(0)

        return __plug_exc

    return _plug_exc


class Handler(object):
    """Handler class handles a full scene scenario.
    """

    __slots__ = [
        "screen",
        "scenes",
        "iscene",
        "key",
        "tick",
        "timers",
        "render_events",
        "pinput_events",
        "keys",
    ]

    def __init__(self, tick: float = 10):
        self.screen: Any = get_plugin().init()
        self.scenes: List[Scene] = []
        self.iscene: int = -1
        self.key: int = -1
        self.tick: float = tick
        self.timers: List[Timer] = []
        self.render_events: List[Event] = []
        self.pinput_events: List[Event] = []
        self.keys: List[int] = []

    def colors(self, color_pairs):
        """colors setups for using given list of color pairs.
        """
        get_plugin().colors(color_pairs)

    def run(self):
        """run runs all scenes.
        """
        self.__main(self.screen)

    def __get_input(self) -> int:
        """__get_input is an internal method that loops for any user input key
        being entered.
        """
        return get_plugin().get_ch(self.screen)

    def get_input(self) -> int:
        """get_input gets the input from the active scene.
        """
        if self.iscene != -1:
            return self.scenes[self.iscene].get_input(self.screen)
        else:
            return self.__get_input()

    def restore_screen(self, screen: Any = None):
        """restore_screen restores the terminal screen to the original
        configuration.
        """
        if screen is None:
            screen = self.screen
        get_plugin().restore_screen(screen)

    @plug_exc(True)
    def __main(self, screen: Any):
        """__main is an internal method that implements the handler main
        loop functionality.
        """
        self.screen = screen
        get_plugin().nodelay(screen, True)
        get_plugin().cursor(False)
        while True:
            get_plugin().wait(self.tick)
            key = self.get_input()
            if key != -1:
                self.keys.append(key)
            self.screen_erase()
            self.pinput()
            self.update()
            self.render()

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

    @plug_exc()
    def add_scene(self, scn: Scene) -> Scene:
        """add_scene adds a scene to the handler.
        """
        scn.setup(self.screen)
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

    def _move_to_scene(self, iscene: int = 0) -> int:
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

    def first_scene(self) -> int:
        return self._move_to_scene()

    def last_scene(self) -> int:
        last = len(self.scenes) - 1
        return self._move_to_scene(last)

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

    def update_timers(self):
        """update_timers proceeds to update all scene timers.
        """
        events = []
        for t in self.timers:
            if t.inc():
                events.append(EventTimer(t))
        return events

    def screen_erase(self):
        """screen_erase proceeds to erase active scene screen.
        """
        if self.iscene != -1:
            self.scenes[self.iscene].screen_erase(self.screen)

    def pinput(self):
        """pinput checks any user input for the main scene.
        """
        if self.iscene != -1:
            self.pinput_events = self.scenes[self.iscene].pinput(self.screen, self.keys)

    def update(self):
        """update updates scenes, events and nobject in the handler.
        """
        if self.iscene != -1:
            events = []
            events.extend(self.pinput_events)
            events.extend(self.render_events)
            if len(self.keys):
                events.append(EventKey(self.keys.pop()))
            events.extend(self.update_timers())
            update_events = self.scenes[self.iscene].update(self.screen, *events)
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
        get_plugin().doupdate()
