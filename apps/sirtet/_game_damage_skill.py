from pyplay import Color
from ._game_skill import GameSkill


DAMAGE_COLOR = Color.RED


class GameSkillDamageUp(GameSkill):
    def __init__(self, **kwargs):
        super(GameSkillDamageUp, self).__init__(
            "damage-up", DAMAGE_COLOR, 100, **kwargs
        )
        self.damage_value = kwargs.get("damage", 1)
        self.expire = kwargs.get("expire", 5)

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
            target._damage.del_buff(self.damave_value)

        return _clean_up


class GameSkillDamageBuffUp(GameSkill):
    def __init__(self, **kwargs):
        super(GameSkillDamageBuffUp, self).__init__(
            "damage-buff-up", DAMAGE_COLOR, 50, **kwargs
        )
        self.damage_value = kwargs.get("damage", 1)
        self.expire = kwargs.get("expire", 5)

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


class GameSkillRawDamage(GameSkill):
    def __init__(self, **kwargs):
        super(GameSkillRawDamage, self).__init__(
            "raw-damage", DAMAGE_COLOR, 25, **kwargs
        )
        self._target = "target"
        self.damage_value = kwargs.get("damage", 10)

    def action(self, source, target):
        """can_run checks if the skill is available to be executed.
        """
        if self.can_run(source):
            target.health -= self.damage_value
            source.counter_colors_available[self.color_str] -= self.threshold
