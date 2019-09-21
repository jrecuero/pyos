import os
import pygame
from pyplay import Scene, GEvent, Color
from pyplay.gobject import GText, GImage


class GameTitleScene(Scene):
    """GameTitleScene implements all functionality for the title scene.
    """

    def __init__(self, surface, **kwargs):
        super(GameTitleScene, self).__init__("game title", surface, **kwargs)
        self.add_gobject(
            GImage(
                "background",
                os.path.join("apps/sirtet/images", "sirtet.jpg"),
                0,
                0,
                1200,
                850,
            )
        )
        self.add_gobject(
            GText(
                "press", 500, 700, f"press any key to continue...", bcolor=Color.ALPHA
            )
        )

    def open(self, **kwargs):
        """open is called when transitioning into the scene.
        """
        pygame.mixer.music.stop()
        pygame.mixer.music.load(os.path.join("apps/sirtet/music", "bensound-epic.mp3"))
        pygame.mixer.music.play(-1)

    def handle_keyboard_event(self, event):
        """handle_keyboard_event should process the keyboard event given.
        Keyboard events are passed to the active scene to be handle.
        """
        GEvent.handler_event(GEvent.HSCENE, source="next")
