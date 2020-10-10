import pygame
from pyplay import GObject


class GameActorSheet(GObject):
    """GameActorSheet implements the graphical object that displays all
    actor information in the main scene.
    """

    def __init__(self, actor, x, y, dx, dy, **kwargs):
        super(GameActorSheet, self).__init__(actor.name, x, y, dx, dy, **kwargs)
        self.actor = actor
        self.font = pygame.font.SysFont("Courier", 12, bold=True)

    def update(self, surface, **kwargs):
        """update calls update method for all scenes and  graphical objects.
        """
        pass
