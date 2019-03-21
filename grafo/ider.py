__ider: int = 0


def next_ider() -> int:
    global __ider
    __ider += 1
    return __ider
