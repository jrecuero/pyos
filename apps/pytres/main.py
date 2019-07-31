import sys
import os
import random

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
from point import Point
from collision import CollisionBox
from content import Content
from cell import Cell
from matrix import Matrix


WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAVITY_EVENT = pygame.USEREVENT + 1
GRAVITY_TIMEOUT = 1000
BSIZE = 20
pieces = [
    [[1, 0, 0], [1, 1, 0], [1, 0, 0]],
    [[0, 1, 0], [0, 1, 0], [0, 1, 0]],
    [[1, 0, 0], [1, 0, 0], [1, 1, 0]],
    [[1, 1, 0], [1, 1, 0], [0, 0, 0]],
    [[1, 1, 0], [0, 1, 1], [0, 0, 0]],
]


def create_matrix(pos, dx, dy, colors):
    # piece = [[1, 0, 0], [1, 1, 0], [1, 0, 0]]
    piece = random.choice(pieces)
    mat = []
    for row in piece:
        rows = []
        for col in row:
            cell = Cell(Content(dx, dy, colors))
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
        self.cells = []
        for x in range(self.dx):
            pos = Point(self.x + x, self.y)
            self.pos.append(pos)
            gpos = Point(self.gx(pos.x), self.gy(pos.y))
            self.cells.append(Cell(Content(gsize, gsize, [RED]), pos=gpos))

    def gx(self, x):
        return x * self.gsize

    def gy(self, y):
        return y * self.gsize

    def grect(self, x, y):
        return (self.gx(x), self.gx(y), self.gsize, self.gsize)

    def add_pos(self, pos):
        self.pos.extend(pos)

    def add_cells(self, cells):
        self.cells.extend(cells)

    def get_collision_box(self):
        collision_box = CollisionBox()
        for p in self.pos:
            collision_box.add(p)
        return collision_box

    def render(self, surface, color, **kwargs):
        # for p in self.pos:
        #     rect = self.grect(p.x, p.y)
        #     pygame.draw.rect(surface, color, rect)
        # for i, cell in enumerate(self.cells):
        #     cell.render(surface)
        for i, cell in enumerate(self.cells):
            cell.render_at(surface, self.gx(self.pos[i].x), self.gy(self.pos[i].y))

    def check_for_rows(self):
        score = []
        result = {}
        indexes = []
        for pos in self.pos:
            result.setdefault(pos.y, []).append(pos)
        for k, v in result.items():
            if len(v) == self.dx and k != self.y:
                for p in v:
                    # self.pos.remove(p)
                    indexes.append(self.pos.index(p))
        for i in sorted(indexes, reverse=True):
            del self.pos[i]
            score.append(self.cells[i].content.color)
            del self.cells[i]
        step = 0
        for key in sorted(result.keys(), reverse=True):
            if key == self.y:
                continue
            entries = result[key]
            if len(entries) < self.dx and step:
                for pos in entries:
                    pos.y += step
            elif len(entries) == self.dx:
                step += 1
        return score


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
            floor.add_pos(actor.gobject.get_pos())
            floor.add_cells(actor.gobject.get_cells())
            matrix = create_matrix(Point(8, 2), BSIZE, BSIZE, [BLACK, BLUE, GREEN])
            score = floor.check_for_rows()
            # for k in set(score):
            #     print(f"{k}: {score.count(k)}")
            print({k: score.count(k) for k in set(score)})
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
    matrix = create_matrix(Point(8, 2), BSIZE, BSIZE, [BLACK, BLUE, GREEN])
    player = Actor("piece", matrix)
    board = Board(2, 2, 10, 14, BSIZE)
    floor = Floor(3, 15, 8, 1, BSIZE)
    pygame.key.set_repeat(100, 100)
    pygame.time.set_timer(GRAVITY_EVENT, GRAVITY_TIMEOUT)
    while True:
        clock.tick(30)
        allow_space = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == GRAVITY_EVENT:
                player.move(0, 1)
                allow_space = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.move(-1, 0)
                if event.key == pygame.K_RIGHT:
                    player.move(1, 0)
                if event.key == pygame.K_UP:
                    player.rotate()
                if event.key == pygame.K_DOWN:
                    player.rotate("anticlockwise")
                if allow_space and event.key == pygame.K_SPACE:
                    player.move(0, 1)

        # Clear the screen
        screen.fill(WHITE)

        # Update/Move Objects
        player = check_collision(player, board, floor)

        # Draw objects
        board.render(screen, RED)
        floor.render(screen, RED)
        player.render(screen)

        # Update the screeen
        pygame.display.flip()
        # pygame.display.update()


if __name__ == "__main__":
    main()
