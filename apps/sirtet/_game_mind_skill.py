from pyplay import Color
from ._game_skill import GameSkill


class GameSkillMindUp(GameSkill):
    def __init__(self, color, **kwargs):
        super(GameSkillMindUp, self).__init__("skill-up", Color.GREEN, 100, **kwargs)
        self.mind_value = kwargs.get("mind", 1)
        self.expire = kwargs.get("expire", 5)

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
