from pyplay import Color
from ._game_skill import GameSkill

DEFENSE_COLOR = Color.BLUE


class GameSkillDefenseUp(GameSkill):
    def __init__(self, color, **kwargs):
        super(GameSkillDefenseUp, self).__init__(
            "defense-up", DEFENSE_COLOR, 50, **kwargs
        )
        self.defense_value = kwargs.get("defense", 1)
        self.expire = kwargs.get("expire", 5)

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


class GameSkillDefenseBuffUp(GameSkill):
    def __init__(self, **kwargs):
        super(GameSkillDefenseBuffUp, self).__init__(
            "defense-buff-up", DEFENSE_COLOR, 50, **kwargs
        )
        self.defense_value = kwargs.get("defense", 1)
        self.expire = kwargs.get("expire", 5)

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
