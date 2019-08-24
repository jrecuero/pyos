import pygame


class GEvent:
    """GEvent implements all codes related with user events used in the
    application via pygame events.
    """

    # pygame.USEREVENT = 24
    USER = pygame.USEREVENT
    CREATE = pygame.USEREVENT + 1
    DELETE = pygame.USEREVENT + 2
    # limit is pygame.NUMEVENTS = 32
