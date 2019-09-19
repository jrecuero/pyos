import pygame
import random
from pyplay import GHandler, Color, GEvent
from pyplay.gobject import GText
from _game_stat import GameStat
from _game_actor import GameActor
import _game_skill as gs


class Actor(GameActor):
    def __init__(self, **kwargs):
        super(Actor, self).__init__("actor")
        self.max_health = 1000
        self.max_damage = 1
        self.max_defense = 1
        self.max_skill = 1
        self.set_play_damage(Color.RED)
        self.set_play_defense(Color.BLUE)
        self.set_play_mind(Color.GREEN)
        self.damage_skills.append(gs.GameSkillRawDamage(Color.RED))
        self.defense_skills.append(gs.GameSkillDamageUp(Color.BLUE))
        self.mind_skills.append(gs.GameSkillBlowEmpty(Color.GREEN))
        self.mind_skills.append(gs.GameSkillHeal(Color.GREEN))
        self.mind_skills.append(gs.GameSkillGreatHeal(Color.GREEN))


class Target(GameActor):
    def __init__(self, name, **kwargs):
        super(Target, self).__init__(name, **kwargs)
        self.max_health = 50
        self.max_damage = 2
        self.set_play_damage(Color.BLACK)
        self.set_play_defense(Color.BLACK)
        self.set_play_mind(Color.BLACK)
        self.damage_skills.append(gs.GameSkillRawDamage(Color.BLACK))
        self.defense_skills.append(gs.GameSkillDefenseUp(Color.BLACK))
        self.mind_skills.append(gs.GameSkillHeal(Color.BLACK))


