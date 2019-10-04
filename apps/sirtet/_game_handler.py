# import os
import pygame
import random
from pyplay import GHandler, Color, GEvent
from pyplay.gobject import GText
from _game_stat import GameStat


class GameHandler(GHandler):
    """GameHandler implements all custom functionality for the actual game.
    """

    def __init__(self, name, surface, **kwargs):
        super(GameHandler, self).__init__(name, surface, **kwargs)
        self.gstat = GameStat()
        self.gobj_console = GText("console", 10, 800, f"> {' ' * 50}")
        self.actor = None
        self.targets = None
        self.skill_actions = {"lines": [], "timer": [], "pieces": []}

    @property
    def target(self):
        """target property returns the first entry in the targets attribute.
        It returns None if targets list is empty.
        """
        if len(self.targets):
            return self.targets[0]
        return None

    def start_match(self, **kwargs):
        """start_match proceeds to start a match and it will call all
        objects involved in the match like skills, ...
        """
        self.actor = kwargs.get("actor", None)
        self.targets = kwargs.get("targets", None)
        self.actor.start_match()
        for target in self.targets:
            target.start_match()

    def end_match(self, **kwargs):
        """end_match proceeds to end a match and it will call all objects
        that were involved in the match like skills.
        """
        self.actor.end_match()
        for target in self.targets:
            target.end_match()

    def start(self, actor, targets, **kwargs):
        """start starts the game handler.
        """
        self.actor = actor
        self.targets = targets

    def stop(self, **kwargs):
        """stop stops the game handler.
        """
        pass

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
        """check_skill_actions checks all active skills if any of them has
        reached expiration threshold. In that case call the skill action
        clean up and removed it from the list of active skills.
        """
        for sa in self.skill_actions["lines"][:]:
            sa["expire"] -= lines
            if sa["expire"] <= 0:
                # execute skill clean up action.
                sa["action"](*sa["args"])
                self.skill_actions["lines"].remove(sa)

    def check_target_skills(self, lines, color_dict):
        """check_target_skills checks if the target can trigger any skill
        and trigger any possible skill by a random behavior.
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
        # Update screen with new total of lines and colors.
        self.gstat.add_color_dict(color_dict)
        self.gstat.add_to_lines(len(lines))
        self.actor.add_color_dict(color_dict)
        self.target.add_color_dict(color_dict)

        # Calculate damage dealt from the actor to the target.
        actor_damage = self.get_actor_damage(self.actor, color_dict)
        target_defense = self.get_actor_defense(self.target, color_dict)
        damage_to_target = actor_damage - target_defense
        damage_to_target = damage_to_target if damage_to_target > 0 else 0
        self.target.health = self.target.health - damage_to_target

        # Calculate damage dealt from the target to the actor.
        actor_defense = self.get_actor_defense(self.actor, color_dict)
        target_damage = self.get_actor_damage(self.target, color_dict)
        damage_to_actor = target_damage - actor_defense
        damage_to_actor = damage_to_actor if damage_to_actor > 0 else 0
        self.actor.health = self.actor.health - damage_to_actor

        self.gobj_console.message = (
            f"> Damage To Target {damage_to_target}. Target To Actor {damage_to_actor}"
        )

        # Check if target is dead and has to be removed.
        if self.target.health <= 0:
            self.targets.remove(self.target)
            if len(self.targets):
                GEvent.scene_event(GEvent.CREATE, source=self.target.gdisplay())
        if len(self.targets) == 0:
            GEvent.engine_event(GEvent.END, winner="actor")

        # Check any actor skills expiration.
        self.check_skill_actions_for_lines(len(lines), color_dict)

        # Check if target can execute any action.
        self.check_target_skills(len(lines), color_dict)

    def handle_keyboard_event(self, event):
        """handle_keyboard_event should process the keyboard event given.
        """
        # Handle all keyboard inputs that trigger skills by the user.
        if self.running:
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

    def launch_scene_board(self, event):
        """launch_scene_board moves to the scene board.
        """
        self.hscene.next(
            console=self.gobj_console,
            stats=self.gstat,
            actor=self.actor,
            target=self.target,
            music=event.music,
        )

    def handle_custom_event(self, event):
        """handle_custom_event should process pygame custom event given.
        Any object in the game, like, scene, graphic objects, ... can post
        customs events, and those should be handled at this time.
        """
        if event.type == GEvent.ENGINE:
            if event.subtype == GEvent.HSCENE and event.source == "board":
                self.launch_scene_board(event)
            if event.subtype == GEvent.COMPLETED:
                self.handle_completed_lines(event.source)
            elif event.subtype == GEvent.END:
                if event.winner == "actor":
                    self.gobj_console.message = f"> GAME OVER. You WON!!!"
                else:
                    self.gobj_console.message = f"> GAME OVER. You LOST!!!"
                self.running = False
                self.hscene.next()
                print("This is the end")

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
