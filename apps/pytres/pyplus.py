import sys
import os
import random

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
from pyplay import GHandler, Scene, Move, Point, Color, GEvent
from pyplay.gobject import Board, GRect, GCircle, GText, GPolygon

from logging import FileHandler
from tools.loggar import get_loggar

log = get_loggar("pyplus", handler=FileHandler("loggar.log", mode="w"))


class Actor(GPolygon):
    def __init__(self, **kwargs):
        points = [
            Point(100, 100),
            Point(100, 90),
            Point(110, 90),
            Point(120, 80),
            Point(130, 90),
            Point(140, 90),
            Point(140, 100),
        ]
        super(Actor, self).__init__("actor", points, **kwargs)
        # self.scale(50, 50)

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
            gev = pygame.event.Event(
                GEvent.CREATE,
                source=self,
                klass="bullet",
                at=Point(self.content.centerx, self.content.centery, -1),
                move=Move(0, -5),
            )
            pygame.event.post(gev)


class Bullet(GCircle):
    def __init__(self, x, y, radius, parent, **kwargs):
        super(Bullet, self).__init__("bullet", x, y, radius, **kwargs)
        self.parent = parent

    def out_of_bounds_x_response(self):
        gev = pygame.event.Event(GEvent.DELETE, source=self)
        pygame.event.post(gev)
        return True

    def out_of_bounds_y_response(self):
        gev = pygame.event.Event(GEvent.DELETE, source=self)
        pygame.event.post(gev)
        return True

    def collide_with(self, other):
        if other != self.parent:
            del_self = pygame.event.Event(GEvent.DELETE, source=self)
            del_other = pygame.event.Event(GEvent.DELETE, source=other)
            pygame.event.post(del_self)
            pygame.event.post(del_other)


class GameBoard(Board):
    def __init__(self, name, x, y, dx, dy, **kwargs):
        super(GameBoard, self).__init__(name, x, y, dx, dy, **kwargs)

    def handle_custom_event(self, event):
        """handle_custom_event should process pygame custom event given.
        Any object in the game, like, scene, graphic objects, ... can post
        customs events, and those should be handled at this time.
        """
        if event.type == GEvent.CREATE:
            # log.Board(self.name).Create(event.klass).At(f"{event.at}").call()
            bullet = Bullet(
                event.at.x, event.at.y, 2, event.source, z=event.at.z, move=event.move
            )
            self.add_gobject(bullet)
        elif event.type == GEvent.DELETE:
            log.Board(self.name).Delete(event.source).call()
            gobj = event.source
            if gobj in self.gobjects:
                self.gobjects.remove(gobj)


def main():
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption("PY-PLUS")
    surface = pygame.display.set_mode((600, 400))
    clock = pygame.time.Clock()
    # -> Create game handler, scenes and graphical objects.
    gh = GHandler("app", surface)
    scene = Scene("main", surface)
    board = GameBoard("board", 0, 0, 600, 300, outline=1)
    # Generate balls and squares
    for _ in range(10):
        x = random.randint(50, 500)
        y = random.randint(50, 200)
        size = random.randint(10, 50)
        speed_x = random.randint(1, 5)
        speed_y = random.randint(1, 5)
        selection = random.choice(["rect", "circle"])
        if selection == "rect":
            obj = GRect(
                "rect",
                x,
                y,
                size,
                size,
                move=Move(speed_x, speed_y),
                color=Color.RED,
                outline=2,
            )
            board.add_gobject(obj)
        else:
            obj = GCircle(
                "circle",
                x,
                y,
                size,
                move=Move(speed_x, speed_y),
                color=Color.GREEN,
                outline=2,
            )
            board.add_gobject(obj)
    obj3 = Actor(color=Color.BLUE, z=1, outline=1)
    text = GText("text", 10, 310, "Bouncing Ball")
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
            elif event.type >= pygame.USEREVENT:
                # log.Event("Main-Loop").Create(f"{event.__dict__}").call()
                gh.handle_custom_event(event)

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
