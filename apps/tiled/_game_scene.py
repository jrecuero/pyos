import sys
import os
import pygame
from pyengine import Scene, GSpriteSheet, GAniImage, TileMap, GTileMap
# from pyengine import Log
from _game_board import GameBoard

ROWS = 32
COLS = 32
CSIZE = 32


class GameScene(Scene):

    def __init__(self, surface, **kwargs):
        super(GameScene, self).__init__("Game Tiled Scene", surface, **kwargs)
        game_folder = os.path.dirname(__file__)
        map_folder = os.path.join(game_folder, "tilemap")
        self.map = TileMap(os.path.join(map_folder, "base.tmx"))
        self.tile_map = GTileMap("world", self.map, 0, 0, 640, 640)
        self.player_sprite_sheet = GSpriteSheet(os.path.join(map_folder, "full_soldier.png"), CSIZE)
        self.player = GAniImage("player", self.player_sprite_sheet, 0, 0, CSIZE, CSIZE, 0, 3, keyboard=True)
        self.board = GameBoard(ROWS, COLS, 0, 0, CSIZE, CSIZE)
        self.board.add_tilemap(self.tile_map)
        self.board.add_gobject(self.player)
        self.add_gobject(self.board)

    def handle_keyboard_event(self, event, **kwargs):
        """handle_keyboard_event should process the keyboard event given.
        """
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_x]:
            sys.exit(0)
        if key_pressed[pygame.K_LEFT]:
            self.player.set_new_frames(12, 15)
            ok, collision = self.board.move_gobject_left()
        if key_pressed[pygame.K_RIGHT]:
            self.player.set_new_frames(8, 11)
            ok, collision = self.board.move_gobject_right()
        if key_pressed[pygame.K_UP]:
            self.player.set_new_frames(4, 7)
            ok, collision = self.board.move_gobject_up()
        if key_pressed[pygame.K_DOWN]:
            self.player.set_new_frames(0, 3)
            ok, collision = self.board.move_gobject_down()

        super(GameScene, self).handle_keyboard_event(event, **kwargs)

    def update(self, **kwargs):
        """update calls update method for all scene graphical objects.
        """
        super(GameScene, self).update(**kwargs)

    def render(self, **kwargs):
        """render calls render method for all scene graphical objects.
        """
        super(GameScene, self).render(**kwargs)
