import os
import pygame
from pyplay import Scene, Color
from pyplay.gobject import GText, GInput


class GameSceneEnd(Scene):
    """GameSceneEnd implements all functionality for the end scene.
    """

    def __init__(self, surface, **kwargs):
        super(GameSceneEnd, self).__init__("game end", surface, **kwargs)
        self.add_gobject(GText("press", 500, 250, f"Game Over", bcolor=Color.ALPHA))
        self.add_gobject(
            GText("press", 500, 300, f"Enter your name:", bcolor=Color.ALPHA)
        )
        self.gobj_name = GInput("name", 700, 300, 200, 25)
        self.add_gobject(self.gobj_name)

    def open(self, **kwargs):
        """open is called when transitioning into the scene.
        """
        pygame.mixer.music.stop()
        pygame.mixer.music.load(
            os.path.join("apps/sirtet/music", "bensound-ukulele.mp3")
        )
        pygame.mixer.music.play(-1)

    def handle_keyboard_event(self, event):
        """handle_keyboard_event should process the keyboard event given.
        Keyboard events are passed to the active scene to be handle.
        """
        super(GameSceneEnd, self).handle_keyboard_event(event)
