import pygame


class Scene:
    """Scene class identifies a pyplay scene. A scene can contain multiple
    elements like boards, objects, ...
    Scene will handle all those instances, calling proper update and render
    for each of them.
    """

    __GID = 0

    def __init__(self, name, surface, **kwargs):
        Scene.__GID += 1
        self.__gid = Scene.__GID
        self.name = name
        self.surface = surface
        self.gobjects = pygame.sprite.Group()
        self.timers = []
        self.enable = kwargs.get("enable", True)
        self.visible = kwargs.get("visible", True)

    @property
    def gid(self):
        return self.__gid

    def __str__(self):
        return f"[{self.gid}] : {self.__class__.__name__}@{self.name}"

    def add_gobject(self, gobject):
        """add_gobject adds a graphical object to the scene.
        """
        self.gobjects.add(gobject)

    def del_gobject(self, gobject):
        """del_gobject deletes a graphical object from the scene.
        """
        if gobject in self.gobjects:
            self.gobjects.remove(gobject)

    def open(self, **kwargs):
        """open is called when transitioning into the scene.
        """
        pass

    def close(self, **kwargs):
        """close is called when transitioning out of the scene.
        """
        pass

    def handle_custom_events(self):
        """handle_custom_events should process all pygame custom events. Any
        object in the game, like, scene, graphic objects, ... can post
        customs events, and those should be handled at this time.
        """
        pass

    def handle_these_events(self, events):
        """handle_these_events should process the given list of events. That
        list can contains custom or pygame events.
        """
        pass

    def handle_these_custom_events(self, events):
        """handle_these_custom_events should process the given list of custom
        events.
        """
        pass

    def handle_keyboard_event(self, event):
        """handle_keyboard_event should process the keyboard event given.
        """
        for gobj in self.gobjects:
            gobj.handle_keyboard_event(event)

    def handle_custom_event(self, event):
        """handle_custom_event should process pygame custom event given.
        Any object in the game, like, scene, graphic objects, ... can post
        customs events, and those should be handled at this time.
        """
        for gobj in self.gobjects:
            gobj.handle_custom_event(event)

    def update(self, **kwargs):
        """update calls update method for all scene graphical objects.
        """
        self.gobjects.update(self.surface)

    def render(self, **kwargs):
        """render calls render method for all scene graphical objects.
        """
        self.gobjects.draw(self.surface)
        for gobj in self.gobjects:
            gobj.render(self.surface, **kwargs)
