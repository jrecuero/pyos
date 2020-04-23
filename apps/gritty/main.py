import os
import sys

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame


WHITE = (255, 255, 255)


def main():
    pygame.init()
    pygame.display.set_caption("GRITTY")
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    while True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

        # Clear the screen
        screen.fill(WHITE)

        # Update the screeen
        pygame.display.flip()


if __name__ == "__main__":
    main()
