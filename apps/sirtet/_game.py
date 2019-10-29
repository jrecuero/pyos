import sys
import pygame

from _game_scene_title import GameSceneTitle
from _game_scene_main import GameSceneMain
from _game_scene_board import GameSceneBoard
from _game_scene_result import GameSceneResult
from _game_scene_end import GameSceneEnd
from _game_handler import GameHandler
from _game_actor_player import GameActorPlayer
from _game_actor_target import GameActorTarget


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
        self._played = True
        self._match_played = True

    def create(self):
        """create creates all custom instances required for handling the
        actual game implementation.
        """
        self.gh = GameHandler("app", self.surface)
        self.scene_title = GameSceneTitle(self.surface)
        self.scene_main = GameSceneMain(self.surface)
        self.scene_board = GameSceneBoard(self.surface)
        self.scene_result = GameSceneResult(self.surface)
        self.scene_end = GameSceneEnd(self.surface)
        self.gh.add_scene(self.scene_title)
        # self.gh.add_scene(self.scene_main)
        self.gh.add_scene(self.scene_board)
        # self.gh.add_scene(self.scene_result)
        self.gh.add_scene(self.scene_end)
        self.gh.hscene.active(self.scene_title)

    def new_game(self):
        """new_game should create all required resources (actor and targets)
        for a new match. It should be called only one time for the full game.
        """
        self.actor = GameActorPlayer()

    def stop_game(self):
        """stop_game stops and proceeds to end the game.
        """
        self._played = False

    def end_game(self):
        """end_game should be called for closing the game.
        """
        pass

    def start_match(self):
        """start_match starts a new match with all resources already created.
        It should be called every time a match start.
        """
        self.number_of_targets = 1
        self.targets = [
            GameActorTarget(f"t{i+1}") for i in range(self.number_of_targets)
        ]
        # TODO: call game handler start new match, which shoudl initializes
        # the game handler.
        # TODO: reinitialize scene board at this point.
        self.gh.start_match(actor=self.actor, targets=self.targets)
        self._match_played = True

    def stop_match(self):
        """stop_match stops the current played match.
        """
        self._match_played = False

    def end_match(self):
        """end_match stops and end a match.
        """
        self.gh.end_match()

    def is_play(self):
        """is_play returns if the game should be still be playable.
        """
        return self._played

    def is_match(self):
        """is_match returns if the game match is still playable.
        """
        return self._match_played

    def play_match(self):
        """play_match runs and plays a match game.
        """
        # # ->
        # # TODO: This should be called when a new match starts.
        # self.gh.start_match()
        # # <-

        while self.is_match():
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

        # # ->
        # # TODO: This should be called when a match ends.
        # self.gh.end_match()
        # # <-

    def play(self):
        """play implements the game loop.
        """
        self.create()
        self.new_game()
        while self.is_play():
            self.start_match()
            self.play_match()
            self.end_match()
        self.end_game()
