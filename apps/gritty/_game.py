import sys
import pygame
from pyengine import Scene, GRect, GHandler, Color, Grid, Layer, GEvent, GObject
from pyengine import Log


class GTimed(GObject):
    """GTimed contains all information with any graphical object that requires
    a timer in order to work.
    """

    def __init__(self, name, x, y, dx, dy, **kwargs):
        super(GTimed, self).__init__(name, x, y, dx, dy, **kwargs)
        pygame.draw.rect(self.image, self.color, (0, 0, self.dx, self.dy), self.outline)
        self.timed_tick = 0
        self.timed_tick_counter = 0
        self.timed_threshold = kwargs.get("timed_threshold", 100)
        self.timed_counter = kwargs.get("timed_counter", 0)
        self.timed_event_type = kwargs.get("timed_event_type", GEvent.CALLBACK)
        self.timed_event_subtype = kwargs.get("timed_event_subtype", GEvent.MOVE_TO)
        self.timed_event_destination = kwargs.get("timed_destination", GEvent.BOARD)

    def timed_callback(self, dx, dy):
        """timed_callback is the function to be executed every time timer expires.
        """
        def _timed_callback():
            # self.move_it(dx, dy)
            if self.timed_tick_counter == 3:
                GEvent.new_event(
                    GEvent.ENGINE,
                    GEvent.LOGGER,
                    self,
                    GEvent.SCENE,
                    "GObject is being deleted")
                GEvent.new_event(
                    self.timed_event_type,
                    GEvent.DELETE,
                    self,
                    self.timed_event_destination,
                    {
                        "callback": None,
                        "validation": None,
                    })
        return _timed_callback

    def update(self, surface, **kwargs):
        """update updates object.
        """
        super(GTimed, self).update(surface, **kwargs)
        if self.timed_counter == 0 or self.timed_counter > self.timed_tick_counter:
            if self.timed_tick == sys.maxsize:
                self.timed_tick = 0
            if self.timed_tick_counter == sys.maxsize:
                self.timed_tick_counter = 0
            self.timed_tick += 1
            if self.timed_tick % self.timed_threshold == 0:
                self.timed_tick_counter += 1
                Log.Update(self.name).Counter(self.timed_tick).call()
                GEvent.new_event(
                    self.timed_event_type,
                    self.timed_event_subtype,
                    self,
                    self.timed_event_destination,
                    {
                        "callback": self.timed_callback(self.dx, self.dy),
                        "validation": lambda: (self.dx, self.dy)
                    })


class GameBoard(Grid):

    def __init__(self, rows, cols, g_x, g_y, g_dx, g_dy, **kwargs):
        super(GameBoard, self).__init__("Game Board", rows, cols, g_x, g_y, g_dx, g_dy, **kwargs)

    def handle_keyboard_event(self, event):
        """handle_keyboard_event should process the keyboard event given.
        """
        if self.running:
            if self.catch_keyboard_gobject:
                key_pressed = pygame.key.get_pressed()
                if key_pressed[pygame.K_x]:
                    sys.exit(0)
        super(GameBoard, self).handle_keyboard_event(event)

    def handle_custom_event(self, event):
        """handle_custom_event should process pygame custom event given.
        Any object in the game, like, scene, graphic objects, ... can post
        customs events, and those should be handled at this time.
        """
        super(GameBoard, self).handle_custom_event(event)


class GameScene(Scene):

    def __init__(self, surface, **kwargs):
        cs = 32     # cell size
        super(GameScene, self).__init__("Game Scene", surface, **kwargs)
        self.target = GRect("target", 0, 0, cs, cs, color=Color.RED)
        self.deco = GTimed("decoration", 4 * cs, 2 * cs, cs, cs, z=Layer.BACKGROUND, color=Color.BLUE, solid=False, timed_counter=0)
        self.actor = GRect("actor", cs, cs, cs, cs, keyboard=True)
        # self.actor.move = Move(1, 1, 5)
        self.grid = GameBoard(10, 10, 32, 32, cs, cs)
        self.grid.add_gobject(self.actor)
        self.grid.add_gobject(self.target)
        self.grid.add_gobject(self.deco)
        self.add_gobject(self.grid)


class GameHandler(GHandler):

    def __init__(self, surface, clock, **kwargs):
        super(GameHandler, self).__init__("Gritty", surface, clock, **kwargs)
