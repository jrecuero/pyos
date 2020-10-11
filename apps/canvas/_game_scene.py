import sys
import pygame
from pyengine import Scene, GCanvas, GLoader
from _game_player import GamePlayer
from _game_gobjects import GameEnemy
from _settings import HEIGHT, IMAGES_PATH, LAYERS, PLAYER_LAYER, ENEMY_LAYER


class GameScene(Scene):

    def __init__(self, surface, **kwargs):
        super(GameScene, self).__init__("Canvas", surface, **kwargs)
        self.canvas = GCanvas("My Canvas", 2, 2, surface.get_width() - 4, surface.get_height() - 4, len(LAYERS))
        self.gloader = GLoader("canvas loader")
        plane_img = self.gloader.load_image(IMAGES_PATH, "plane.png")
        gplane = GamePlayer(plane_img, 32, HEIGHT - plane_img.get_rect().height * 3 / 2)
        self.canvas.add_gobject(gplane, PLAYER_LAYER)
        self.alien_img = self.gloader.load_image(IMAGES_PATH, "alien.png")
        galien = GameEnemy(self.alien_img, 32, 32)
        self.canvas.add_gobject(galien, ENEMY_LAYER)
        self.add_gobject(self.canvas)

    def handle_keyboard_event(self, event, **kwargs):
        """handle_keyboard_event should process the keyboard event given.
        """
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_x]:
            sys.exit(0)
        super(GameScene, self).handle_keyboard_event(event, **kwargs)

    def update(self, **kwargs):
        """update method update the GameScene instance.

        Args:
            **kwargs (dict): custom instance arguments.

        Returns:
            None: no return
        """
        super(GameScene, self).update(**kwargs)
        if len(self.canvas.glayers[ENEMY_LAYER]) == 0:
            galien = GameEnemy(self.alien_img, 32, 32)
            self.canvas.add_gobject(galien, ENEMY_LAYER)
