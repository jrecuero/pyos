__GID = 0


def new_gid():
    """new_gid generates a new graphical object identifier.
    """
    global __GID
    __GID += 1
    return __GID
