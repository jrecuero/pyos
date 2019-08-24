import pygame

from .._loggar import log
from .._gobject import GObject


class Board(GObject):
    """Board represents a graphical object that can contain other graphical
    objects, and it handles those inside their own graphical boundaries.
    """

    def __init__(self, name, x, y, dx, dy, **kwargs):
        super(Board, self).__init__(name, x, y, dx, dy, **kwargs)
        self.gobjects = pygame.sprite.Group()
        pygame.draw.rect(self.image, self.color, (0, 0, self.dx, self.dy), self.outline)

    def __str__(self):
        return f"[{self.gid}] : {self.__class__.__name__} ({self.x}, {self.y}) ({self.dx}, {self.dy})"

    def add_gobject(self, gobject):
        """add_gobject adds a graphical object to the scene.
        """
        self.gobjects.add(gobject)

    def del_gobject(self, gobject):
        """del_gobject deletes a graphical object from the scene.
        """
        if gobject in self.gobjects:
            self.gobjects.remove(gobject)

    def handle_keyboard_event(self, event):
        """handle_keyboard_event should process the keyboard event given.
        """
        for gobj in self.gobjects:
            gobj.handle_keyboard_event(event)

    def handle_custom_event(self, event):
        """handle_custom_event should process pygame custom event given.
        Any object in the game, like, scene, graphic objects, ... can post
        customs events, and those should be handled at this time.
        """
        for gobj in self.gobjects:
            gobj.handle_custom_event(event)

    def update(self, surface, **kwargs):
        self.gobjects.update(surface)

        # only check those objects that can move for out of bounds or
        # collisions.
        for gobj in [obj for obj in self.gobjects if obj.move]:
            # -> check out of bound at this point
            log.Board().OutOfBounds(str(gobj)).call()
            if not self.rect.contains(gobj.rect):
                rect = gobj.rect
                if (rect.x < 0) or (rect.x + rect.w) > (self.x + self.dx):
                    response = gobj.out_of_bounds_x_response()
                elif (rect.y < 0) or (rect.y + rect.h) > (self.y + self.dy):
                    response = gobj.out_of_bounds_y_response()
                if not response:
                    rect.clamp_ip(self.rect)
            # <-
            # -> check collision against any other object
            for other in [_ for _ in self.gobjects if _ != gobj]:
                rect = gobj.rect
                other_rect = other.rect
                if rect.colliderect(other_rect):
                    gobj.collide_with(other)
                    other.collide_with(gobj)
            # <-

    def render(self, surface, **kwargs):
        self.gobjects.draw(surface)
