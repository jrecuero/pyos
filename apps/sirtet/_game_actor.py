import pygame
from pyplay import Gid, GObject, Color
from _game_actor_attr import GameActorAttr
from _game_actor_stats import GameActorStats


class GameDisplayActor(GObject):
    def __init__(self, actor, x, y, dx, dy, **kwargs):
        super(GameDisplayActor, self).__init__("display-actor", x, y, dx, dy, **kwargs)
        self.actor = actor
        self.font = pygame.font.SysFont("Courier", 18)
        self.health_surface = pygame.surface.Surface((50, 50))
        self.damage_surface = pygame.Surface((50, 50))
        self.defense_surface = pygame.Surface((50, 50))
        self.skill_surface = pygame.Surface((50, 50))
        self.text_actor = self.font.render(f"{self.actor.name}", True, self.color)
        self.text_health = self.font.render(f"{self.actor.health}", True, Color.BLACK)
        self.text_damage = self.font.render(f"{self.actor.damage}", True, Color.WHITE)
        self.text_defense = self.font.render(f"{self.actor.defense}", True, Color.WHITE)
        self.text_skill = self.font.render(f"{self.actor.skill}", True, Color.WHITE)
        # self.health_surface.fill((0, 255, 0, 0))
        # health_delta = (self.actor.health / self.actor.max_health) * 50
        # pygame.draw.rect(
        #     self.health_surface, (0, 255, 0, 0), (0, 0, 50, int(health_delta))
        # )
        # self.health_surface.blit(self.text_health, (0, 0, 50, 50))
        self.damage_surface.fill(self.actor.get_damage_color())
        self.damage_surface.blit(self.text_damage, (0, 0, 50, 50))
        self.defense_surface.fill(self.actor.get_defense_color())
        self.defense_surface.blit(self.text_defense, (0, 0, 50, 50))
        self.skill_surface.fill(self.actor.get_skill_color())
        self.skill_surface.blit(self.text_skill, (0, 0, 50, 50))
        # self.image.blit(self.health_surface, (0, 0, 50, 50))
        # self.image.blit(self.damage_surface, (50, 0, 50, 50))
        # self.image.blit(self.defense_surface, (100, 0, 50, 50))
        # self.image.blit(self.skill_surface, (150, 0, 50, 50))
        # self.image.blit(self.text_actor, (225, 20, self.dx, 100))

    def update(self, surface, **kwargs):
        self.text_actor = self.font.render(f"{self.actor.name}", True, self.color)
        self.image.fill((255, 255, 255, 0))
        self.text_health = self.font.render(f"{self.actor.health}", True, Color.BLACK)
        health_delta = (self.actor.health / self.actor.max_health) * 50
        self.health_surface.fill(Color.WHITE)
        pygame.draw.rect(
            self.health_surface, (0, 255, 0, 0), (0, 0, 50, int(health_delta))
        )
        pygame.draw.rect(self.health_surface, Color.BLACK, (0, 0, 50, 50), 1)
        self.health_surface.blit(self.text_health, (0, 0, 50, 50))
        self.image.blit(self.health_surface, (0, 0, 50, 50))
        self.image.blit(self.damage_surface, (50, 0, 50, 50))
        self.image.blit(self.defense_surface, (100, 0, 50, 50))
        self.image.blit(self.skill_surface, (150, 0, 50, 50))
        self.image.blit(self.text_actor, (225, 20, self.dx, 100))


class GameActor(Gid):
    """GameActor implements any actor in the game.
    """

    def __init__(self, name, **kwargs):
        super(GameActor, self).__init__()
        self.name = name
        self._health = GameActorAttr("health", kwargs.get("health", 0))
        self._damage = GameActorAttr("damage", kwargs.get("damage", 0))
        self._defense = GameActorAttr("defense", kwargs.get("defense", 0))
        self._skill = GameActorAttr("skill", kwargs.get("skill", 0))
        self.stats = GameActorStats()
        self.play_stats = {"damage": None, "defense": None, "skill": None}

    @property
    def health(self):
        return self._health.real

    @health.setter
    def health(self, value):
        self._health.real = value

    @property
    def damage(self):
        return self._damage.real

    @damage.setter
    def damage(self, value):
        self._damage.real = value

    @property
    def defense(self):
        return self._defense.real

    @defense.setter
    def defense(self, value):
        self._defense.real = value

    @property
    def skill(self):
        return self._skill.real

    @skill.setter
    def skill(self, value):
        self._skill.real = value

    @property
    def max_health(self):
        return self._health.max

    @max_health.setter
    def max_health(self, value):
        self._health.max = value
        self._health.real = value

    @property
    def max_damage(self):
        return self._damage.max

    @max_damage.setter
    def max_damage(self, value):
        self._damage.max = value
        self._damage.real = value

    @property
    def max_defense(self):
        return self._defense.max

    @max_defense.setter
    def max_defense(self, value):
        self._defense.max = value
        self._defense.real = value

    @property
    def max_skill(self):
        return self._skill.max

    @max_skill.setter
    def max_skill(self, value):
        self._skill.max = value
        self._skill.real = value

    def __str__(self):
        return f"[{self.gid}] : {self.__class__.__name__}@{self.name} | {self.health.real} {self.damage.real} {self.defense.real} {self.skill.real}"

    def gdisplay(self):
        return GameDisplayActor(self, 0, 0, 600, 200)

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
        return self.damage.real * value

    def defense_for(self, value):
        return self.defense.real * value

    def skill_for(self, value):
        return self.skill.real * value
