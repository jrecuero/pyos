import pygame
from pyplay import GObject, Color


class GameActorDisplay(GObject):
    def __init__(self, actor, x, y, dx, dy, **kwargs):
        super(GameActorDisplay, self).__init__("display-actor", x, y, dx, dy, **kwargs)
        self.actor = actor
        self.damage_color = Color.color_to_str(self.actor.get_damage_color())
        self.defense_color = Color.color_to_str(self.actor.get_defense_color())
        self.skill_color = Color.color_to_str(self.actor.get_skill_color())
        self.font = pygame.font.SysFont("Courier", 12, bold=True)
        self.health_surface = pygame.surface.Surface((50, 50))
        self.damage_surface = pygame.Surface((50, 50))
        self.defense_surface = pygame.Surface((50, 50))
        self.skill_surface = pygame.Surface((50, 50))
        self.text_actor = self.font.render(f"{self.actor.name}", True, self.color)
        # self.text_health = self.font.render(f"{self.actor.health}", True, Color.BLACK)
        # self.text_damage = self.font.render(f"{self.actor.damage}", True, Color.WHITE)
        # self.text_defense = self.font.render(f"{self.actor.defense}", True, Color.WHITE)
        # self.text_skill = self.font.render(f"{self.actor.skill}", True, Color.WHITE)
        # self.health_surface.fill((0, 255, 0, 0))
        # health_delta = (self.actor.health / self.actor.max_health) * 50
        # pygame.draw.rect(
        #     self.health_surface, (0, 255, 0, 0), (0, 0, 50, int(health_delta))
        # )
        # self.health_surface.blit(self.text_health, (0, 0, 50, 50))
        # self.damage_surface.fill(self.actor.get_damage_color())
        # self.damage_surface.blit(self.text_damage, (0, 0, 50, 50))
        # self.defense_surface.fill(self.actor.get_defense_color())
        # self.defense_surface.blit(self.text_defense, (0, 0, 50, 50))
        # self.skill_surface.fill(self.actor.get_skill_color())
        # self.skill_surface.blit(self.text_skill, (0, 0, 50, 50))
        # self.image.blit(self.health_surface, (0, 0, 50, 50))
        # self.image.blit(self.damage_surface, (50, 0, 50, 50))
        # self.image.blit(self.defense_surface, (100, 0, 50, 50))
        # self.image.blit(self.skill_surface, (150, 0, 50, 50))
        # self.image.blit(self.text_actor, (225, 20, self.dx, 100))

    def update(self, surface, **kwargs):
        self.text_actor = self.font.render(f"{self.actor.name}", True, self.color)
        self.image.fill((255, 255, 255, 0))
        self.text_health = self.font.render(f"{self.actor.health}", True, Color.BLACK)
        self.damage_surface.fill(self.actor.get_damage_color())
        self.text_damage = self.font.render(
            f"{self.actor.damage}/{self.actor.skill_colors[self.damage_color]}",
            True,
            Color.WHITE,
        )
        self.defense_surface.fill(self.actor.get_defense_color())
        self.text_defense = self.font.render(
            f"{self.actor.defense}/{self.actor.skill_colors[self.defense_color]}",
            True,
            Color.WHITE,
        )
        self.skill_surface.fill(self.actor.get_skill_color())
        self.text_skill = self.font.render(
            f"{self.actor.skill}/{self.actor.skill_colors[self.skill_color]}",
            True,
            Color.WHITE,
        )
        health_delta = (self.actor.health / self.actor.max_health) * 50
        self.health_surface.fill(Color.WHITE)
        pygame.draw.rect(
            self.health_surface, (0, 255, 0, 0), (0, 0, 50, int(health_delta))
        )
        pygame.draw.rect(self.health_surface, Color.BLACK, (0, 0, 50, 50), 1)
        self.health_surface.blit(self.text_health, (0, 0, 50, 50))
        self.damage_surface.blit(self.text_damage, (0, 0, 50, 50))
        self.defense_surface.blit(self.text_defense, (0, 0, 50, 50))
        self.skill_surface.blit(self.text_skill, (0, 0, 50, 50))
        self.image.blit(self.health_surface, (0, 0, 50, 50))
        self.image.blit(self.damage_surface, (50, 0, 50, 50))
        self.image.blit(self.defense_surface, (100, 0, 50, 50))
        self.image.blit(self.skill_surface, (150, 0, 50, 50))
        self.image.blit(self.text_actor, (225, 20, self.dx, 100))
