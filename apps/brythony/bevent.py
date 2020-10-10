class BryEvent:
    def __init__(self, system, event, source, dest, evargs, **kwargs):
        self.system = system
        self.event = event
        self.source = source
        self.dest = dest
        self.evargs = evargs


def move_bevent(source, dest, x, y):
    evt = BryEvent("update", "move", source, dest, evargs={"x": x, "y": y})
    return evt


def rotate_bevent(source, dest, rotation):
    evt = BryEvent("update", "rotate", source, dest, evargs={"rotation": rotation})
    BryEvent("update", "rotate", source, dest, evargs={"rotation": rotation})
    return evt
