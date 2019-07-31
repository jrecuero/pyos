import sys
import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
from point import Point
from collision import CollisionBox
from content import Content
from cell import Cell
from matrix import Matrix


WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAVITY_EVENT = pygame.USEREVENT + 1
GRAVITY_TIMEOUT = 1000
BSIZE = 20


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


class Board:
    def __init__(self, x, y, xsize, ysize, gsize):
        self.x = x
        self.y = y
        self.dx = xsize
        self.dy = ysize
        self.gsize = gsize
        self.pos = []
        for y in range(self.dy):
            self.pos.append(Point(self.x, self.y + y))
            self.pos.append(Point(self.x + self.dx - 1, self.y + y))

    def gx(self, x):
        return x * self.gsize

    def gy(self, y):
        return y * self.gsize

    def grect(self, x, y):
        return (self.gx(x), self.gy(y), self.gsize, self.gsize)

    def add_pos(self, pos):
        self.pos.extend(pos)

    def get_collision_box(self):
        collision_box = CollisionBox()
        for p in self.pos:
            collision_box.add(p)
        return collision_box

    def render(self, surface, color, **kwargs):
        for p in self.pos:
            pygame.draw.rect(surface, color, self.grect(p.x, p.y))


class Floor:
    def __init__(self, x, y, xsize, ysize, gsize):
        self.x = x
        self.y = y
        self.dx = xsize
        self.dy = ysize
        self.gsize = gsize
        self.floor = True
        self.pos = []
        for x in range(self.dx):
            self.pos.append(Point(self.x + x, self.y))

    def gx(self, x):
        return x * self.gsize

    def gy(self, y):
        return y * self.gsize

    def grect(self, x, y):
        return (self.gx(x), self.gx(y), self.gsize, self.gsize)

    def add_pos(self, pos):
        self.pos.extend(pos)

    def get_collision_box(self):
        collision_box = CollisionBox()
        for p in self.pos:
            collision_box.add(p)
        return collision_box

    def render(self, surface, color, **kwargs):
        for p in self.pos:
            rect = self.grect(p.x, p.y)
            pygame.draw.rect(surface, color, rect)


class Actor:
    def __init__(self, name, gobject, **kwargs):
        self.name = name
        self.gobject = gobject
        self.back_move = {}

    def move(self, x, y):
        self.back_move = {"move": (x, y)}
        return self.gobject.move(x, y)

    def rotate(self, direction="clockwise"):
        self.back_move = {"rotate": direction}
        if direction == "clockwise":
            self.gobject = self.gobject.rotate_clockwise()
        else:
            self.gobject = self.gobject.rotate_anticlockwise()

    def render(self, surface, **kwargs):
        return self.gobject.render(surface, **kwargs)

    def back(self):
        for key, value in self.back_move.items():
            if key == "move":
                self.move(*[-1 * v for v in value])
            elif key == "rotate":
                if value == "clockwise":
                    self.gobject = self.gobject.rotate_anticlockwise()
                else:
                    self.gobject = self.gobject.rotate_clockwise()


def check_collision(actor, board, floor):
    actor_box = actor.gobject.get_collision_box()
    board_box = board.get_collision_box()
    floor_box = floor.get_collision_box()
    collision = actor_box.collision_with(floor_box)
    if collision:
        actor.back()
        actor_box = actor.gobject.get_collision_box()
        if actor_box.collision_with_upper(collision):
            pos_to_add = actor.gobject.get_pos()
            floor.add_pos(pos_to_add)
            matrix = create_matrix(Point(8, 2), BSIZE, BSIZE, BLUE)
            return Actor("piece", matrix)
    else:
        collision = actor_box.collision_with(board_box)
        if collision:
            actor.back()
    return actor


def main():
    pygame.init()
    pygame.display.set_caption("PY-TRES")
    screen = pygame.display.set_mode((500, 400))
    clock = pygame.time.Clock()
    matrix = create_matrix(Point(8, 2), BSIZE, BSIZE, BLUE)
    player = Actor("piece", matrix)
    board = Board(2, 2, 10, 14, BSIZE)
    floor = Floor(2, 16, 10, 10, BSIZE)
    # waiting = False
    pygame.key.set_repeat(100, 100)
    pygame.time.set_timer(GRAVITY_EVENT, GRAVITY_TIMEOUT)
    while True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.move(-1, 0)
                if event.key == pygame.K_RIGHT:
                    player.move(1, 0)
                if event.key == pygame.K_UP:
                    player.rotate()
                if event.key == pygame.K_DOWN:
                    player.rotate("anticlockwise")
            elif event.type == GRAVITY_EVENT:
                player.move(0, 1)

        # Clear the screen
        screen.fill(WHITE)

        # Update/Move Objects
        player = check_collision(player, board, floor)

        # Draw objects
        # screen.blit(rot, (100, 100))
        board.render(screen, RED)
        floor.render(screen, RED)
        player.render(screen)

        # Update the screeen
        pygame.display.flip()
        # pygame.display.update()


if __name__ == "__main__":
    main()
