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

    def update(self, surface, **kwargs):
        for gobj in self.gobjects:
            gobj.update(surface, **kwargs)
            # -> check out of bound at this point
            # log.Board().GObject(gobj.bounds()).call()
            if not self.bounds().contains(gobj.bounds()):
                rect = gobj.bounds()
                if (rect.x < 0) or (rect.x + rect.w) > (self.x + self.dx):
                    gobj.bounce_x()
                elif (rect.y < 0) or (rect.y + rect.h) > (self.y + self.dy):
                    gobj.bounce_y()
                rect.clamp_ip(self.bounds())
                # gobj.reverse()
            # <-
            # -> check collision
            pass
            # <-

    def render(self, surface, **kwargs):
        pygame.draw.rect(surface, self.color, self.content, self.outline)
        for gobj in self.gobjects:
            gobj.render(surface, **kwargs)
