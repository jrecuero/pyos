# import os
import pygame
from pyplay import Scene, GEvent, Color
from pyplay.gobject import GText, GImage, GCheckBox
from _game_loader import load_image, load_music


class GameSceneTitle(Scene):
    """GameSceneTitle implements all functionality for the title scene.
    """

    def __init__(self, surface, **kwargs):
        super(GameSceneTitle, self).__init__("game title", surface, **kwargs)
        background_image = load_image("apps/sirtet/images", "sirtet.jpg")
        self.add_gobject(
            GImage(
                "background",
                # os.path.join("apps/sirtet/images", "sirtet.jpg"),
                background_image,
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
        self.gobj_play_music = GCheckBox(
            "play-music", 500, 750, 25, 25, color=Color.RED
        )
        self.add_gobject(self.gobj_play_music)
        self.add_gobject(GText("press", 550, 750, f"music on/off", bcolor=Color.ALPHA))

    def open(self, **kwargs):
        """open is called when transitioning into the scene.
        """
        pygame.mixer.music.stop()
        # pygame.mixer.music.load(os.path.join("apps/sirtet/music", "bensound-epic.mp3"))
        load_music("apps/sirtet/music", "bensound-epic.mp3")
        pygame.mixer.music.play(-1)

    def handle_keyboard_event(self, event):
        """handle_keyboard_event should process the keyboard event given.
        Keyboard events are passed to the active scene to be handle.
        """
        if event.type == pygame.KEYUP:
            pygame.mixer.music.stop()
            GEvent.handler_event(
                GEvent.HSCENE, source="board", music=self.gobj_play_music.selected
            )
