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
BSIZE = 16
THRESHOLD = 5
pieces = [
    [[1, 0, 0], [1, 1, 0], [1, 0, 0]],
    [[0, 1, 0], [0, 1, 0], [0, 1, 0]],
    [[1, 0, 0], [1, 0, 0], [1, 1, 0]],
    [[1, 1, 0], [1, 1, 0], [0, 0, 0]],
    [[1, 1, 0], [0, 1, 1], [0, 0, 0]],
]
score = {"lines": 0, "colors": {BLACK: 0, BLUE: 0, GREEN: 0}}
thresholds = [
    {"lines": 25, "gravity": 500},
    {"lines": 50, "gravity": 250},
    {"lines": 100, "gravity": 100},
    {"lines": 200, "gravity": 50},
]
next_piece = None


def color_to_str(color):
    if color == BLUE:
        return "BLUE"
    elif color == BLACK:
        return "BLACK"
    elif color == GREEN:
        return "GREEN"
    elif color == RED:
        return "RED"
    elif color == WHITE:
        return "WHITE"
    else:
        return "NONE"


def message_display(screen, text, pos):
    # font = pygame.font.Font("freesansbold.ttf", 20)
    font = pygame.font.SysFont("courier", 20)
    text_surf = font.render(text, True, (0, 0, 0))
    text_rect = text_surf.get_rect()
    text_rect.center = (pos.x, pos.y)
    screen.blit(text_surf, text_rect)


def new_piece(pos, dx, dy, colors, the_piece=None):
    piece = the_piece if the_piece else random.choice(pieces)
    global next_piece
    next_piece = random.choice(pieces)
    return create_matrix(piece, pos, dx, dy, colors)


def create_matrix(piece, pos, dx, dy, colors):
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


class Piece:
    def __init__(self, gobject, **kwargs):
        self.gobject = gobject

    def render(self, surface, **kwargs):
        return self.gobject.render(surface, **kwargs)


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

    def delete_for_color(self, color):
        for cell in self.cells:
            if cell.content.color == color:
                cell.status = "deleted"

    def check_for_rows(self):
        score = []
        result = {}
        indexes = []
        for pos in self.pos:
            result.setdefault(pos.y, []).append(pos)
        if min(result.keys()) < THRESHOLD:
            return None, True
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
        return score, False

    def check_board(self):
        to_delete = {}
        for i, cell in enumerate(self.cells):
            if cell.status == "deleted":
                to_delete[self.pos[i]] = (i, cell)
        result = {}
        for pos in self.pos:
            result.setdefault(pos.x, []).append(pos)
        step = 0
        for k, v in result.items():
            if k == self.y:
                continue
            for entry in sorted(v, key=lambda p: p.y, reverse=True):
                if pos in to_delete.keys():
                    step += 1
                elif step:
                    pos.y += step
        top = len(self.pos) - 1
        bottom = -1
        for i in range(top, bottom, -1):
            if self.cell[i].status == "deleted":
                del self.cell[i]
                del self.pos[i]


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
            matrix = new_piece(
                Point(6, 2), BSIZE, BSIZE, [BLACK, BLUE, GREEN], next_piece
            )
            line_score, threshold = floor.check_for_rows()
            if threshold:
                return None, threshold
            if line_score:
                global score
                score["lines"] += 1
                for key, value in {
                    k: line_score.count(k) for k in set(line_score)
                }.items():
                    score["colors"][key] += value
                # print(score)
            return Actor("piece", matrix), False
    else:
        collision = actor_box.collision_with(board_box)
        if collision:
            actor.back()
    return None, False


