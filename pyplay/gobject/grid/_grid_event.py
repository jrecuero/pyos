from ..._gevent import GEvent


class GridEvent(GEvent):

    COMPLETED = GEvent.LAST + 1
    NEXT = GEvent.LAST + 2
    LAST = GEvent.LAST + 2
    # limit is pygame.NUMEVENTS = 32
