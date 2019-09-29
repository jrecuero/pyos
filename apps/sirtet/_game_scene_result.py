from pyplay import Scene


class GameSceneResult(Scene):
    """GameSceneResult implements scene where match results are being
    displayed.
    """

    def __init__(self, surface, **kwargs):
        super(GameSceneResult, self).__init__("game main", surface, **kwargs)
