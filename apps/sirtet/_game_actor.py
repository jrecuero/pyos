import pygame
from pyplay import Gid, GObject
from _game_actor_stats import GameActorStats


class GameDisplayActor(GObject):
    def __init__(self, actor, x, y, dx, dy, **kwargs):
        super(GameDisplayActor, self).__init__("display-actor", x, y, dx, dy, **kwargs)
        self.actor = actor
        self.font = pygame.font.SysFont("Courier", 18)
        self.text_actor = self.font.render(f"{actor}", True, self.color)
        self.image.blit(self.text_actor, (0, 20, dx, 100))

    def update(self, surface, **kwargs):
        self.text_actor = self.font.render(f"{self.actor}", True, self.color)
        self.image.fill((255, 255, 255, 0))
        self.image.blit(self.text_actor, (0, 20, self.dx, 100))


class GameActor(Gid):
    """GameActor implements any actor in the game.
    """

    def __init__(self, name, **kwargs):
        super(GameActor, self).__init__()
        self.name = name
        self._health = kwargs.get("health", 0)
        self._damage = kwargs.get("damage", 0)
        self._defense = kwargs.get("defense", 0)
        self._skill = kwargs.get("skill", 0)
        self.stats = GameActorStats()
        self.play_stats = {"damage": None, "defense": None, "skill": None}
        # self.gtext = GameDisplayActor(self, 0, 0, 400, 200)
        self.gtext = None

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        self._health = value

    @property
    def damage(self):
        return self._damage

    @damage.setter
    def damage(self, value):
        self._damage = value

    @property
    def defense(self):
        return self._defense

    @defense.setter
    def defense(self, value):
        self._defense = value

    @property
    def skill(self):
        return self._skill

    @skill.setter
    def skill(self, value):
        self._skill = value

    def __str__(self):
        return f"[{self.gid}] : {self.__class__.__name__}@{self.name} | {self.health} {self.damage} {self.defense} {self.skill}"

    def gdisplay(self):
        self.gtext = GameDisplayActor(self, 0, 0, 400, 200)
        return self.gtext

    def set_play_damage(self, color):
        self.play_stats["damage"] = color

    def set_play_defense(self, color):
        self.play_stats["defense"] = color

    def set_play_skill(self, color):
        self.play_stats["skill"] = color

    def get_damage_color(self):
        return self.play_stats["damage"]

    def get_defense_color(self):
        return self.play_stats["defense"]

    def get_skill_color(self):
        return self.play_stats["skill"]

    def damage_for(self, value):
        return self.damage * value

    def defense_for(self, value):
        return self.defense * value

    def skill_for(self, value):
        return self.skill * value
