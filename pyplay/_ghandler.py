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
        self.running = True

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

    def start_tick(self):
        """start_tick should set all elements ready for a new tick.
        """
        self.hscene.start_tick()

    def end_tick(self):
        """end_tick shoudl set all elements ready for the end of a tick. Any
        structure to be clean up can be done at this point.
        """
        self.hscene.end_tick()

    def handle_custom_event(self, event):
        """handle_custom_event should process pygame custom event given.
        Any object in the game, like, scene, graphic objects, ... can post
        customs events, and those should be handled at this time.
        """
        self.hscene.handle_custom_event(event)

    def handle_keyboard_event(self, event):
        """handle_keyboard_event should process the keyboard event given.
        Keyboard events are passed to the active scene to be handle.
        """
        self.hscene.handle_keyboard_event(event)

    def handle_mouse_event(self, event):
        """handle_mouse_event should process the mouse event given.
        Mouse events are passed to the active scene to be handle.
        """
        self.hscene.handle_mouse_event(event)

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