class GameHandler(GHandler):
    """GameHandler implements all custom functionality for the actual game.
    """

    def __init__(self, name, surface, **kwargs):
        super(GameHandler, self).__init__(name, surface, **kwargs)
        self.gstat = GameStat()
        self.gobj_console = GText("console", 10, 800, f"> {' ' * 50}")
        self.actor = Actor()
        self.targets = [Target("t1"), Target("t2"), Target("t3")]
        self.skill_actions = {"lines": [], "timer": [], "pieces": []}

    @property
    def target(self):
        """target property returns the first entry in the targets attribute.
        It returns None if targets list is empty.
        """
        if len(self.targets):
            return self.targets[0]
        return None

    def start_match(self):
        """start_match proceeds to start a match and it will call all
        objects involved in the match like skills, ...
        """
        self.actor.start_match()
        for target in self.targets:
            target.start_match()

    def end_match(self):
        """end_match proceeds to end a match and it will call all objects
        that were involved in the match like skills.
        """
        self.actor.end_match()
        for target in self.targets:
            target.end_match()

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

    def get_actor_mind(self, actor, color_dict):
        """get_actor_mind returns the mind for the given actor with the
        pieces completed.
        """
        mind_color = Color.color_to_str(actor.get_mind_color())
        mind_value = color_dict[mind_color]
        mind = actor.mind_for(mind_value)
        return mind

    def check_skill_actions_for_lines(self, lines, color_dict):
        """check_skill_actions check for any skill action to be triggered when
        lines are being completed.
        """
        for sa in self.skill_actions["lines"][:]:
            sa["expire"] -= lines
            if sa["expire"] <= 0:
                sa["action"](*sa["args"])
                self.skill_actions["lines"].remove(sa)

    def check_target_skills(self, lines, color_dict):
        """check_target_skills checks if the target can trigger any skill.
        """
        if self.target:
            available_skills = [None]
            for skill in self.target.damage_skills:
                if skill.can_run(self.target):
                    available_skills.append(skill)
            for skill in self.target.defense_skills:
                if skill.can_run(self.target):
                    available_skills.append(skill)
            for skill in self.target.mind_skills:
                if skill.can_run(self.target):
                    available_skills.append(skill)
            call_skill = random.choice(available_skills)
            if call_skill:
                call_skill.action(
                    self.target, call_skill.target(self.target, self.actor)
                )
                self.gobj_console.message = f"> {skill}"

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
        self.target.add_color_dict(color_dict)
        t_damage = self.get_actor_damage(self.target, color_dict)
        self.target.health = self.target.health - actor_damage
        target_damage = t_damage - actor_defense
        target_damage = target_damage if target_damage > 0 else 0
        self.actor.health = self.actor.health - target_damage
        self.gobj_console.message = f"> Actor Damage {actor_damage} Defense {actor_defense}. Target Damage {t_damage} {target_damage}"
        if self.target.health <= 0:
            self.targets.remove(self.target)
            if len(self.targets):
                GEvent.scene_event(GEvent.CREATE, source=self.target.gdisplay())
        if len(self.targets) == 0:
            GEvent.engine_event(GEvent.END, winner="actor")
        self.check_skill_actions_for_lines(len(lines), color_dict)
        self.check_target_skills(len(lines), color_dict)

    def handle_keyboard_event(self, event):
        """handle_keyboard_event should process the keyboard event given.
        """
        # Handle all keyboard inputs that trigger skills.
        if event.key == pygame.K_1:
            if len(self.actor.damage_skills):
                skill = self.actor.damage_skills[0]
                skill.action(self.actor, skill.target(self.actor, self.target))
                self.gobj_console.message = f"> {skill}"
        if event.key == pygame.K_2:
            if len(self.actor.defense_skills):
                skill = self.actor.defense_skills[0]
                skill.action(self.actor, skill.target(self.actor, self.target))
                self.gobj_console.message = f"> {skill}"
        if event.key == pygame.K_3:
            if len(self.actor.mind_skills):
                skill = self.actor.mind_skills[0]
                skill.action(self.actor, skill.target(self.actor, self.target))
                self.gobj_console.message = f"> {skill}"
        if event.key == pygame.K_4:
            if len(self.actor.mind_skills) > 1:
                skill = self.actor.mind_skills[1]
                skill.action(self.actor, skill.target(self.actor, self.target))
                self.gobj_console.message = f"> {skill}"
        if event.key == pygame.K_5:
            if len(self.actor.mind_skills) > 2:
                skill = self.actor.mind_skills[2]
                skill.action(self.actor, skill.target(self.actor, self.target))
                self.gobj_console.message = f"> {skill}"
        if self.target and self.target.health <= 0:
            self.targets.remove(self.target)
            if len(self.targets):
                GEvent.scene_event(GEvent.CREATE, source=self.target.gdisplay())
        if len(self.targets) == 0:
            GEvent.engine_event(GEvent.END, winner="actor")
        super(GameHandler, self).handle_keyboard_event(event)

    def handle_custom_event(self, event):
        """handle_custom_event should process pygame custom event given.
        Any object in the game, like, scene, graphic objects, ... can post
        customs events, and those should be handled at this time.
        """
        if event.type == GEvent.ENGINE:
            if event.subtype == GEvent.HSCENE and event.source == "next":
                # TODO: Pass actor and target at this point.
                target = self.targets[0] if self.targets else None
                self.hscene.next(
                    console=self.gobj_console,
                    stats=self.gstat,
                    actor=self.actor,
                    target=target,
                )
            if event.subtype == GEvent.COMPLETED:
                self.handle_completed_lines(event.source)
            elif event.subtype == GEvent.END:
                if event.winner == "actor":
                    self.gobj_console.message = f"> GAME OVER. You WON!!!"
                else:
                    self.gobj_console.message = f"> GAME OVER. You LOST!!!"
                self.running = False
            elif event.subtype == GEvent.PAUSE:
                if event.source:
                    self.gobj_console.message = f"> PAUSED"
                    self.running = False
                else:
                    self.gobj_console.message = f">"
                    self.running = True
            elif event.subtype == GEvent.SKILL and GEvent.check_destination(
                event, GEvent.HANDLER
            ):
                if "lines" in event.expire.keys():
                    self.skill_actions["lines"].append(
                        {
                            "expire": event.expire["lines"],
                            "action": event.action,
                            "args": event.args,
                        }
                    )
                pass
        super(GameHandler, self).handle_custom_event(event)

    def update(self, **kwargs):
        """update calls update method for all scenes and  graphical objects.
        """
        super(GameHandler, self).update(**kwargs)
