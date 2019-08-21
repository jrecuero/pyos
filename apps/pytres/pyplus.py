import sys
import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
from pyplay import GameHandler


def main():
    pygame.init()
    pygame.display.set_caption("PY-PLUS")
    surface = pygame.display.set_mode((600, 400))
    clock = pygame.time.Clock()
    gh = GameHandler("app", surface)
    while True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

        # update objects
        gh.update()

        # render objects
        surface.fill((255, 255, 255))
        gh.render()
        pygame.display.flip()


if __name__ == "__main__":
    main()
