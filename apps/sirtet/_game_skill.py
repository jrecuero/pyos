from pyplay import Color


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
        colors = source.play_colors[self.color_str]
        return colors > self.threshold

    def action(self, source, target):
        """can_run checks if the skill is available to be executed.
        """
        pass


class GameSkillHeal(GameSkill):
    def __init__(self, color, **kwargs):
        super(GameSkillHeal, self).__init__("heal", color, 50, **kwargs)

    def action(self, source, target):
        """can_run checks if the skill is available to be executed.
        """
        target.health += 50
