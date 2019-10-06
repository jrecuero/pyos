from pyplay import Scene


class GameSceneMain(Scene):
    """GameSceneMain implements the game main scene. Main scene should display
    all attributes from the main actor, any skill to be selected or upgraded
    and the next scene to be played.
    """

    def __init__(self, surface, **kwargs):
        super(GameSceneMain, self).__init__("game main", surface, **kwargs)

    def open(self, **kwargs):
        """open is called when transitioning into the scene.
        """
        self.actor = kwargs.get("actor", None)
        # TODO: Basically here display all actor information, like all
        # attributes and all available skills.
