import os
import sys

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
from pyengine import Scene, GRect, GHandler, Color, Move, Log, Grid


class GameScene(Scene):

    def __init__(self, surface, **kwargs):
        super(GameScene, self).__init__("Game Scene", surface, **kwargs)
        self.actor = GRect("actor", 32, 32, 32, 32)
        self.actor.move = Move(1, 0, 1)
        self.grid = Grid("Grid", 10, 10, 0, 0, 32, 32)
        self.grid.add_gobject(self.actor)
        self.add_gobject(self.grid)


class GameHandler(GHandler):

    def __init__(self, surface, **kwargs):
        super(GameHandler, self).__init__("Gritty", surface, **kwargs)


def main():
    Log.Main("Gritty App").State("Init").call()
    pygame.init()
    pygame.display.set_caption("GRITTY")
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    ghandler = GameHandler(screen)
    gscene = GameScene(screen)
    ghandler.add_scene(gscene)
    ghandler.hscene.active(gscene)
    while True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

        # -> update objects
        ghandler.update()
        # <-

        # -> render objects
        screen.fill(Color.WHITE)
        ghandler.render()
        # pygame.display.flip()
        # <-
    Log.Main("Gritty App").State("End").call()


if __name__ == "__main__":
    main()
