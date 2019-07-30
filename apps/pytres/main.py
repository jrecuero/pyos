import sys
import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
from content import Content
from cell import Cell
from matrix import Matrix


WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)


def create_matrix(pos, dx, dy, color):
    figure = [[1, 0, 0], [1, 1, 0], [1, 0, 0]]
    mat = []
    for row in figure:
        rows = []
        for col in row:
            cell = Cell(Content(dx, dy, color))
            if not col:
                cell.disable()
            rows.append(cell)
        mat.append(rows)
    return Matrix(mat, pos, dx, dy)


def draw(surface, x, y):
    pygame.draw.rect(surface, BLUE, (x, y, 100, 50), 1)


def main():
    pygame.init()
    pygame.display.set_caption("PY-TRES")
    screen = pygame.display.set_mode((500, 400))
    clock = pygame.time.Clock()
    x, y = 0, 0
    incr = 1
    angle = 0
    rect = pygame.Surface((100, 100))
    while True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

        # Clear the screen
        screen.fill(WHITE)

        # Check input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            incr = -1
        if keys[pygame.K_RIGHT]:
            incr = 1

        x += incr
        y += incr
        angle += 1

        # Update/Move Objects

        # Draw objects
        rect.fill(RED)
        pygame.draw.rect(rect, WHITE, (0, 0, 100, 100), 1)
        rot = pygame.transform.rotate(rect, angle)
        rot_rect = rot.get_rect()
        # screen.blit(rot, (100, 100))
        screen.blit(rot, rot_rect)
        draw(screen, x, y)

        # Update the screeen
        pygame.display.flip()
        # pygame.display.update()


if __name__ == "__main__":
    main()
