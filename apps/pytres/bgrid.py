import sys
import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
from pyplay import GHandler, Scene, Color
from pyplay.gobject import GText
from pyplay.gobject.grid import GridBoard, GridRect


class Actor(GridRect):
    def __init__(self, x, y, **kwargs):
        super(Actor, self).__init__("actor", x, y, 50, 50, **kwargs)

    def handle_keyboard_event(self, event):
        """handle_keyboard_event should process the keyboard event given.
        """
        speed = 50
        if event.key == pygame.K_LEFT:
            self.move_inc(speed * (-1), 0)
            self.gridx -= 1
        if event.key == pygame.K_RIGHT:
            self.move_inc(speed, 0)
            self.gridx += 1
        if event.key == pygame.K_UP:
            self.move_inc(0, speed * (-1))
            self.gridy -= 1
        if event.key == pygame.K_DOWN:
            self.move_inc(0, speed)
            self.gridy += 1


def main():
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption("B-GRID")
    surface = pygame.display.set_mode((600, 500))
    clock = pygame.time.Clock()
    # -> Create game handler, scenes and graphical objects.
    gh = GHandler("app", surface)
    scene = Scene("main", surface)
    board = GridBoard("board", 50, 50, 500, 400, 50, outline=1)
    actor = Actor(0, 0, color=Color.BLUE)
    board.add_gobject(actor)
    text = GText("text", 10, 460, "loading...")
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
        text.message = f"({actor.gridx}, {actor.gridy})"
        # <-

        # -> render objects
        surface.fill((255, 255, 255))
        gh.render()
        pygame.display.flip()
        # <-


if __name__ == "__main__":
    main()
