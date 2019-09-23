import os
import pygame
from pyplay import Scene, GEvent
from _game_tools import (
    CELL_SIZE,
    XSIZE_CELLS,
    YSIZE_CELLS,
    YSIZE_THRESHOLD,
    GRAVITY_TIMER,
)
from _game_board import GameBoard

SCREEN_SIZE = (1200, 850)
BOARD_ORIGIN = {"x": 50, "y": 50}
BOARD_SIZE = {"dx": CELL_SIZE * XSIZE_CELLS, "dy": CELL_SIZE * YSIZE_CELLS}


class GameSceneBoard(Scene):
    """GameSceneBoard implements all functionality for the scene that contains
    the board.
    """

    def __init__(self, surface, **kwargs):
        super(GameSceneBoard, self).__init__("game scene", surface, **kwargs)
        self.gobj_next_piece = None
        self.gtext_actor = None
        self.gtext_target = None
        self.board = None

    def open(self, **kwargs):
        """open is called when transitioning into the scene.
        """
        self.board = GameBoard(
            "gravity-board",
            BOARD_ORIGIN["x"],
            BOARD_ORIGIN["y"],
            BOARD_SIZE["dx"],
            BOARD_SIZE["dy"],
            CELL_SIZE,
            outline=1,
            threshold=YSIZE_THRESHOLD,
            gravity_timer=GRAVITY_TIMER,
        )
        self.board.next_piece()
        self.add_gobject(self.board)
        self.gobj_console = kwargs.get("console", None)
        if self.gobj_console:
            self.add_gobject(self.gobj_console)
        self.gobj_stats = kwargs.get("stats", None)
        if self.gobj_stats:
            self.gobj_stats.x = 450
            self.gobj_stats.y = 200
            self.add_gobject(self.gobj_stats)
        self.actor = kwargs.get("actor", None)
        gobj_actor = self.actor.gdisplay()
        gobj_actor.x = 450
        gobj_actor.y = 500
        self.add_gobject(gobj_actor)

        self.target = kwargs.get("target", None)
        self.gobj_target = self.target.gdisplay()
        self.gobj_target.x = 450
        self.gobj_target.y = 564
        self.add_gobject(self.gobj_target)

        if kwargs.get("music", True):
            pygame.mixer.music.stop()
            pygame.mixer.music.load(
                os.path.join("apps/sirtet/music", "bensound-elevate.mp3")
            )
            pygame.mixer.music.play(-1)

    def handle_custom_event(self, event):
        """handle_custom_event should process pygame custom event given.
        Any object in the game, like, scene, graphic objects, ... can post
        customs events, and those should be handled at this time.
        """
        super(GameSceneBoard, self).handle_custom_event(event)
        if event.type == GEvent.ENGINE:
            if event.subtype == GEvent.NEXT:
                if self.gobj_next_piece:
                    self.del_gobject(self.gobj_next_piece)
                self.gobj_next_piece = event.source
                self.gobj_next_piece.x = 550
                self.gobj_next_piece.y = 50
                self.add_gobject(self.gobj_next_piece)
            elif event.subtype == GEvent.CREATE:
                if getattr(event, "dest", None) == GEvent.SCENE:
                    self.del_gobject(self.gobj_target)
                    self.gobj_target = event.source
                    self.gobj_target.x = 450
                    self.gobj_target.y = 564
                    self.add_gobject(self.gobj_target)

    def render(self, **kwargs):
        """render calls render method for all scene graphical objects.
        """
        super(GameSceneBoard, self).render(**kwargs)
