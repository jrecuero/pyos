class Scene:
    """Scene class identifies a pyplay scene. A scene can contain multiple
    elements like boards, objects, ...
    Scene will handle all those instances, calling proper update and render
    for each of them.
    """

    def __init__(self, name, surface, **kwargs):
        self.name = name
        self.surface = surface
        self.gobjects = []
        self.timers = []
        self.enable = kwargs.get("enable", True)
        self.visible = kwargs.get("visible", True)

    def open(self, **kwargs):
        """open is called when transitioning into the scene.
        """
        pass

    def clos(self, **kwargs):
        """open is called when transitioning out of the scene.
        """
        pass

    def update(self, **kwargs):
        """update calls update method for all scene graphical objects.
        """
        for gobj in self.bobjects:
            gobj.update(self.surface, **kwargs)

    def render(self, **kwargs):
        """render calls render method for all scene graphical objects.
        """
        for gobj in self.gobjects:
            gobj.render(self.surface, **kwargs)
