from typing import Dict, List, Callable, Optional


class EVT:
    """EVT class contains enums required to identify events and scenes.
    """

    class ENG:
        """ENG class contains enums to identify engine events.
        """

        KEY: int = 100
        TIMER: int = 200
        INPUT: int = 300
        SELECT: int = 400
        MENU: int = 500

    class SCN:
        """SCN class contains enums to identify engine scenes.
        """

        ISCENE: int = 1000
        NEXT_SCENE: int = 1001
        PREV_SCENE: int = 1002
        FIRST_SCENE: int = 1003
        LAST_SCENE: int = 1004


class Timer:
    """Timer class identify an timer counter.
    """

    def __init__(self, timeout: int, enable: bool = True):
        self.timeout: int = timeout
        self.__counter: int = 0
        self.enable: bool = enable

    def inc(self) -> bool:
        """inc returns True when counter has expired, False else.
        """
        if self.enable:
            self.__counter += 1
            if self.__counter >= self.timeout:
                self.__counter = 0
                return True
        return False


class Event:
    """Event class identifies any engine event to be used.
    """

    def __init__(self, evt: int, **kwargs):
        self.evt = evt
        self.params = kwargs

    def get_key(self) -> Optional[int]:
        """get_key returns the key attribute for an event.
        """
        if self.evt == EVT.ENG.KEY:
            return self.params.get("key", None)
        return None

    def get_timer(self) -> Optional[Timer]:
        """get_key returns the timer attribute for an event.
        """
        if self.evt == EVT.ENG.TIMER:
            return self.params.get("timer", None)
        return None

    def get_input(self) -> Optional[str]:
        """get_input returns the input attribute for an event.
        """
        if self.evt == EVT.ENG.INPUT:
            return self.params.get("input_str", None)
        return None

    def get_selected_index(self) -> int:
        """get_selected_index returns the index for the token selected.
        """
        if self.evt == EVT.ENG.SELECT:
            return self.params.get("index", None)

    def get_selected_data(self) -> str:
        """get_selected_data returns the data for the token selected.
        """
        if self.evt == EVT.ENG.SELECT:
            return self.params.get("data", None)

    def get_iscene(self) -> Optional[int]:
        """get_iscene returns the iscene attribute for an event.
        """
        if self.evt == EVT.SCN.ISCENE:
            return self.params.get("iscene", None)
        return None

    def exit_on_key(self, key: str):
        """exit_on_key allows to exit the application for the given key.
        """
        if self.evt == EVT.ENG.KEY and self.get_key() == ord(key):
            exit(0)


class EventKey(Event):
    """EventKey class identifies a Key Event.
    """

    def __init__(self, key: int):
        super(EventKey, self).__init__(EVT.ENG.KEY, key=key)


class EventTimer(Event):
    """EventTimer class identifies a Timer Event.
    """

    def __init__(self, t: Timer):
        super(EventTimer, self).__init__(EVT.ENG.TIMER, timer=t)


class EventInput(Event):
    """EventInput class identifies an Input Event.
    """

    def __init__(self, data: str):
        super(EventInput, self).__init__(EVT.ENG.INPUT, input_str=data)


class EventSelected(Event):
    """EventSelected class identifies when a Selection is done.
    """

    def __init__(self, index: int, data: str):
        super(EventSelected, self).__init__(EVT.ENG.SELECT, index=index, data=data)


class EventMenuItem(Event):
    """EventMenuItem class identifies when a menu item is selected.
    """

    def __init__(self, select_str: str, callback):
        super(EventMenuItem, self).__init__(
            EVT.ENG.MENU, select_str=select_str, callback=callback
        )


class EventIScene(Event):
    """EventIScene class identifies an IScene Event.
    """

    def __init__(self, iscene: int):
        super(EventIScene, self).__init__(EVT.SCN.ISCENE, iscene=iscene)


class EventNextScene(Event):
    """EventNextScene class identifies a Next Scene Event.
    """

    def __init__(self):
        super(EventNextScene, self).__init__(EVT.SCN.NEXT_SCENE)


class EventPrevScene(Event):
    """EventPrevScene class identifies a Prev Scene Event.
    """

    def __init__(self):
        super(EventPrevScene, self).__init__(EVT.SCN.PREV_SCENE)


class EventFirstScene(Event):
    """EventFirstScene class identifies a First Scene Event.
    """

    def __init__(self):
        super(EventFirstScene, self).__init__(EVT.SCN.FIRST_SCENE)


class EventLastScene(Event):
    """EventLastScene class identifies a Last Scene Event.
    """

    def __init__(self):
        super(EventLastScene, self).__init__(EVT.SCN.LAST_SCENE)


class KeyHandler:
    """KeyHandler class allows to handle any Key Event in a common and
    abstract way.
    """

    def __init__(self, keyreg: Dict[str, Callable[[], List[Event]]]):
        self.keyreg = keyreg

    def register(self, key: str, cb: Callable[[], List[Event]]):
        """register adds a key to be handle.
        """
        self.keyreg[key] = cb

    def deregister(self, key):
        """deregister removes a key to be handle.
        """
        del self.keyreg[key]

    def update(self, event: Event) -> List[Event]:
        """update looks fo the proper handle for the key being entered.
        """
        event_to_return: List[Event] = []
        if event.evt == EVT.ENG.KEY and event.get_key() is not None:
            key = event.get_key()
            for k, cb in self.keyreg.items():
                if key == ord(k):
                    return cb()
        return event_to_return
