from pyplay import Gid
from _game_stat import GameStat
from _game_actor_attr import GameActorAttr
from _game_actor_stats import GameActorStats
from _game_actor_display import GameActorDisplay
from _game_level import GameLevel


class GameActor(Gid):
    """GameActor implements any actor in the game.
    """

    def __init__(self, name, **kwargs):
        super(GameActor, self).__init__()
        self.name = name
        self._health = GameActorAttr("health", kwargs.get("health", 0))
        self._damage = GameActorAttr("damage", kwargs.get("damage", 0))
        self._defense = GameActorAttr("defense", kwargs.get("defense", 0))
        self._mind = GameActorAttr("mind", kwargs.get("mind", 0))
        self.image = GameActorAttr("image", kwargs.get("image", None))
        self.stats = GameActorStats()
        self.counter_colors_all = GameStat.new_play_colors()
        self.counter_colors_available = GameStat.new_play_colors()
        self.attr_to_color = {"damage": None, "defense": None, "mind": None}
        self.damage_skills = []
        self.defense_skills = []
        self.mind_skills = []
        self.damage_buffs = []
        self.defense_buffs = []
        self.mind_buffs = []
        self.glevel = GameLevel()

    @property
    def health(self):
        """health property returns the real/actual value for the _health
        attribute.
        """
        return self._health.real

    @health.setter
    def health(self, value):
        """health setter sets the value for real health.
        """
        self._health.real = value

    @property
    def damage(self):
        """damage property returns the real/actual value for the _damage
        attribute.
        """
        return self._damage.real

    @damage.setter
    def damage(self, value):
        """damage setter sets the value for real damage.
        """
        self._damage.real = value

    @property
    def defense(self):
        """defense property returns the real/actual value for the _defense
        attribute.
        """
        return self._defense.real

    @defense.setter
    def defense(self, value):
        """defense setter sets the value for real defense.
        """
        self._defense.real = value

    @property
    def mind(self):
        """mind property returns the real/actual value for the _mind
        attribute.
        """
        return self._mind.real

    @mind.setter
    def mind(self, value):
        """mind setter sets the value for real mind.
        """
        self._mind.real = value

    @property
    def max_health(self):
        """max_health returns the maximum health for the actor. It is
        found as max attribute for _health.
        """
        return self._health.max

    @max_health.setter
    def max_health(self, value):
        """max_health setter updates the maximum and real health.
        """
        self._health.max = value
        self._health.real = value

    @property
    def max_damage(self):
        """max_damage returns the maximum health for the actor. It is
        found as max attribute for _damage.
        """
        return self._damage.max

    @max_damage.setter
    def max_damage(self, value):
        """max_damage setter updates the maximum and real damage.
        """
        self._damage.max = value
        self._damage.real = value

    @property
    def max_defense(self):
        """max_defense returns the maximum health for the actor. It is
        found as max attribute for _defense.
        """
        return self._defense.max

    @max_defense.setter
    def max_defense(self, value):
        """max_defense setter updates the maximum and real defense.
        """
        self._defense.max = value
        self._defense.real = value

    @property
    def max_mind(self):
        """max_mind returns the maximum health for the actor. It is
        found as max attribute for _mind.
        """
        return self._mind.max

    @max_mind.setter
    def max_mind(self, value):
        """max_mind setter updates the maximum and real mind.
        """
        self._mind.max = value
        self._mind.real = value

    @property
    def level(self):
        """level return the level attribute for glevel.
        """
        return self.glevel.level

    @property
    def all_skills(self):
        """all_skills property returns a list with all skills put together.
        """
        skills = self.damage_skills[:]
        skills.extend(self.defense_skills)
        skills.extend(self.mind_skills)
        return skills

    def __str__(self):
        return f"[{self.gid}] : {self.__class__.__name__}@{self.name} | {self.health.real} {self.damage.real} {self.defense.real} {self.mind.real}"

    def gdisplay(self):
        """gdisplay returns the graphical sprite object to be added to a scene
        in order to display actor information.
        """
        return GameActorDisplay(self, 0, 0, 700, 200)

    def add_color_dict(self, color_dict=None):
        """add_color_dict adds the given color dictionary to the total colors
        for the actual game.
        """
        if color_dict:
            self.stats.add_color_dict(color_dict)
            for k, v in color_dict.items():
                self.counter_colors_all[k] += v
                self.counter_colors_available[k] += v
        else:
            self.counter_colors_all = GameStat.new_play_colors()
            self.counter_colors_available = GameStat.new_play_colors()

    def set_play_damage(self, color):
        """set_play_damage sets the color to be used by the actor as damage
        color.
        """
        self.attr_to_color["damage"] = color

    def set_play_defense(self, color):
        """set_play_defense sets the color to be used by the actor as defense
        color.
        """
        self.attr_to_color["defense"] = color

    def set_play_mind(self, color):
        """set_play_mind sets the color to be used by the actor as mind
        color.
        """
        self.attr_to_color["mind"] = color

    def get_damage_color(self):
        """get_damage_color returns the color used by the actor as damage
        color.
        """
        return self.attr_to_color["damage"]

    def get_defense_color(self):
        """get_defense_color returns the color used by the actor as defense
        color.
        """
        return self.attr_to_color["defense"]

    def get_mind_color(self):
        """get_mind_color returns the color used by the actor as mind
        color.
        """
        return self.attr_to_color["mind"]

    def damage_for(self, value):
        """damage_for returns the damage caused for the given number of cells
        of the actor damage color.
        """
        return self.damage.real * value + sum(self.damage_buffs)

    def defense_for(self, value):
        """defense_for returns the defense caused for the given number of cells
        of the actor defense color.
        """
        return self.defense.real * value + sum(self.defense_buffs)

    def mind_for(self, value):
        """mind_for returns the mind caused for the given number of cells of
        the actor mind color.
        """
        return self.mind.real * value + sum(self.mind_buffs)

    def start_match(self):
        """start_match proceeds to start a match and it will call all
        objects involved in the match like skills, ...
        """
        for skill in self.all_skills:
            skill.start_match(self)

    def end_match(self):
        """end_match proceeds to end a match and it will call all objects
        that were involved in the match like skills.
        """
        for skill in self.all_skills:
            skill.end_match(self)
