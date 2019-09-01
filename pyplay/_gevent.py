import pygame


class GEvent:
    """GEvent implements all codes related with user events used in the
    application via pygame events.
    """

    # pygame.USEREVENT = 24
    GRAVITY = pygame.USEREVENT
    DB = pygame.USEREVENT + 1  # CREATE, DELETE,
    HANDLING = pygame.USEREVENT + 2  # END, PAUSE, TIMER
    GAMEPLAY = pygame.USEREVENT + 3  # COMPLETED,
    DISPLAY = pygame.USEREVENT + 4  # NEXT, DISPLAY
    # CREATE = pygame.USEREVENT + 1
    # DELETE = pygame.USEREVENT + 2
    # END = pygame.USEREVENT + 3
    # GRAVITY = pygame.USEREVENT + 4
    # PAUSE = pygame.USEREVENT + 5
    # COMPLETED = pygame.USEREVENT + 6
    # NEXT = pygame.USEREVENT + 7
    # DISPLAY = pygame.USEREVENT + 8
    # TIMER = pygame.USEREVENT + 9
    # LAST = pygame.USEREVENT + 10
    # limit is pygame.NUMEVENTS = 32 // +8

    CREATE = 1
    DELETE = 2
    END = 3
    PAUSE = 4
    COMPLETED = 5
    NEXT = 6
    GDISPLAY = 7
