import sys
import pygame
from pyengine import Scene, GRect, Color, Layer, GEvent, GObject
from pyengine import Log
from _game_board import GameBoard


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


class GameScene(Scene):

    def __init__(self, surface, **kwargs):
        cs = 32     # cell size
        super(GameScene, self).__init__("Game Scene", surface, **kwargs)
        self.board = GameBoard(10, 10, 32, 32, cs, cs)
        # row, col = self.board.g_cell(0, 0)
        # self.target = GRect("target", row, col, cs, cs, color=Color.RED)
        self.target = GRect("target", *self.board.g_cell(0, 0), cs, cs, color=Color.RED)
        # row, col = self.board.g_cell(2, 4)
        # self.deco = GTimed("decoration", row, col, cs, cs, z=Layer.BACKGROUND, color=Color.BLUE, solid=False, timed_counter=0)
        self.deco = GRect("decoration", *self.board.g_cell(2, 4), cs, cs, z=Layer.BACKGROUND, color=Color.BLUE)
        # row, col = self.board.g_cell(1, 1)
        # self.actor = GRect("actor", row, col, cs, cs, keyboard=True)
        self.actor = GRect("actor", *self.board.g_cell(1, 1), cs, cs, keyboard=True)
        # self.actor.move = Move(1, 1, 5)
        self.board.add_gobject(self.actor, relative=False)
        self.board.add_gobject(self.target, relative=False)
        self.board.add_gobject(self.deco, relative=False)
        self.add_gobject(self.board)

    def handle_keyboard_event(self, event):
        """handle_keyboard_event should process the keyboard event given.
        """
        ok, collision = False, None
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_x]:
            sys.exit(0)
        if key_pressed[pygame.K_LEFT]:
            ok, collision = self.board.move_player_left()
        if key_pressed[pygame.K_RIGHT]:
            ok, collision = self.board.move_player_right()
        if key_pressed[pygame.K_UP]:
            ok, collision = self.board.move_player_up()
        if key_pressed[pygame.K_DOWN]:
            ok, collision = self.board.move_player_down()
        if not ok and collision:
            GEvent.new_event(
                GEvent.ENGINE,
                GEvent.LOGGER,
                self,
                GEvent.SCENE,
                f"Player collision with {str(collision)}")

        super(GameScene, self).handle_keyboard_event(event)
