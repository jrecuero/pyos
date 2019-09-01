import pygame
from pyplay import GHandler, Color, GEvent
from pyplay.gobject import GText
from _game_stat import GameStat
from _game_actor import GameActor


class Actor(GameActor):
    def __init__(self, **kwargs):
        super(Actor, self).__init__("actor")
        self.health = 1000
        self.damage = 1
        self.defense = 1
        self.skill = 1
        self.set_play_damage(Color.RED)
        self.set_play_defense(Color.GREEN)
        self.set_play_skill(Color.BLUE)


class Target(GameActor):
    def __init__(self, name, **kwargs):
        super(Target, self).__init__(name, **kwargs)
        self.health = 50
        self.damage = 1
        self.set_play_damage(Color.BLACK)


class GameHandler(GHandler):
    """GameHandler implements all custom functionality for the actual game.
    """

    def __init__(self, name, surface, **kwargs):
        super(GameHandler, self).__init__(name, surface, **kwargs)
        self.gstat = GameStat()
        self.console = GText("console", 10, 800, f"> {' ' * 50}")
        self.actor = Actor()
        self.targets = [Target("t1")]

    def handle_completed_lines(self, lines):
        """handle_completed_lines handles lines that have been completed in the
        play cells area.
        """
        color_dict = self.gstat.get_color_dict()
        for cell in [c for _, line in lines for c in line]:
            # self.gstat.add_to_color(cell.color)
            color_dict[Color.color_to_str(cell.color)] += 1
        self.gstat.add_color_dict(color_dict)
        self.gstat.add_to_lines(len(lines))
        damage_color = Color.color_to_str(self.actor.get_damage_color())
        damage_value = color_dict[damage_color]
        damage = self.actor.damage_for(damage_value)
        self.console.message = (
            f"> Damage {damage_color}:{color_dict[damage_color]} for {damage}"
        )

    def handle_custom_event(self, event):
        """handle_custom_event should process pygame custom event given.
        Any object in the game, like, scene, graphic objects, ... can post
        customs events, and those should be handled at this time.
        """
        if event.type == GEvent.GAMEPLAY and event.subtype == GEvent.COMPLETED:
            self.handle_completed_lines(event.source)
        elif event.type == GEvent.HANDLING and event.subtype == GEvent.END:
            self.console.message = f"> GAME OVER"
            self.running = False
        elif event.type == GEvent.HANDLING and event.subtype == GEvent.PAUSE:
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
        actor_event = pygame.event.Event(
            GEvent.DISPLAY, subtype=GEvent.GDISPLAY, source=self.actor, actor="actor"
        )
        pygame.event.post(actor_event)

        targets_event = pygame.event.Event(
            GEvent.DISPLAY,
            subtype=GEvent.GDISPLAY,
            source=self.targets[0],
            actor="target",
        )
        pygame.event.post(targets_event)
        super(GameHandler, self).update(**kwargs)
