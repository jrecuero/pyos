# import pygame
from pyplay import Gid
from _game_stat import GameStat
from _game_actor_attr import GameActorAttr
from _game_actor_stats import GameActorStats
from _game_actor_display import GameActorDisplay


class GameActor(Gid):
    """GameActor implements any actor in the game.
    """

    def __init__(self, name, **kwargs):
        super(GameActor, self).__init__()
        self.name = name
        self._health = GameActorAttr("health", kwargs.get("health", 0))
        self._damage = GameActorAttr("damage", kwargs.get("damage", 0))
        self._defense = GameActorAttr("defense", kwargs.get("defense", 0))
        self._skill = GameActorAttr("skill", kwargs.get("skill", 0))
        self.stats = GameActorStats()
        self.play_colors = GameStat.new_play_colors()
        self.skill_colors = GameStat.new_play_colors()
        self.play_stats = {"damage": None, "defense": None, "skill": None}
        self.damage_skills = []
        self.defense_skills = []
        self.skill_skills = []

    @property
    def health(self):
        return self._health.real

    @health.setter
    def health(self, value):
        self._health.real = value

    @property
    def damage(self):
        return self._damage.real

    @damage.setter
    def damage(self, value):
        self._damage.real = value

    @property
    def defense(self):
        return self._defense.real

    @defense.setter
    def defense(self, value):
        self._defense.real = value

    @property
    def skill(self):
        return self._skill.real

    @skill.setter
    def skill(self, value):
        self._skill.real = value

    @property
    def max_health(self):
        return self._health.max

    @max_health.setter
    def max_health(self, value):
        self._health.max = value
        self._health.real = value

    @property
    def max_damage(self):
        return self._damage.max

    @max_damage.setter
    def max_damage(self, value):
        self._damage.max = value
        self._damage.real = value

    @property
    def max_defense(self):
        return self._defense.max

    @max_defense.setter
    def max_defense(self, value):
        self._defense.max = value
        self._defense.real = value

    @property
    def max_skill(self):
        return self._skill.max

    @max_skill.setter
    def max_skill(self, value):
        self._skill.max = value
        self._skill.real = value

    def __str__(self):
        return f"[{self.gid}] : {self.__class__.__name__}@{self.name} | {self.health.real} {self.damage.real} {self.defense.real} {self.skill.real}"

    def gdisplay(self):
        """gdisplay returns the graphical sprite object to be added to a scene
        in order to display actor information.
        """
        return GameActorDisplay(self, 0, 0, 600, 200)

    def add_color_dict(self, color_dict=None):
        """add_color_dict adds the given color dictionary to the total colors
        for the actual game.
        """
        if color_dict:
            self.stats.add_color_dict(color_dict)
            for k, v in color_dict.items():
                self.play_colors[k] += v
                self.skill_colors[k] += v
        else:
            self.play_colors = GameStat.new_play_colors()
            self.skill_colors = GameStat.new_play_colors()

    def set_play_damage(self, color):
        """set_play_damage sets the color to be used by the actor as damage
        color.
        """
        self.play_stats["damage"] = color

    def set_play_defense(self, color):
        """set_play_defense sets the color to be used by the actor as defense
        color.
        """
        self.play_stats["defense"] = color

    def set_play_skill(self, color):
        """set_play_skill sets the color to be used by the actor as skill
        color.
        """
        self.play_stats["skill"] = color

    def get_damage_color(self):
        """get_damage_color returns the color used by the actor as damage
        color.
        """
        return self.play_stats["damage"]

    def get_defense_color(self):
        """get_defense_color returns the color used by the actor as defense
        color.
        """
        return self.play_stats["defense"]

    def get_skill_color(self):
        """get_skill_color returns the color used by the actor as skill
        color.
        """
        return self.play_stats["skill"]

    def damage_for(self, value):
        """damage_for returns the damage caused for the given number of cells
        of the actor damage color.
        """
        return self.damage.real * value

    def defense_for(self, value):
        """defense_for returns the defense caused for the given number of cells
        of the actor defense color.
        """
        return self.defense.real * value

    def skill_for(self, value):
        """skill_for returns the skill caused for the given number of cells of
        the actor skill color.
        """
        return self.skill.real * value