def main():
    global GRAVITY_TIMEOUT
    pygame.init()
    pygame.display.set_caption("PY-TRES")
    screen = pygame.display.set_mode((500, 400))
    clock = pygame.time.Clock()
    matrix = new_piece(Point(6, 2), BSIZE, BSIZE, [BLACK, BLUE, GREEN], None)
    player = Actor("piece", matrix)
    board = Board(2, 2, 10, 20, BSIZE)
    floor = Floor(3, 21, 8, 1, BSIZE)
    next_p = Piece(create_matrix(next_piece, Point(20, 2), BSIZE, BSIZE, [RED]))
    pygame.key.set_repeat(100, 100)
    pygame.time.set_timer(GRAVITY_EVENT, GRAVITY_TIMEOUT)
    enable_keys = True
    end_game = False
    level = 0
    while True:
        clock.tick(30)
        allow_space = True
        trigger_action = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == GRAVITY_EVENT:
                player.move(0, 1)
                allow_space = False
            elif event.type == pygame.KEYDOWN:
                if enable_keys:
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
                    if event.key == pygame.K_q:
                        floor.delete_for_color(BLACK)
                        trigger_action = True
                    if event.key == pygame.K_w:
                        floor.delete_for_color(BLUE)
                        trigger_action = True
                    if event.key == pygame.K_e:
                        floor.delete_for_color(GREEN)
                        trigger_action = True

        # Clear the screen
        screen.fill(WHITE)

        if not end_game:
            # Update/Move Objects
            new_player, threshold = check_collision(player, board, floor)
            if threshold:
                end_game = True
                pygame.time.set_timer(GRAVITY_EVENT, 0)
                enable_keys = False
                # pygame.quit()
                # exit(0)
            elif new_player:
                player = new_player
                next_p = Piece(
                    create_matrix(next_piece, Point(20, 2), BSIZE, BSIZE, [RED])
                )

            if trigger_action:
                floor.check_board()

        # Draw objects
        board.render(screen, RED)
        floor.render(screen, RED)
        # threshold at y= 4 * BSIZE
        for x in range(8):
            pygame.draw.line(
                screen,
                BLACK,
                ((4 + x) * BSIZE, (THRESHOLD) * BSIZE),
                ((4 + x) * BSIZE, (THRESHOLD + 16) * BSIZE),
                1,
            )
        for y in range(16):
            pygame.draw.line(
                screen,
                BLACK,
                (3 * BSIZE, (THRESHOLD + y) * BSIZE),
                (11 * BSIZE, (THRESHOLD + y) * BSIZE),
                1,
            )
        pygame.draw.line(
            screen,
            RED,
            (3 * BSIZE, THRESHOLD * BSIZE),
            (11 * BSIZE, THRESHOLD * BSIZE),
            2,
        )
        if player:
            player.render(screen)
        pygame.draw.rect(
            screen, BLACK, (19 * BSIZE, 1 * BSIZE, 5 * BSIZE, 5 * BSIZE), 2
        )
        next_p.render(screen)
        # if level == 0 and score["lines"] > thresholds[level]["lines"]:
        #     level = 1
        # elif level == 1 and score["lines"] > thresholds[level]["lines"]:
        #     level = 2
        # elif level == 2 and score["lines"] > thresholds[level]["lines"]:
        #     level = 3
        # elif level == 3 and score["lines"] > thresholds[level]["lines"]:
        #     level = 4
        if level < len(thresholds) and score["lines"] > thresholds[level]["lines"]:
            level += 1
            GRAVITY_TIMEOUT = thresholds[level]["gravity"]
            pygame.time.set_timer(GRAVITY_EVENT, GRAVITY_TIMEOUT)

        message_display(
            screen, f"Lines: {score['lines']}", Point(20 * BSIZE, 10 * BSIZE)
        )
        message_display(
            screen, f"Black: {score['colors'][BLACK]}", Point(20 * BSIZE, 11 * BSIZE)
        )
        message_display(
            screen, f"Blue : {score['colors'][BLUE]}", Point(20 * BSIZE, 12 * BSIZE)
        )
        message_display(
            screen, f"Green: {score['colors'][GREEN]}", Point(20 * BSIZE, 13 * BSIZE)
        )
        if end_game:
            message_display(screen, "END GAME", Point(20 * BSIZE, 18 * BSIZE))

        # Update the screeen
        pygame.display.flip()
        # pygame.display.update()


if __name__ == "__main__":
    main()
