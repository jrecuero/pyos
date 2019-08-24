import sys
import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
from pyplay import GHandler, Scene, Move, Point, Color
from pyplay.gobject import Board, GRect, GCircle, GText, GPolygon

# from logging import FileHandler
# from tools.loggar import get_loggar

# log = get_loggar("pyplus", handler=FileHandler("loggar.log", mode="w"))


class Actor(GRect):
    def __init__(self, x, y, dx, dy, **kwargs):
        super(Actor, self).__init__("actor", x, y, dx, dy, **kwargs)

    def handle_keyboard_event(self, event):
        """handle_keyboard_event should process the keyboard event given.
        """
        # log.Actor(self.name).Keydown(event).call()
        speed = 5
        if event.key == pygame.K_LEFT:
            self.move = Move(speed * (-1), 0)
        if event.key == pygame.K_RIGHT:
            self.move = Move(speed, 0)
        if event.key == pygame.K_UP:
            self.move = Move(0, speed * (-1))
        if event.key == pygame.K_DOWN:
            self.move = Move(0, speed)
        if event.key == pygame.K_SPACE:
            self.move = Move(0, 0)


def main():
    pygame.init()
    pygame.display.set_caption("PY-PLUS")
    surface = pygame.display.set_mode((600, 400))
    clock = pygame.time.Clock()
    # -> Create game handler, scenes and graphical objects.
    gh = GHandler("app", surface)
    scene = Scene("main", surface)
    board = Board("board", 0, 0, 600, 300, outline=1)
    # obj1 = GRect("rect", 100, 100, 25, 25, move=Move(5, 5), outline=1)
    obj1 = Actor(100, 100, 25, 25, outline=1)
    obj2 = GCircle("circle", 50, 50, 10, move=Move(5, 1), outline=1)
    obj3 = GPolygon(
        "pol",
        [Point(300, 100), Point(350, 50), Point(400, 100)],
        color=Color.BLUE,
        outline=1,
        move=Move(2, 3),
    )
    obj3.scale(dx=25, dy=25)
    text = GText("text", 10, 310, "Bouncing Ball")
    board.add_gobject(obj1)
    board.add_gobject(obj2)
    board.add_gobject(obj3)
    scene.add_gobject(board)
    scene.add_gobject(text)
    gh.add_scene(scene)
    gh.hscene.active()
    # <-
    while True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                gh.handle_keyboard_event(event)

        # -> update objects
        gh.update()
        # <-

        # -> render objects
        surface.fill((255, 255, 255))
        gh.render()
        pygame.display.flip()
        # <-


if __name__ == "__main__":
    main()
