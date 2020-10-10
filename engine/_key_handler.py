from ._event import KeyHandler
from ._dplug import get_plugin


KEY_SPACE = " "
KEY_EXIT = "x"


class ArrowKeyHandler(KeyHandler):
    def __init__(self, **kwargs):
        super(ArrowKeyHandler, self).__init__()
        self.register(KEY_EXIT, lambda: exit(0))
        self.register(chr(get_plugin().key("KEY_LEFT")), kwargs.get("left", None))
        self.register(chr(get_plugin().key("KEY_RIGHT")), kwargs.get("right", None))
        self.register(chr(get_plugin().key("KEY_UP")), kwargs.get("up", None))
        self.register(chr(get_plugin().key("KEY_DOWN")), kwargs.get("down", None))
        self.register(KEY_SPACE, kwargs.get("space", None))
