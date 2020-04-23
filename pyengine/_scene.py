import pygame
from ._gid import Gid


class Scene(Gid):
    """Scene class identifies a pyplay scene. A scene can contain multiple
    elements like boards, objects, ...
    Scene will handle all those instances, calling proper update and render
    for each of them.
    """

    def __init__(self, name, surface, **kwargs):
        super(Scene, self).__init__()
        self.name = name
        self.surface = surface
        self.sprites = pygame.sprite.Group()
        self.gobjects = []
        self.timers = []
        self.enable = kwargs.get("enable", True)
        self.visible = kwargs.get("visible", True)

    def __str__(self):
        return f"[{self.gid}] : {self.__class__.__name__}@{self.name}"

    def add_sprite(self, sprite):
        """add_sprite adds a graphical object to the scene.
        """
        if sprite in self.sprites:
            raise Exception(f"sprite {sprite} already present in list")
        self.sprites.add(sprite)

    def del_sprite(self, sprite):
        """del_sprite deletes a graphical object from the scene.
        """
        if sprite in self.sprites:
            self.sprites.remove(sprite)

    def add_gobject(self, gobject):
        """add_gobject adds a graphical object to the scene.
        """
        if gobject in self.objects:
            raise Exception(f"object {object} already present in list")
        self.objects.add(object)

    def del_object(self, object):
        """del_object deletes a graphical object from the scene.
        """
        if object in self.objects:
            self.objects.remove(object)

    def open(self, **kwargs):
        """open is called when transitioning into the scene.
        """
        pass

    def close(self, **kwargs):
        """close is called when transitioning out of the scene.
        """
        pass

    def start_tick(self):
        """start_tick should set all elements ready for a new tick.
        """
        for sprite in self.sprites:
            sprite.start_tick()
        for gobj in self.gobjects:
            gobj.start_tick()

    def end_tick(self):
        """end_tick shoudl set all elements ready for the end of a tick. Any
        structure to be clean up can be done at this point.
        """
        for sprite in self.sprites:
            sprite.end_tick()
        for gobj in self.objects:
            gobj.end_tick()

    def handle_keyboard_event(self, event):
        """handle_keyboard_event should process the keyboard event given.
        """
        for sprite in self.sprites:
            sprite.handle_keyboard_event(event)
        for gobj in self.gobjects:
            gobj.handle_keyboard_event(event)

    def handle_mouse_event(self, event):
        """handle_mouse_event should process the mouse event given.
        Mouse events are passed to the active scene to be handle.
        """
        for sprite in self.sprites:
            sprite.handle_mouse_event(event)
        for gobj in self.gobjects:
            gobj.handle_mouse_event(event)

    def handle_custom_event(self, event):
        """handle_custom_event should process pygame custom event given.
        Any object in the game, like, scene, graphic objects, ... can post
        customs events, and those should be handled at this time.
        """
        for sprite in self.sprites:
            sprite.handle_custom_event(event)
        for gobj in self.objects:
            gobj.handle_custom_event(event)

    def update(self, **kwargs):
        """update calls update method for all scene graphical objects.
        """
        self.sprites.update(self.surface)
        self.gobjects.update(self.surface)

    def render(self, **kwargs):
        """render calls render method for all scene graphical objects.
        """
        self.sprites.draw(self.surface)

        for gobj in self.gobjects:
            gobj.render(self.surface, **kwargs)
