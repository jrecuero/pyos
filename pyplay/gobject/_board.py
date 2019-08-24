import pygame

# from .._loggar import log
from .._color import Color
from .._point import Point
from .._gobject import GObject


class Board(GObject):
    """Board represents a graphical object that can contain other graphical
    objects, and it handles those inside their own graphical boundaries.
    """

    def __init__(self, name, x, y, dx, dy, **kwargs):
        super(Board, self).__init__(name, pos=Point(x, y), **kwargs)
        self.dx = dx
        self.dy = dy
        self.gobjects = []
        self.color = kwargs.get("color", Color.BLACK)
        self.outline = kwargs.get("outline", 0)
        self.set_content(pygame.Rect(self.x, self.y, self.dx, self.dy), GObject.BOARD)

    def __str__(self):
        return f"[{self.gid}] : {self.__class__.__name__} ({self.x}, {self.y}) ({self.dx}, {self.dy})"

    def bounds(self):
        """bounds should returns a rectangle that contains the board.
        """
        return self.content

    def add_gobject(self, gobject):
        """add_gobject adds a graphical object to the scene.
        """
        self.gobjects.append(gobject)

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
        for gobj in self.gobjects:
            gobj.update(surface, **kwargs)

        # only check those objects that can move for out of bounds or
        # collisions.
        for gobj in [obj for obj in self.gobjects if obj.move]:
            # -> check out of bound at this point
            # log.Board().GObject(gobj.bounds()).call()
            if not self.bounds().contains(gobj.bounds()):
                rect = gobj.bounds()
                if (rect.x < 0) or (rect.x + rect.w) > (self.x + self.dx):
                    response = gobj.out_of_bounds_x_response()
                elif (rect.y < 0) or (rect.y + rect.h) > (self.y + self.dy):
                    response = gobj.out_of_bounds_y_response()
                if not response:
                    rect.clamp_ip(self.bounds())
            # <-
            # -> check collision against any other object
            for other in [_ for _ in self.gobjects if _ != gobj]:
                rect = gobj.bounds()
                other_rect = other.bounds()
                if rect.colliderect(other_rect):
                    gobj.collide_with(other)
                    other.collide_with(gobj)
            # <-

    def render(self, surface, **kwargs):
        pygame.draw.rect(surface, self.color, self.content, self.outline)
        for gobj in sorted(self.gobjects, key=lambda obj: obj.z):
            gobj.render(surface, **kwargs)
