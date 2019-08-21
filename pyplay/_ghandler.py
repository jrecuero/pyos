class SceneHandler:
    """SceneHandler is a private class to be used by GameHandler in order to
    handle all scenes in the app.
    SceneHandler allows to handle scene, moving from one to other in an
    idenpendant way.
    """

    def __init__(self, **kwargs):
        self.scenes = []
        self.iactive = None

    def active(self, scene=None):
        """active sets the given scene as the active one. If no scene is given
        sets the first scene as the active one.
        """
        if scene is None:
            self.iactive = 0
        elif scene in self.scenes:
            self.iactive = self.scenes.index(scene)

    def enable(self, scene=None):
        """enable sets the given scene as enable. If no scene is given sets
        the active scene as enable.
        """
        if scene is None:
            if self.iactive is not None:
                self.scenes[self.iactive].enable = True
        else:
            scene.enable = True

    def disable(self, scene=None):
        """disable sets the given scene as disable. if no scene is given sets
        the active scene as disable.
        """
        if scene is None:
            if self.iactive is not None:
                self.scenes[self.iactive].enable = False
        else:
            scene.enable = False

    def visible(self, scene=None):
        """visible sets the given scene as visible. if no scene is given sets
        the active scene as visible.
        """
        if scene is None:
            if self.iactive is not None:
                self.scenes[self.iactive].visible = True
        else:
            scene.visible = True

    def hidden(self, scene=None):
        """hidden sets the given scene as not visible. if no scene is given
        sets the active scene as not visible.
        """
        if scene is None:
            if self.iactive is not None:
                self.scenes[self.iactive].visible = False
        else:
            scene.visible = False

    def add(self, scene):
        """add adds a new scene.
        """
        self.scenes.append(scene)

    def delete(self, scene):
        """delete deletes an existing scene.
        """
        if scene in self.scenes:
            self.scenes.remove(scene)

    def scene(self):
        """scene returns the active scene.
        """
        if self.iactive is not None and self.scenes:
            return self.scene[self.iactive]

    def next(self):
        """next moves to the next available scene. close will be called for
        the old active  scene and open will be called for the new active
        scene.
        """
        if self.iactive is not None and self.scenes:
            self.scenes[self.iactive].close()
            self.iactive = (self.iactive + 1) % len(self.scenes)
            self.scenes[self.iactive].open()

    def prev(self):
        """prev moves to the previous available scene. close will be called for
        the old active  scene and open will be called for the new active
        scene.
        """
        if self.iactive is not None and self.scenes:
            self.scenes[self.iactive].close()
            self.iactive = abs(self.iactive - 1) % len(self.scenes)
            self.scenes[self.iactive].open()

    def first(self):
        """first moves to the first available scene. close will be called for
        the old active  scene and open will be called for the new active
        scene.
        """
        if self.iactive is not None and self.scenes:
            self.scenes[self.iactive].close()
            self.iactive = 0
            self.scenes[self.iactive].open()

    def last(self):
        """last moves to the last available scene. close will be called for
        the old active  scene and open will be called for the new active
        scene.
        """
        if self.iactive is not None and self.scenes:
            self.scenes[self.iactive].close()
            self.iactive = len(self.scences) - 1
            self.scenes[self.iactive].open()


class GameHandler:
    """GameHandler controls all scenes in the app. Any scene has to be
    registered to the game handler, as any other global instance that is
    scene independent.
    GameHandler will be in charge to call update and render methods for
    all those instances (scenes and any other app global instance).
    """

    def __init__(self, name, surface, **kwargs):
        self.name = name
        self.surface = surface
        self.hscene = SceneHandler()
        self.gobjects = []
        self.timers = []

    def update(self, **kwargs):
        """update calls update method for all scenes and  graphical objects.
        """
        for scene in self.hscene.scenes:
            scene.update(**kwargs)
        for gobj in self.gobjects:
            gobj.update(self.surface, **kwargs)

    def render(self, **kwargs):
        """render calls render method for all scenes and graphical objects.
        """
        for scene in self.hscene.scenes:
            scene.render(**kwargs)
        for gobj in self.gobjects:
            gobj.render(self.surface, **kwargs)
