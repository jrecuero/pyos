import pygame


class GEvent:
    """GEvent implements all codes related with user events used in the
    application via pygame events.
    """

    # pygame.USEREVENT = 24
    ENGINE = pygame.USEREVENT
    T_GRAVITY = pygame.USEREVENT + 1
    # limit is pygame.NUMEVENTS = 32 // +8

    CREATE = 1
    DELETE = 2
    END = 3
    PAUSE = 4
    COMPLETED = 5
    NEXT = 6
    DISPLAY = 7
