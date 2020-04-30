import os
# import sys

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
from pyengine import Scene, GRect, GHandler, Color, Log, Grid, Layer, GTimed
# from pyengine import Move


class GameScene(Scene):

    def __init__(self, surface, **kwargs):
        cs = 32     # cell size
        super(GameScene, self).__init__("Game Scene", surface, **kwargs)
        self.target = GRect("target", 0, 0, cs, cs, color=Color.RED)
        self.deco = GTimed("decoration", 4 * cs, 2 * cs, cs, cs, z=Layer.BACKGROUND, color=Color.BLUE, solid=False, timed_counter=0)
        self.actor = GRect("actor", cs, cs, cs, cs, keyboard=True)
        # self.actor.move = Move(1, 1, 5)
        self.grid = Grid("Grid", 10, 10, 0, 0, cs, cs)
        self.grid.add_gobject(self.actor)
        self.grid.add_gobject(self.target)
        self.grid.add_gobject(self.deco)
        self.add_gobject(self.grid)


class GameHandler(GHandler):

    def __init__(self, surface, clock, **kwargs):
        super(GameHandler, self).__init__("Gritty", surface, clock, **kwargs)


def main():
    Log.Main("Gritty App").State("Init").call()
    pygame.init()
    pygame.display.set_caption("GRITTY")
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    ghandler = GameHandler(screen, clock)
    gscene = GameScene(screen)
    ghandler.add_scene(gscene)
    ghandler.hscene.active(gscene)
    while True:
        clock.tick(30)
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         pygame.quit()
        #         sys.exit(0)
        ghandler.event_handler()

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
