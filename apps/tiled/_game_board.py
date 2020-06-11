# import sys
# import pygame
from pyengine import Grid
from pyengine import Log


class GameBoard(Grid):

    NONE = 0
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4

    def __init__(self, rows, cols, grid_origin_x, grid_origin_y, cell_width, cell_height, **kwargs):
        super(GameBoard, self).__init__("Game Board", rows, cols, grid_origin_x, grid_origin_y, cell_width, cell_height, **kwargs)
        self.player_turn = True
        self.off_player_counter = 0

    def move_it_gobject(self, gobject, dx, dy):
        """move_it_gobject moves the given object the given x-y delta.
        """
        return super(GameBoard, self).move_it_gobject(gobject, dx, dy)

    def move_player_to(self, direction):
        """move_player_to moves the player to the given direction.
        """
        if self.catch_keyboard_gobject and self.player_turn:
            if direction == GameBoard.LEFT:
                ok, collision = self.move_it_gobject(self.catch_keyboard_gobject, -self.g_cell_size.x, 0)
            elif direction == GameBoard.RIGHT:
                ok, collision = self.move_it_gobject(self.catch_keyboard_gobject, self.g_cell_size.x, 0)
            elif direction == GameBoard.UP:
                ok, collision = self.move_it_gobject(self.catch_keyboard_gobject, 0, -self.g_cell_size.y)
            elif direction == GameBoard.DOWN:
                ok, collision = self.move_it_gobject(self.catch_keyboard_gobject, 0, self.g_cell_size.y)
            else:
                return False, None
            if ok:
                self.player_turn = False
                Log.Board(self.name).EndPlayerTurn().call()
            return ok, collision
        return True, None

    def move_player_left(self):
        """move_player_left moves the player to the left.
        """
        return self.move_player_to(GameBoard.LEFT)

    def move_player_right(self):
        """move_player_right moves the player to the right.
        """
        return self.move_player_to(GameBoard.RIGHT)

    def move_player_up(self):
        """move_player_up moves the player to the up.
        """
        return self.move_player_to(GameBoard.UP)

    def move_player_down(self):
        """move_player_down moves the player to the down.
        """
        return self.move_player_to(GameBoard.DOWN)

    def handle_keyboard_event(self, event, **kwargs):
        """handle_keyboard_event should process the keyboard event given.
        """
        if self.player_turn:
            super(GameBoard, self).handle_keyboard_event(event, **kwargs)

    def handle_custom_event(self, event, **kwargs):
        """handle_custom_event should process pygame custom event given.
        Any object in the game, like, scene, graphic objects, ... can post
        customs events, and those should be handled at this time.
        """
        super(GameBoard, self).handle_custom_event(event, **kwargs)

    def update(self, surface, **kwargs):
        """update provides any functionality to be done every tick.
        """
        super(GameBoard, self).update(surface, **kwargs)
        # event_bucket = kwargs["event-bucket"]
        # bucket = []
        # while len(event_bucket):
        #     event = event_bucket.pop(0)
        #     # Log.Scene(self.name).EventUpdateBucket(event).call()
        #     if event.type == GEvent.ENGINE and event.subtype == GEvent.DELETE and event.destination == GEvent.BOARD:
        #         self.del_gobject(event.source)
        #         event.destination = GEvent.SCENE
        #         bucket.append(event)
        # event_bucket.extend(bucket)
