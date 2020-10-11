import pygame
from ._color import Color
from ._gobject import GDummy


class GCanvas(GDummy):
    """GCanvas class identifies a graphic canvas containing sprites to be
    displayed
    """

    def __init__(self, name, x, y, dx, dy, nlayers, **kwargs):
        """__init__ method initializes a GCanvas instance.

        Args:
            name (type): Description of parameter `name`.
            x (int): canvas X-axis position.
            y (int): canvas Y-axis position.
            dx (int): sanvas width.
            dy (int): canvas height.
            nlayers (int): canvas number of layers.
            **kwargs (dict): canvas custom arguments.
        """
        super(GCanvas, self).__init__(name, x, y, dx, dy, **kwargs)
        self.number_layers = nlayers
        self.glayers = [pygame.sprite.LayeredUpdates() for _ in range(nlayers)]
        self.image = pygame.Surface((self.dx, self.dy), pygame.SRCALPHA)
        self.running = True

    def __str__(self):
        """__str__ method display GCanvas instance as a string.

        Returns:
            str: string with Canvas instance information.

        """
        return f"[{self.gid}] : {self.__class__.__name__} ({self.x}, {self.y}) ({self.dx. self.dy})"

    def add_gobject(self, gobject, layer):
        if 0 <= layer < self.number_layers:
            self.glayers[layer].add(gobject)
        return False

    def handle_keyboard_event(self, event, **kwargs):
        if self.running:
            for layer in self.glayers[::-1]:
                for sprite in layer.sprites():
                    sprite.handle_keyboard_event(event, **kwargs)

    def handle_mouse_event(self, event, **kwargs):
        if self.running:
            for layer in self.glayers[::-1]:
                for sprite in layer.sprites():
                    sprite.handle_mouse_event(event, **kwargs)

    def handle_custom_event(self, event, **kwargs):
        if self.running:
            for layer in self.glayers[::-1]:
                for sprite in layer.sprites():
                    sprite.handle_custom_event(event, **kwargs)

    def update(self, surface, **kwargs):
        if self.running:
            for layer in self.glayers[::-1]:
                for sprite in layer.sprites():
                    sprite.update(surface, **kwargs)

    def render(self, surface, **kwargs):
        """render method draws canvas instance in the given surface.

        Args:
            surface (Surface): pygame Surface where canvas will be drew.
            **kwargs (dict): render custom arguments

        Returns:
            None: no return value.

        """
        for layer in range(self.number_layers - 1, 0, -1):
            self.image.fill(Color.WHITE)
            self.glayers[layer].draw(self.image)
            surface.blit(self.image, (self.x, self.y))
