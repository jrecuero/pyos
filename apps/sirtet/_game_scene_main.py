from pyplay import Scene


class GameSceneMain(Scene):
    """GameSceneMain implements the game main scene, where any other scene
    should be trigger.
    """

    def __init__(self, surface, **kwargs):
        super(GameSceneMain, self).__init__("game main", surface, **kwargs)

    def open(self, **kwargs):
        """open is called when transitioning into the scene.
        """
        self.actor = kwargs.get("actor", None)
        # TODO: Basically here display all actor information, like all
        # attributes and all available skills.
