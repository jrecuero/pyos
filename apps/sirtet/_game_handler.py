import pygame
from pyplay import GHandler, Color, GEvent
from pyplay.gobject import GText
from _game_stat import GameStat
from _game_actor import GameActor
from _game_skill import GameSkillHeal


class Actor(GameActor):
    def __init__(self, **kwargs):
        super(Actor, self).__init__("actor")
        self.max_health = 1000
        self.max_damage = 2
        self.max_defense = 1
        self.max_skill = 1
        self.set_play_damage(Color.RED)
        self.set_play_defense(Color.BLUE)
        self.set_play_skill(Color.GREEN)
        self.skill_skills.append(GameSkillHeal(Color.GREEN))


class Target(GameActor):
    def __init__(self, name, **kwargs):
        super(Target, self).__init__(name, **kwargs)
        self.max_health = 50
        self.max_damage = 2
        self.set_play_damage(Color.BLACK)
        self.set_play_defense(Color.BLACK)
        self.set_play_skill(Color.BLACK)


class GameHandler(GHandler):
    """GameHandler implements all custom functionality for the actual game.
    """

    def __init__(self, name, surface, **kwargs):
        super(GameHandler, self).__init__(name, surface, **kwargs)
        self.gstat = GameStat()
        self.console = GText("console", 10, 800, f"> {' ' * 50}")
        self.actor = Actor()
        self.targets = [Target("t1"), Target("t2"), Target("t3")]

    def get_actor_damage(self, actor, color_dict):
        """get_actor_damage returns the damage deal for the given actor with
        the pieces being completed.
        """
        damage_color = Color.color_to_str(actor.get_damage_color())
        damage_value = color_dict[damage_color]
        damage = actor.damage_for(damage_value)
        return damage

    def get_actor_defense(self, actor, color_dict):
        """get_actor_defense returns the defense for the given actor with
        the pieces being completed.
        """
        defense_color = Color.color_to_str(actor.get_defense_color())
        defense_value = color_dict[defense_color]
        defense = actor.defense_for(defense_value)
        return defense

    def get_actor_skill(self, actor, color_dict):
        """get_actor_skill returns the skill for the given actor with the
        pieces completed.
        """
        skill_color = Color.color_to_str(actor.get_skill_color())
        skill_value = color_dict[skill_color]
        skill = actor.skill_for(skill_value)
        return skill

    def handle_completed_lines(self, lines):
        """handle_completed_lines handles lines that have been completed in the
        play cells area.
        """
        color_dict = GameStat.new_play_colors()
        for cell in [c for _, line in lines for c in line]:
            color_dict[Color.color_to_str(cell.color)] += 1
        self.gstat.add_color_dict(color_dict)
        self.gstat.add_to_lines(len(lines))
        self.actor.add_color_dict(color_dict)
        actor_damage = self.get_actor_damage(self.actor, color_dict)
        actor_defense = self.get_actor_defense(self.actor, color_dict)
        target = self.targets[0]
        target.add_color_dict(color_dict)
        t_damage = self.get_actor_damage(target, color_dict)
        target.health = target.health - actor_damage
        target_damage = t_damage - actor_defense
        target_damage = target_damage if target_damage > 0 else 0
        self.actor.health = self.actor.health - target_damage
        self.console.message = f"> Actor Damage {actor_damage} Defense {actor_defense}. Target Damage {t_damage} {target_damage}"
        if target.health <= 0:
            self.targets.remove(target)
            if len(self.targets):
                new_target = pygame.event.Event(
                    GEvent.ENGINE,
                    subtype=GEvent.CREATE,
                    dest=GEvent.SCENE,
                    source=self.targets[0].gdisplay(),
                )
                pygame.event.post(new_target)
        if len(self.targets) == 0:
            end_event = pygame.event.Event(
                GEvent.ENGINE, subtype=GEvent.END, winner="actor"
            )
            pygame.event.post(end_event)

    def handle_keyboard_event(self, event):
        """handle_keyboard_event should process the keyboard event given.
        """
        if event.key == pygame.K_1:
            if self.actor.skill_skills[0].can_run(self.actor):
                self.actor.skill_skills[0].action(self.actor, self.actor)
        super(GameHandler, self).handle_keyboard_event(event)

    def handle_custom_event(self, event):
        """handle_custom_event should process pygame custom event given.
        Any object in the game, like, scene, graphic objects, ... can post
        customs events, and those should be handled at this time.
        """
        if event.type == GEvent.ENGINE and event.subtype == GEvent.COMPLETED:
            self.handle_completed_lines(event.source)
        elif event.type == GEvent.ENGINE and event.subtype == GEvent.END:
            if event.winner == "actor":
                self.console.message = f"> GAME OVER. You WON!!!"
            else:
                self.console.message = f"> GAME OVER. You LOST!!!"
            self.running = False
        elif event.type == GEvent.ENGINE and event.subtype == GEvent.PAUSE:
            if event.source:
                self.console.message = f"> PAUSED"
                self.running = False
            else:
                self.console.message = f">"
                self.running = True
        super(GameHandler, self).handle_custom_event(event)

    def update(self, **kwargs):
        """update calls update method for all scenes and  graphical objects.
        """
        super(GameHandler, self).update(**kwargs)
