import os
import pygame
from pyplay import Color, GEvent
from _game_level import GameLevel


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
        self.expire = kwargs.get("expire", None)
        self.image = None

    def __str__(self):
        return f"{self.name} {self.color_str} {self.threshold} {self._target}"

    def target(self, source, target):
        """target returns if skill target is 'self' or 'target'.
        """
        return source if self._target == "self" else target

    def can_run(self, source):
        """can_run checks if the skill is available to be executed.
        """
        colors = source.counter_colors_available[self.color_str]
        return colors > self.threshold

    def start_match(self, source=None):
        """start_match sets up the skill to be used in a match.
        """
        pass

    def end_match(self, source=None):
        """end_match cleans up anything related with the skill at the end of
        the match.
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
            source.counter_colors_available[self.color_str] -= self.threshold
            GEvent.board_event(
                GEvent.SKILL, action="blow-color", args=(self.blow_color,)
            )


class GameSkillBlowEmpty(GameSkill):
    def __init__(self, color, **kwargs):
        super(GameSkillBlowEmpty, self).__init__("blow-color", color, 250, **kwargs)

    def action(self, source, target):
        """can_run checks if the skill is available to be executed.
        """
        if self.can_run(source):
            source.counter_colors_available[self.color_str] -= self.threshold
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
            source.counter_colors_available[self.color_str] -= self.threshold
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
            source.counter_colors_available[self.color_str] -= self.threshold
            GEvent.board_event(
                GEvent.SKILL, action="color-to-empty", args=(self.from_color,)
            )


class GameSkillHeal(GameSkill):
    def __init__(self, color, **kwargs):
        super(GameSkillHeal, self).__init__("heal", color, 25, **kwargs)
        self.heal_value = kwargs.get("heal", 10)
        self.image = pygame.image.load(os.path.join("apps/sirtet/images", "heal.jpg"))

    def action(self, source, target):
        """can_run checks if the skill is available to be executed.
        """
        if self.can_run(source):
            print(f"heal {target} fpr {self.heal_value}")
            target.health += self.heal_value
            source.counter_colors_available[self.color_str] -= self.threshold


class GameSkillGreatHeal(GameSkillHeal):
    def __init__(self, color, **kwargs):
        super(GameSkillGreatHeal, self).__init__(color, heal=50, **kwargs)
        self.name = "great-heal"
        self.threshold = 100
        self.image = pygame.image.load(
            os.path.join("apps/sirtet/images", "great_heal.jpg")
        )


class GameSkillMegaHeal(GameSkill):
    def __init__(self, color, **kwargs):
        super(GameSkillMegaHeal, self).__init__(color, heal=500, **kwargs)
        self.name = "mega-heal"
        self.threshold = 250
        self.image = pygame.image.load(
            os.path.join("apps/sirtet/images", "mega_heal.jpg")
        )


class GameSkillDefenseUp(GameSkill):
    def __init__(self, color, **kwargs):
        super(GameSkillDefenseUp, self).__init__(
            "defense-up", color, 50, expire=5, **kwargs
        )
        self.defense_value = kwargs.get("defense", 1)
        self.image = pygame.image.load(
            os.path.join("apps/sirtet/images", "defense_up.jpg")
        )

    def action(self, source, target):
        """can_run checks if the skill is available to be executed.
        """
        if self.can_run(source):
            target._defense.add_buff(self.defense_value)
            source.counter_colors_available[self.color_str] -= self.threshold
            self.clean_up_event(source, target, expire={"lines": self.expire})

    def clean_up(self, source, target):
        """clean_up proceeds to reverse any action triggered by the skill.
        """

        def _clean_up():
            target._defense.del_buff(self.defense_value)

        return _clean_up


class GameSkillDamageUp(GameSkill):
    def __init__(self, color, **kwargs):
        super(GameSkillDamageUp, self).__init__(
            "damage-up", color, 100, expire=5, **kwargs
        )
        self.damage_value = kwargs.get("damage", 1)
        self.image = pygame.image.load(
            os.path.join("apps/sirtet/images", "damage_up.jpg")
        )

    def action(self, source, target):
        """can_run checks if the skill is available to be executed.
        """
        if self.can_run(source):
            target._damage.add_buff(self.damage_value)
            source.counter_colors_available[self.color_str] -= self.threshold
            self.clean_up_event(source, target, expire={"lines": self.expire})

    def clean_up(self, source, target):
        """clean_up proceeds to reverse any action triggered by the skill.
        """

        def _clean_up():
            target._damage.del_buff(self.damage_value)

        return _clean_up


class GameSkillMindUp(GameSkill):
    def __init__(self, color, **kwargs):
        super(GameSkillMindUp, self).__init__(
            "skill-up", color, 100, expire=5, **kwargs
        )
        self.mind_value = kwargs.get("mind", 1)

    def action(self, source, target):
        """can_run checks if the skill is available to be executed.
        """
        if self.can_run(source):
            target._skill.add_buff(self.mind_value)
            source.counter_colors_available[self.color_str] -= self.threshold
            self.clean_up_event(source, target, expire={"lines": self.expire})

    def clean_up(self, source, target):
        """clean_up proceeds to reverse any action triggered by the skill.
        """

        def _clean_up():
            target._skill.del_buff(self.mind_value)

        return _clean_up


class GameSkillDamageBuffUp(GameSkill):
    def __init__(self, color, **kwargs):
        super(GameSkillDamageBuffUp, self).__init__(
            "damage-buff-up", color, 50, expire=5, **kwargs
        )
        self.damage_value = kwargs.get("damage", 1)

    def action(self, source, target):
        """can_run checks if the skill is available to be executed.
        """
        if self.can_run(source):
            target.damage_buffs.append(self.damage_value)
            source.counter_colors_available[self.color_str] -= self.threshold
            self.clean_up_event(source, target, expire={"lines": self.expire})

    def clean_up(self, source, target):
        """clean_up proceeds to reverse any action triggered by the skill.
        """

        def _clean_up():
            target.damage_buffs.remove(self.damage_value)

        return _clean_up


class GameSkillDefenseBuffUp(GameSkill):
    def __init__(self, color, **kwargs):
        super(GameSkillDefenseBuffUp, self).__init__(
            "defense-buff-up", color, 50, expire=5, **kwargs
        )
        self.defense_value = kwargs.get("defense", 1)

    def action(self, source, target):
        """can_run checks if the skill is available to be executed.
        """
        if self.can_run(source):
            target.defense_buffs.append(self.defense_value)
            source.counter_colors_available[self.color_str] -= self.threshold
            self.clean_up_event(source, target, expire={"lines": self.expire})

    def clean_up(self, source, target):
        """clean_up proceeds to reverse any action triggered by the skill.
        """

        def _clean_up():
            target.defense_buffs.remove(self.defense_value)

        return _clean_up


class GameSkillMindBuffUp(GameSkill):
    def __init__(self, color, **kwargs):
        super(GameSkillMindBuffUp, self).__init__(
            "skill-buff-up", color, 50, expire=5, **kwargs
        )
        self.mind_value = kwargs.get("mind", 1)

    def action(self, source, target):
        """can_run checks if the skill is available to be executed.
        """
        if self.can_run(source):
            target.mind_buffs.append(self.mind_value)
            source.counter_colors_available[self.color_str] -= self.threshold
            self.clean_up_event(source, target, expire={"lines": self.expire})

    def clean_up(self, source, target):
        """clean_up proceeds to reverse any action triggered by the skill.
        """

        def _clean_up():
            target.mind_buffs.remove(self.mind_value)

        return _clean_up


class GameSkillRawDamage(GameSkill):
    def __init__(self, color, **kwargs):
        super(GameSkillRawDamage, self).__init__("raw-damage", color, 25, **kwargs)
        self._target = "target"
        self.damage_value = kwargs.get("damage", 10)
        self.image = pygame.image.load(
            os.path.join("apps/sirtet/images", "raw_damage.jpg")
        )

    def action(self, source, target):
        """can_run checks if the skill is available to be executed.
        """
        if self.can_run(source):
            target.health -= self.damage_value
            source.counter_colors_available[self.color_str] -= self.threshold
