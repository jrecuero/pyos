import sys
import os
import pygame
from pyengine import Scene, GSpriteSheet, GAniImage, TileMap, GTileMap
# from pyengine import Log
from _game_board import GameBoard


class GameScene(Scene):

    def __init__(self, surface, **kwargs):
        super(GameScene, self).__init__("Game Tiled Scene", surface, **kwargs)
        game_folder = os.path.dirname(__file__)
        map_folder = os.path.join(game_folder, "tilemap")
        self.map = TileMap(os.path.join(map_folder, "base.tmx"))
        self.tile_map = GTileMap("world", self.map, 0, 0, 640, 640)
        # self.add_gobject(self.tile_map)
        self.player_sprite_sheet = GSpriteSheet(os.path.join(map_folder, "full_soldier.png"), 32)
        self.player = GAniImage("player", self.player_sprite_sheet, 0, 0, 32, 32, 0, 3)
        # self.add_gobject(self.player)
        self.board = GameBoard(32, 32, 0, 0, 32, 32)
        self.board.add_gobject(self.tile_map)
        self.board.add_gobject(self.player)
        self.add_gobject(self.board)

    def handle_keyboard_event(self, event, **kwargs):
        """handle_keyboard_event should process the keyboard event given.
        """
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_x]:
            sys.exit(0)
        if key_pressed[pygame.K_DOWN]:
            self.player.y += 32
            self.player.set_new_frames(0, 3)
        if key_pressed[pygame.K_UP]:
            self.player.y -= 32
            self.player.set_new_frames(4, 7)
        if key_pressed[pygame.K_RIGHT]:
            self.player.x += 32
            self.player.set_new_frames(8, 11)
        if key_pressed[pygame.K_LEFT]:
            self.player.x -= 32
            self.player.set_new_frames(12, 15)

        super(GameScene, self).handle_keyboard_event(event, **kwargs)

    def update(self, **kwargs):
        """update calls update method for all scene graphical objects.
        """
        super(GameScene, self).update(**kwargs)

    def render(self, **kwargs):
        """render calls render method for all scene graphical objects.
        """
        super(GameScene, self).render(**kwargs)
