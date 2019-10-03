from pyplay import Color
from _game_actor import GameActor

# import _game_skill as gs


class GameActorTarget(GameActor):
    def __init__(self, name, **kwargs):
        super(GameActorTarget, self).__init__(name, **kwargs)
        self.max_health = 10
        self.max_damage = 2
        self.set_play_damage(Color.BLACK)
        self.set_play_defense(Color.BLACK)
        self.set_play_mind(Color.BLACK)
        # self.damage_skills.append(gs.GameSkillRawDamage(Color.BLACK))
        # self.defense_skills.append(gs.GameSkillDefenseUp(Color.BLACK))
        # self.mind_skills.append(gs.GameSkillHeal(Color.BLACK))
