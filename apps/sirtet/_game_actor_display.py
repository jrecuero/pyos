import pygame
from pyplay import GObject, Color


class GameActorDisplay(GObject):
    """GameActorDisplay implements the graphical object that displays all
    actor information in any scene.
    """

    def __init__(self, actor, x, y, dx, dy, **kwargs):
        super(GameActorDisplay, self).__init__("display-actor", x, y, dx, dy, **kwargs)
        self.actor = actor
        self.damage_color = Color.color_to_str(self.actor.get_damage_color())
        self.defense_color = Color.color_to_str(self.actor.get_defense_color())
        self.mind_color = Color.color_to_str(self.actor.get_mind_color())
        self.font = pygame.font.SysFont("Courier", 12, bold=True)
        self.surface_health = pygame.surface.Surface((50, 50))
        self.surface_damage = pygame.Surface((50, 50))
        self.surface_defense = pygame.Surface((50, 50))
        self.surface_mind = pygame.Surface((50, 50))
        self.surface_damage_skills = pygame.Surface((50, 50))
        self.surface_defense_skills = pygame.Surface((50, 50))
        self.surface_mind_skills = pygame.Surface((150, 50))

    def update(self, surface, **kwargs):
        """update calls update method for all scenes and  graphical objects.
        """
        text_pos = (10, 10, 50, 50)
        self.text_actor = self.font.render(
            f"[{self.actor.level}] {self.actor.name}", True, self.color
        )
        self.image.fill((255, 255, 255, 0))
        self.text_health = self.font.render(f"{self.actor.health}", True, Color.BLACK)
        self.surface_damage.fill(self.actor.get_damage_color())
        self.text_damage = self.font.render(
            f"{self.actor.damage}/{self.actor.skill_colors[self.damage_color]}",
            True,
            Color.WHITE,
        )
        self.surface_defense.fill(self.actor.get_defense_color())
        self.text_defense = self.font.render(
            f"{self.actor.defense}/{self.actor.skill_colors[self.defense_color]}",
            True,
            Color.WHITE,
        )
        self.surface_mind.fill(self.actor.get_mind_color())
        self.text_mind = self.font.render(
            f"{self.actor.mind}/{self.actor.skill_colors[self.mind_color]}",
            True,
            Color.WHITE,
        )
        health_delta = (self.actor.health / self.actor.max_health) * 50
        self.surface_health.fill(Color.WHITE)
        pygame.draw.rect(
            self.surface_health, (0, 255, 0, 0), (0, 0, 50, int(health_delta))
        )
        pygame.draw.rect(self.surface_health, Color.BLACK, (0, 0, 50, 50), 1)

        for skill in self.actor.damage_skills:
            color = skill.color
            self.surface_damage_skills.fill((color))
            damage_skill_text = self.font.render(
                f"{skill.threshold}", True, Color.WHITE
            )
            self.surface_damage_skills.blit(damage_skill_text, text_pos)
            if skill.can_run(self.actor):
                pygame.draw.rect(
                    self.surface_damage_skills, (0, 255, 0), (0, 0, 50, 50), 5
                )
            else:
                pygame.draw.rect(
                    self.surface_damage_skills, Color.BLACK, (0, 0, 50, 50), 5
                )
        for skill in self.actor.defense_skills:
            color = skill.color
            self.surface_defense_skills.fill(color)
            defense_skill_text = self.font.render(
                f"{skill.threshold}", True, Color.WHITE
            )
            self.surface_defense_skills.blit(defense_skill_text, text_pos)
            if skill.can_run(self.actor):
                pygame.draw.rect(
                    self.surface_defense_skills, (0, 255, 0), (0, 0, 50, 50), 5
                )
            else:
                pygame.draw.rect(
                    self.surface_defense_skills, Color.BLACK, (0, 0, 50, 50), 5
                )
        start_x = 0
        for index, skill in enumerate(self.actor.mind_skills):
            color = skill.color
            if index == 0:
                self.surface_mind_skills.fill(color)
            skill_skill_text = self.font.render(f"{skill.threshold}", True, Color.WHITE)
            self.surface_mind_skills.blit(skill_skill_text, (start_x + 10, 10, 50, 50))
            if skill.can_run(self.actor):
                pygame.draw.rect(
                    self.surface_mind_skills, (0, 255, 0), (start_x, 0, 50, 50), 5
                )
            else:
                pygame.draw.rect(
                    self.surface_mind_skills, Color.BLACK, (start_x, 0, 50, 50), 5
                )
            start_x += 50

        self.surface_health.blit(self.text_health, text_pos)
        self.surface_damage.blit(self.text_damage, text_pos)
        self.surface_defense.blit(self.text_defense, text_pos)
        self.surface_mind.blit(self.text_mind, text_pos)
        self.image.blit(self.text_actor, (0, 20, self.dx, 100))
        self.image.blit(self.surface_health, (100, 0, 50, 50))
        self.image.blit(self.surface_damage, (150, 0, 50, 50))
        self.image.blit(self.surface_defense, (200, 0, 50, 50))
        self.image.blit(self.surface_mind, (250, 0, 50, 50))
        self.image.blit(self.surface_damage_skills, (350, 0, 50, 50))
        self.image.blit(self.surface_defense_skills, (400, 0, 50, 50))
        self.image.blit(self.surface_mind_skills, (450, 0, 50, 50))

    def handle_mouse_event(self, event):
        """handle_mouse_event should process the mouse event given.
        Mouse events are passed to the active scene to be handle.
        """
        # if self.rect.collidepoint(pygame.mouse.get_pos()):
        #     print(f"mouse {pygame.mouse.get_pos()} is over me {self}")
        pass
