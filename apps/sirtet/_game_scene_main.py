from pyplay import Scene


class GameSceneMain(Scene):
    """GameSceneMain implements the game main scene, where any other scene
    should be trigger.
    """

    def __init__(self, surface, **kwargs):
        super(GameSceneMain, self).__init__("game main", surface, **kwargs)
