import sys
import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame

from pyplay import Color
from _game_scene_board import GameSceneBoard
from _game_scene_title import GameSceneTitle
from _game_scene_end import GameSceneEnd
from _game_handler import GameHandler
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
        self.mind_skills.append(gs.GameSkillDefenseUp(Color.GREEN))
        self.mind_skills.append(gs.GameSkillHeal(Color.GREEN))
        self.mind_skills.append(gs.GameSkillGreatHeal(Color.GREEN))


class Target(GameActor):
    def __init__(self, name, **kwargs):
        super(Target, self).__init__(name, **kwargs)
        self.max_health = 10
        self.max_damage = 2
        self.set_play_damage(Color.BLACK)
        self.set_play_defense(Color.BLACK)
        self.set_play_mind(Color.BLACK)
        self.damage_skills.append(gs.GameSkillRawDamage(Color.BLACK))
        self.defense_skills.append(gs.GameSkillDefenseUp(Color.BLACK))
        self.mind_skills.append(gs.GameSkillHeal(Color.BLACK))


class TheGame:
    """TheGame class implements game functionality.
    """

    SCREEN_SIZE = (1200, 850)

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("SIRTET")
        self.surface = pygame.display.set_mode(TheGame.SCREEN_SIZE)
        self.clock = pygame.time.Clock()

    def create(self):
        """create creates all custom instances required for handling the
        actual game implementation.
        """
        self.gh = GameHandler("app", self.surface)
        self.scene_board = GameSceneBoard(self.surface)
        self.scene_title = GameSceneTitle(self.surface)
        self.scene_end = GameSceneEnd(self.surface)
        self.gh.add_scene(self.scene_title)
        self.gh.add_scene(self.scene_board)
        self.gh.add_scene(self.scene_end)
        self.gh.hscene.active(self.scene_title)

    def play(self):
        """play runs and plays the game.
        """
        # ->
        # TODO: This should be called when a new match starts.
        self.gh.start_match()
        # <-

        while True:
            self.clock.tick(30)
            self.gh.start_tick()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                elif event.type in [pygame.KEYDOWN, pygame.KEYUP]:
                    self.gh.handle_keyboard_event(event)
                elif event.type in [
                    pygame.MOUSEMOTION,
                    pygame.MOUSEBUTTONDOWN,
                    pygame.MOUSEBUTTONUP,
                ]:
                    self.gh.handle_mouse_event(event)
                elif event.type >= pygame.USEREVENT:
                    self.gh.handle_custom_event(event)

            # -> update objects
            self.gh.update()
            # <-

            # -> render objects
            self.surface.fill((255, 255, 255))
            self.gh.render()
            pygame.display.flip()
            # <-
            self.gh.end_tick()

        # ->
        # TODO: This should be called when a match ends.
        self.gh.end_match()
        # <-


def main():
    """main implements the full game application.
    """
    game = TheGame()
    game.create()
    game.play()


if __name__ == "__main__":
    main()
