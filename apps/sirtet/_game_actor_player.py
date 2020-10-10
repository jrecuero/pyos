from pyplay import Color
from _game_actor import GameActor

# import _game_skill as gs


class GameActorPlayer(GameActor):
    def __init__(self, **kwargs):
        super(GameActorPlayer, self).__init__("actor")
        self.max_health = 1000
        self.max_damage = 1
        self.max_defense = 1
        self.max_skill = 1
        self.set_play_damage(Color.RED)
        self.set_play_defense(Color.BLUE)
        self.set_play_mind(Color.GREEN)
        # self.damage_skills.append(gs.GameSkillRawDamage(Color.RED))
        # self.defense_skills.append(gs.GameSkillDamageUp(Color.BLUE))
        # self.mind_skills.append(gs.GameSkillDefenseUp(Color.GREEN))
        # self.mind_skills.append(gs.GameSkillHeal(Color.GREEN))
        # self.mind_skills.append(gs.GameSkillGreatHeal(Color.GREEN))
