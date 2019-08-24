from ._hscene import SceneHandler


class GHandler:
    """GHandler controls all scenes in the app. Any scene has to be
    registered to the game handler, as any other global instance that is
    scene independent.
    GHandler will be in charge to call update and render methods for
    all those instances (scenes and any other app global instance).
    """

    def __init__(self, name, surface, **kwargs):
        self.name = name
        self.surface = surface
        self.hscene = SceneHandler()
        self.gobjects = []
        self.timers = []

    def add_gobject(self, gobject):
        """add_gobject adds a graphical object to the game handler.
        """
        self.gobjects.append(gobject)

    def del_gobject(self, gobject):
        """del_gobject deletes a graphical object from the game handler.
        """
        if gobject in self.gobjects:
            self.gobjects.remove(gobject)

    def add_scene(self, scene):
        """add_scene adds an scene to the game handler.
        """
        self.hscene.add(scene)

    def del_scene(self, scene):
        """del_scene deletes an scene from the game handler.
        """
        self.hscene.delete(scene)

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
        Keyboard events are passed to the active scene to be handle.
        """
        self.hscene.handle_keyboard_event(event)

    def update(self, **kwargs):
        """update calls update method for all scenes and  graphical objects.
        """
        # call only the active scene.
        self.hscene.update(**kwargs)
        for gobj in self.gobjects:
            gobj.update(self.surface, **kwargs)

    def render(self, **kwargs):
        """render calls render method for all scenes and graphical objects.
        """
        # call only the active scene.
        self.hscene.render(**kwargs)
        for gobj in self.gobjects:
            gobj.render(self.surface, **kwargs)
