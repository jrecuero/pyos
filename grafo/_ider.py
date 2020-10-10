__ider: int = 0


def _next_ider() -> int:
    global __ider
    __ider += 1
    return __ider


class Iderable:
    __slots__ = ["ider", "label"]

    def __init__(self, label: str = None):
        self.ider: int = _next_ider()
        self.label: str = label
