import os
import pygame
from pyplay import Scene, GEvent, Color
from pyplay.gobject import GText, GImage, GCheckBox


class GameSceneTitle(Scene):
    """GameSceneTitle implements all functionality for the title scene.
    """

    def __init__(self, surface, **kwargs):
        super(GameSceneTitle, self).__init__("game title", surface, **kwargs)
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
        self.gobj_play_sound = GCheckBox("check-box", 500, 750, 25, 25, color=Color.RED)
        self.add_gobject(self.gobj_play_sound)
        self.add_gobject(GText("press", 550, 750, f"music on/off", bcolor=Color.ALPHA))

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
        pygame.mixer.music.stop()
        GEvent.handler_event(
            GEvent.HSCENE, source="board", music=self.gobj_play_sound.selected
        )
