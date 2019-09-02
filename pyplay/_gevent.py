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

    # GEvent destination
    SCENE = 1
    BOARD = 2
