import sys
import pygame
from pyengine import Scene, GCanvas, GLoader, GText
from _game_player import GamePlayer
from _game_gobjects import GameEnemy
from _settings import HEIGHT, IMAGES_PATH, LAYERS, PLAYER_LAYER, ENEMY_LAYER


class GameScene(Scene):

    def __init__(self, surface, **kwargs):
        super(GameScene, self).__init__("Canvas", surface, **kwargs)
        self.canvas = GCanvas("My Canvas", 2, 2, surface.get_width() - 4, surface.get_height() - 4, len(LAYERS))
        self.gloader = GLoader("canvas loader")
        plane_img = self.gloader.load_image(IMAGES_PATH, "plane.png")
        self.gplane = GamePlayer(plane_img, 32, HEIGHT - plane_img.get_rect().height * 3 / 2, owner=self)
        # self.gplane.owner = self
        self.canvas.add_gobject(self.gplane, PLAYER_LAYER)
        self.alien_img = self.gloader.load_image(IMAGES_PATH, "alien.png")
        self.galien = GameEnemy(self.alien_img, 32, 32, owner=self)
        self.canvas.add_gobject(self.galien, ENEMY_LAYER)
        self.score = 0
        self.widget_score = GText("score", 32, HEIGHT - 32, f"SCORE: 000000")
        self.canvas.add_gobject(self.widget_score, PLAYER_LAYER)
        self.add_gobject(self.canvas)

    def notify(self, instance, notification):
        """Notify method is called when any instance owned by the session has
        an event (DELETED, ...).

        Args:
            instance (Object): instance owned by the scene.
            notification (str): type of notification

        Returns:
            None: no return.

        """
        if instance == self.gplane and notification == "DELETED":
            sys.exit(0)
        if instance == self.galien and notification == "DELETED":
            self.score += 10
            self.widget_score.message = f"SCORE: {self.score}"

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
            self.galien = GameEnemy(self.alien_img, 32, 32, owner=self)
            self.canvas.add_gobject(self.galien, ENEMY_LAYER)
