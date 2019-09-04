# import pygame
from pyplay import Color, GEvent
from _game_level import GameLevel


# class GameSkillType:
#     """GameSkillType represents the type of skill action to be executed.
#     """
#
#     NONE = 0
#     DAMAGE = 1
#     HEAL = 1
#     DEFENSE = 2


# class GameSkillAction:
#     """GameSkillAction represents attributes for a game skill.
#     """
#
#     def __init__(self, name, source, target, damage, type, **kwargs):
#         self.name = name
#         self.source = source
#         self.target = target
#         self.damage = damage
#         self.type = type


class GameSkill:
    """GameSkill implements any skill usable by any actor in the game.
    Skills are available for any actor for any match. There is start() method
    that initializes the skill to be used in the match and an end() method
    that proceeds to clean up the skill after the match has ended.
    """

    def __init__(self, name, color, threshold, **kwargs):
        self.name = name
        self.color = color
        self.color_str = Color.color_to_str(color)
        self.threshold = threshold
        self.glevel = GameLevel()
        self._target = "self"

    def target(self, source, target):
        """target returns if skill target is 'self' or 'target'.
        """
        if self.target == "self":
            return source
        else:
            return target

    def can_run(self, source):
        """can_run checks if the skill is available to be executed.
        """
        colors = source.skill_colors[self.color_str]
        return colors > self.threshold

    def start(self, source=None):
        """start sets up the skill to be used in a match.
        """
        pass

    def end(self, source=None):
        """end cleans up anything related with the skill at the end of the
        match.
        """
        pass

    def action(self, source, target):
        """can_run checks if the skill is available to be executed.
        """
        pass

    def clean_up(self, source, target):
        """clean_up proceeds to reverse any action triggered by the skill.
        """
        pass

    def clean_up_event(self, source, target, **kwargs):
        """cleaun_up_event sends the clean up event to the handler.
        """
        GEvent.handler_event(
            GEvent.SKILL, action=self.clean_up(source, target), args=(), **kwargs
        )


class GameSkillBlowColor(GameSkill):
    def __init__(self, color, blow_color, **kwargs):
        super(GameSkillBlowColor, self).__init__("blow-color", color, 10, **kwargs)
        self.blow_color = blow_color

    def action(self, source, target):
        """can_run checks if the skill is available to be executed.
        """
        if self.can_run(source):
            source.skill_colors[self.color_str] -= self.threshold
            GEvent.board_event(
                GEvent.SKILL, action="blow-color", args=(self.blow_color,)
            )


class GameSkillBlowEmpty(GameSkill):
    def __init__(self, color, **kwargs):
        super(GameSkillBlowEmpty, self).__init__("blow-color", color, 10, **kwargs)

    def action(self, source, target):
        """can_run checks if the skill is available to be executed.
        """
        if self.can_run(source):
            source.skill_colors[self.color_str] -= self.threshold
            GEvent.board_event(GEvent.SKILL, action="blow-empty", args=())


class GameSkillCopyColor(GameSkill):
    def __init__(self, color, from_color, to_color, **kwargs):
        super(GameSkillCopyColor, self).__init__("copy-color", color, 10, **kwargs)
        self.from_color = from_color
        self.to_color = to_color

    def action(self, source, target):
        """can_run checks if the skill is available to be executed.
        """
        if self.can_run(source):
            source.skill_colors[self.color_str] -= self.threshold
            GEvent.board_event(
                GEvent.SKILL, action="copy-color", args=(self.from_color, self.to_color)
            )


class GameSkillColorToEmpty(GameSkill):
    def __init__(self, color, from_color, **kwargs):
        super(GameSkillColorToEmpty, self).__init__(
            "color-to-empty", color, 10, **kwargs
        )
        self.from_color = from_color

    def action(self, source, target):
        """can_run checks if the skill is available to be executed.
        """
        if self.can_run(source):
            source.skill_colors[self.color_str] -= self.threshold
            GEvent.board_event(
                GEvent.SKILL, action="color-to-empty", args=(self.from_color,)
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
        """clean_up proceeds to reverse any action triggered by the skill.
        """

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
        """clean_up proceeds to reverse any action triggered by the skill.
        """

        def _clean_up():
            target._damage.del_buff(1)

        return _clean_up


class GameSkillSkillUp(GameSkill):
    def __init__(self, color, **kwargs):
        super(GameSkillSkillUp, self).__init__("skill-up", color, 100, **kwargs)

    def action(self, source, target):
        """can_run checks if the skill is available to be executed.
        """
        if self.can_run(source):
            target._skill.add_buff(1)
            source.skill_colors[self.color_str] -= self.threshold
            self.clean_up_event(source, target, tick={"lines": 5})

    def clean_up(self, source, target):
        """clean_up proceeds to reverse any action triggered by the skill.
        """

        def _clean_up():
            target._skill.del_buff(1)

        return _clean_up


class GameSkillDamageBuffUp(GameSkill):
    def __init__(self, color, **kwargs):
        super(GameSkillDamageBuffUp, self).__init__(
            "damage-buff-up", color, 50, **kwargs
        )

    def action(self, source, target):
        """can_run checks if the skill is available to be executed.
        """
        if self.can_run(source):
            target.damage_buffs.append(1)
            source.skill_colors[self.color_str] -= self.threshold
            self.clean_up_event(source, target, tick={"lines": 5})

    def clean_up(self, source, target):
        """clean_up proceeds to reverse any action triggered by the skill.
        """

        def _clean_up():
            target.damage_buffs.remove(1)

        return _clean_up


class GameSkillDefenseBuffUp(GameSkill):
    def __init__(self, color, **kwargs):
        super(GameSkillDefenseBuffUp, self).__init__(
            "defense-buff-up", color, 50, **kwargs
        )

    def action(self, source, target):
        """can_run checks if the skill is available to be executed.
        """
        if self.can_run(source):
            target.defense_buffs.append(1)
            source.skill_colors[self.color_str] -= self.threshold
            self.clean_up_event(source, target, tick={"lines": 5})

    def clean_up(self, source, target):
        """clean_up proceeds to reverse any action triggered by the skill.
        """

        def _clean_up():
            target.defense_buffs.remove(1)

        return _clean_up


class GameSkillSkillBuffUp(GameSkill):
    def __init__(self, color, **kwargs):
        super(GameSkillSkillBuffUp, self).__init__("skill-buff-up", color, 50, **kwargs)

    def action(self, source, target):
        """can_run checks if the skill is available to be executed.
        """
        if self.can_run(source):
            target.skill_buffs.append(1)
            source.skill_colors[self.color_str] -= self.threshold
            self.clean_up_event(source, target, tick={"lines": 5})

    def clean_up(self, source, target):
        """clean_up proceeds to reverse any action triggered by the skill.
        """

        def _clean_up():
            target.skill_buffs.remove(1)

        return _clean_up


class GameSkillRawDamage(GameSkill):
    def __init__(self, color, **kwargs):
        super(GameSkillRawDamage, self).__init__("raw-damage", color, 25, **kwargs)
        self._target = "target"

    def action(self, source, target):
        """can_run checks if the skill is available to be executed.
        """
        if self.can_run(source):
            target.health -= 10
            source.skill_colors[self.color_str] -= self.threshold
