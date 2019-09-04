import pygame
from pyplay import Color, GEvent


class GameSkillType:
    """GameSkillType represents the type of skill action to be executed.
    """

    NONE = 0
    DAMAGE = 1
    HEAL = 1
    DEFENSE = 2


class GameSkillAction:
    """GameSkillAction represents attributes for a game skill.
    """

    def __init__(self, name, source, target, damage, type, **kwargs):
        self.name = name
        self.source = source
        self.target = target
        self.damage = damage
        self.type = type


class GameSkill:
    """GameSkill implements any skill usable by any actor in the game.
    """

    def __init__(self, name, color, threshold, **kwargs):
        self.name = name
        self.color = color
        self.color_str = Color.color_to_str(color)
        self.threshold = threshold

    def can_run(self, source):
        """can_run checks if the skill is available to be executed.
        """
        colors = source.skill_colors[self.color_str]
        return colors > self.threshold

    def action(self, source, target):
        """can_run checks if the skill is available to be executed.
        """
        pass

    def clean_up_event(self, source, target, **kwargs):
        """cleaun_up_event sends the clean up event to the handler.
        """
        GEvent.handler_event(
            GEvent.SKILL, action=self.clean_up(source, target), args=(), **kwargs
        )


class GameSkillHeal(GameSkill):
    def __init__(self, color, **kwargs):
        super(GameSkillHeal, self).__init__("heal", color, 25, **kwargs)

    def action(self, source, target):
        """can_run checks if the skill is available to be executed.
        """
        if self.can_run(source):
            target.health += 10
            source.skill_colors[self.color_str] -= self.threshold


class GameSkillGreatHeal(GameSkill):
    def __init__(self, color, **kwargs):
        super(GameSkillGreatHeal, self).__init__("great-heal", color, 100, **kwargs)

    def action(self, source, target):
        """can_run checks if the skill is available to be executed.
        """
        if self.can_run(source):
            target.health += 50
            source.skill_colors[self.color_str] -= self.threshold


class GameSkillMegaHeal(GameSkill):
    def __init__(self, color, **kwargs):
        super(GameSkillMegaHeal, self).__init__("mega-heal", color, 250, **kwargs)

    def action(self, source, target):
        """can_run checks if the skill is available to be executed.
        """
        if self.can_run(source):
            target.health += 500
            source.skill_colors[self.color_str] -= self.threshold


class GameSkillDefenseUp(GameSkill):
    def __init__(self, color, **kwargs):
        super(GameSkillDefenseUp, self).__init__("defense-up", color, 50, **kwargs)

    def action(self, source, target):
        """can_run checks if the skill is available to be executed.
        """
        if self.can_run(source):
            target._defense.add_buff(1)
            source.skill_colors[self.color_str] -= self.threshold
            self.clean_up_event(source, target, tick={"lines": 5})

    def clean_up(self, source, target):
        def _clean_up():
            target._defense.del_buff(1)

        return _clean_up


class GameSkillDamageUp(GameSkill):
    def __init__(self, color, **kwargs):
        super(GameSkillDamageUp, self).__init__("damage-up", color, 100, **kwargs)

    def action(self, source, target):
        """can_run checks if the skill is available to be executed.
        """
        if self.can_run(source):
            target._damage.add_buff(1)
            source.skill_colors[self.color_str] -= self.threshold
            self.clean_up_event(source, target, tick={"lines": 5})

    def clean_up(self, source, target):
        def _clean_up():
            target._damage.del_buff(1)
            print("clean up")

        return _clean_up
