from pyplay import Color, GEvent
from ._game_skill import GameSkill

MIND_COLOR = Color.GREEN


class GameSkillMindUp(GameSkill):
    def __init__(self, color, **kwargs):
        super(GameSkillMindUp, self).__init__("skill-up", MIND_COLOR, 100, **kwargs)
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


class GameSkillMindBuffUp(GameSkill):
    def __init__(self, **kwargs):
        super(GameSkillMindBuffUp, self).__init__(
            "skill-buff-up", MIND_COLOR, 50, **kwargs
        )
        self.mind_value = kwargs.get("mind", 1)
        self.expire = kwargs.get("expire", 5)

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


class GameSkillBlowColor(GameSkill):
    def __init__(self, blow_color, **kwargs):
        super(GameSkillBlowColor, self).__init__("blow-color", MIND_COLOR, 10, **kwargs)
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
    def __init__(self, **kwargs):
        super(GameSkillBlowEmpty, self).__init__("blow-color", MIND_COLOR, 10, **kwargs)

    def action(self, source, target):
        """can_run checks if the skill is available to be executed.
        """
        if self.can_run(source):
            source.counter_colors_available[self.color_str] -= self.threshold
            GEvent.board_event(GEvent.SKILL, action="blow-empty", args=())


class GameSkillCopyColor(GameSkill):
    def __init__(self, from_color, to_color, **kwargs):
        super(GameSkillCopyColor, self).__init__("copy-color", MIND_COLOR, 10, **kwargs)
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
    def __init__(self, from_color, **kwargs):
        super(GameSkillColorToEmpty, self).__init__(
            "color-to-empty", MIND_COLOR, 10, **kwargs
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
    def __init__(self, **kwargs):
        super(GameSkillHeal, self).__init__("heal", MIND_COLOR, 25, **kwargs)
        self.heal_value = kwargs.get("heal", 10)

    def action(self, source, target):
        """can_run checks if the skill is available to be executed.
        """
        if self.can_run(source):
            print(f"heal {target} fpr {self.heal_value}")
            target.health += self.heal_value
            source.counter_colors_available[self.color_str] -= self.threshold


class GameSkillGreatHeal(GameSkillHeal):
    def __init__(self, **kwargs):
        super(GameSkillGreatHeal, self).__init__(heal=50, **kwargs)
        self.name = "great-heal"
        self.threshold = 100


class GameSkillMegaHeal(GameSkill):
    def __init__(self, **kwargs):
        super(GameSkillMegaHeal, self).__init__(heal=500, **kwargs)
        self.name = "mega-heal"
        self.threshold = 250
