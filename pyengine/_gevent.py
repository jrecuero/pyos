import pygame
from ._loggar import Log


class GEvent:
    """GEvent implements all codes related with user events used in the
    application via pygame events.
    """

    NONE = 0

    # GEvent type. Used by pygame events.
    # pygame.USEREVENT = 24
    USER = pygame.USEREVENT
    ENGINE = pygame.USEREVENT + 1
    TIMER = pygame.USEREVENT + 2
    CALLBACK = pygame.USEREVENT + 3

    # GEvent subtype. Used internaly
    MOVE_TO = 1
    DELETE = 2
    CREATE = 3

    # Event Source/Destination
    HANDLER = 1
    SCENE = 2
    BOARD = 3
    OBJECT = 4
    OTHER = 5

    @staticmethod
    def check_destination(event, dest):
        """check_destination checked if the given destination is in the event
        dest attribute.
        """
        if isinstance(event.destination, list):
            return dest in event.destination
        else:
            return dest == event.destination

    @staticmethod
    def new_event(etype, esubtype, source, destination, payload, **kwargs):
        """new_event creates a new event.
        """
        the_event = pygame.event.Event(etype, subtype=esubtype, source=source, destination=destination, payload=payload, **kwargs)
        pygame.event.post(the_event)
        Log.Event(etype).Subtype(esubtype).Source(source).Destination(destination).Payload(str(payload)).Kwargs(kwargs).call()
