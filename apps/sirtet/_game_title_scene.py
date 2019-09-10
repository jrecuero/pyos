from pyplay import Scene


class GameTitleScene(Scene):
    """GameTitleScene implements all functionality for the title scene.
    """

    def __init__(self, surface, **kwargs):
        super(GameTitleScene, self).__init__("game title", surface, **kwargs)
