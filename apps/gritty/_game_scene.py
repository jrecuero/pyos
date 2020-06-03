import sys
import pygame
from pyengine import Scene, Color, GEvent, GObject, GMenu
from pyengine import Log
from _game_board import GameBoard
from _game_actor import GameActor


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
                GEvent.post_event(
                    GEvent.ENGINE,
                    GEvent.LOGGER,
                    self,
                    GEvent.SCENE,
                    "GObject is being deleted")
                GEvent.post_event(
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
                GEvent.post_event(
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
        self.targets = [GameActor("target1", *self.board.g_cell(0, 0), cs, cs, color=Color.RED, life=100),
                        GameActor("target2", *self.board.g_cell(2, 4), cs, cs, color=Color.BLUE, life=100),
                        GameActor("target2", *self.board.g_cell(3, 8), cs, cs, color=Color.GREEN, life=100), ]
        self.actor = GameActor("actor", *self.board.g_cell(1, 1), cs, cs, keyboard=True)
        for target in self.targets:
            self.board.add_gobject(target, relative=False)
        self.board.add_gobject(self.actor, relative=False)
        self.add_gobject(self.board)
        self.menu = GMenu("menu", 450, 32, 100, 20)
        self.menu.add_menu_item("File")
        self.menu.add_menu_item("Edit")
        self.menu.add_menu_item("Window")
        self.menu.add_menu_item("Help")
        self.add_gobject(self.menu)
        self.event_battle_attack = GEvent.register_subtype_event("BATTLE_ATTACK")

    def handle_keyboard_event(self, event, **kwargs):
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
            event = GEvent.new_event(GEvent.APP_DEFINED,
                                     self.event_battle_attack,
                                     self,
                                     GEvent.SCENE,
                                     {"source": self.actor, "target": collision.solid_object}, )
            kwargs["event-bucket"].append(event)

        super(GameScene, self).handle_keyboard_event(event, **kwargs)

    def update(self, **kwargs):
        """update calls update method for all scene graphical objects.
        """
        event_bucket = kwargs["event-bucket"]
        while len(event_bucket):
            event = event_bucket.pop(0)
            if event.type == GEvent.APP_DEFINED and event.destination == GEvent.SCENE:
                if event.subtype == self.event_battle_attack:
                    source = event.payload["source"]
                    target = event.payload["target"]
                    damage = source.attack(target)
                    GEvent.post_event(
                        GEvent.ENGINE,
                        GEvent.LOGGER,
                        self,
                        GEvent.SCENE,
                        f"{source.name} attack {target.name} for {damage} hp: {target.life}.")
        super(GameScene, self).update(**kwargs)
        event_bucket = kwargs["event-bucket"]
        while len(event_bucket):
            event = event_bucket.pop(0)
            # Log.Scene(self.name).EventUpdateBucket(event).call()
            if event.type == GEvent.ENGINE and event.subtype == GEvent.DELETE and event.destination == GEvent.SCENE:
                GEvent.post_event(
                    GEvent.ENGINE,
                    GEvent.LOGGER,
                    self,
                    GEvent.SCENE,
                    f"Delete {event.source.name}")
                pass
