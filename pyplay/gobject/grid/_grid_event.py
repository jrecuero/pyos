from ..._gevent import GEvent


class GridEvent(GEvent):

    COMPLETED = GEvent.LAST + 1
    LAST = GEvent.LAST + 1
