import pygame


class GEvent:
    """GEvent implements all codes related with user events used in the
    application via pygame events.
    """

    NONE = 0

    # pygame.USEREVENT = 24
    ENGINE = pygame.USEREVENT
    T_GRAVITY = pygame.USEREVENT + 1
    # limit is pygame.NUMEVENTS = 32 // +8

    # GEvent subtype
    CREATE = 1
    DELETE = 2
    END = 3
    PAUSE = 4
    COMPLETED = 5
    NEXT = 6
    DISPLAY = 7
    SKILL = 8
    HSCENE = 9

    # GEvent destination
    HANDLER = 1
    SCENE = 2
    BOARD = 3

    @staticmethod
    def check_destination(event, dest):
        """check_destination checked if the given destination is in the event
        dest attribute.
        """
        if isinstance(event.dest, list):
            return dest in event.dest
        else:
            return dest == event.dest

    @staticmethod
    def engine_event(subtype, **kwargs):
        """engine_event sends an event to any engine component.
        """
        the_event = pygame.event.Event(GEvent.ENGINE, subtype=subtype, **kwargs)
        pygame.event.post(the_event)

    @staticmethod
    def handler_event(subtype, **kwargs):
        """handler_event sends an event to the handler.
        """
        the_event = pygame.event.Event(
            GEvent.ENGINE, subtype=subtype, dest=GEvent.HANDLER, **kwargs
        )
        pygame.event.post(the_event)

    @staticmethod
    def scene_event(subtype, **kwargs):
        """scene_event sends an event to the scene.
        """
        the_event = pygame.event.Event(
            GEvent.ENGINE, subtype=subtype, dest=GEvent.SCENE, **kwargs
        )
        pygame.event.post(the_event)

    @staticmethod
    def board_event(subtype, **kwargs):
        """board_event sends an event to the board.
        """
        the_event = pygame.event.Event(
            GEvent.ENGINE, subtype=subtype, dest=GEvent.BOARD, **kwargs
        )
        pygame.event.post(the_event)
