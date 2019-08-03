import sys
import os
import random

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
from point import Point
from collision import CollisionBox


WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
SNAKE_UPDATE = pygame.USEREVENT + 1
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


class Move:

    NONE: int = 0
    UP: int = 1
    RIGHT: int = 3
    DOWN: int = 2
    LEFT: int = 4

    @staticmethod
    def allowed(move, to_move):
        if (move in [Move.UP, Move.DOWN]) and (to_move in [Move.UP, Move.DOWN]):
            return False
        elif (move in [Move.LEFT, Move.RIGHT]) and (to_move in [Move.LEFT, Move.RIGHT]):
            return False
        return True

    @staticmethod
    def left_or_right():
        return random.choice([Move.RIGHT, Move.LEFT])

    @staticmethod
    def up_or_down():
        return random.choice([Move.DOWN, Move.UP])

    @staticmethod
    def any():
        return random.choice([Move.DOWN, Move.UP, Move.LEFT, Move.RIGHT])


class Link:
    def __init__(self, sprite, pos=None, move=Move.NONE, pushed=False):
        self.sprite = sprite
        self.move = move
        self.pushed = pushed
        self.gsize = self.sprite.width
        self.pos = Point(self.sprite.x, self.sprite.y) if pos is None else pos
        self.sprite.x = self.pos.x * self.gsize
        self.sprite.y = self.pos.y * self.gsize

    @property
    def y(self):
        return self.pos.y

    @y.setter
    def y(self, val):
        self.pos.y = val

    @property
    def x(self):
        return self.pos.x

    @x.setter
    def x(self, val):
        self.pos.x = val

    def render(self, surface, color=BLACK):
        self.sprite.y = self.pos.y * self.gsize
        self.sprite.x = self.pos.x * self.gsize
        pygame.draw.rect(surface, color, self.sprite)


class Entity:
    def __init__(self):
        self.shape = []
        self.timeout = 0

    @property
    def head(self):
        if len(self.shape):
            return self.shape[0]
        return None

    def add(self, link):
        self.shape.append(link)
        return self

    def update(self, timeout):
        return True

    def get_collision_box(self):
        collision_box = CollisionBox()
        collision_box.add(self.head.pos)
        return collision_box

    def render(self, surface, color):
        for link in self.shape:
            link.render(surface, color)


class Chain:
    def __init__(self, length, sprite):
        self.sprite = sprite
        self.timeout = 0
        self.shape = []
        for _ in range(length):
            self.shape.append(Link(sprite))

    @property
    def head(self):
        if len(self.shape):
            return self.shape[0]
        return None

    def start_at(self, move, start_pos):
        for link in self.shape:
            link.x = start_pos.x
            link.y = start_pos.y
            link.move = move
            link.pushed = False
            start_pos.x -= 1

    def add_link(self, sprite=None):
        sprite = self.sprite if sprite is None else sprite
        new_link = Link(sprite)
        last_link = self.shape[-1]
        new_link.move = last_link.move
        if new_link.move == Move.UP:
            new_link.pos = Point(last_link.x, last_link.y + 1)
        elif new_link.move == Move.DOWN:
            new_link.pos = Point(last_link.x, last_link.y - 1)
        elif new_link.move == Move.RIGHT:
            new_link.pos = Point(last_link.x - 1, last_link.y)
        elif new_link.move == Move.LEFT:
            new_link.pos = Point(last_link.x + 1, last_link.y)
        self.shape.append(new_link)

    def update(self):
        pushed = False
        pushed_move = Move.NONE
        next_pushed = False
        next_pushed_move = Move.NONE
        for link in self.shape:
            if link.move == Move.UP:
                link.y = link.y - 1
            elif link.move == Move.DOWN:
                link.y = link.y + 1
            elif link.move == Move.RIGHT:
                link.x = link.x + 1
            elif link.move == Move.LEFT:
                link.x = link.x - 1
            else:
                pass
            if link.pushed:
                next_pushed = link.pushed
                next_pushed_move = link.move
            else:
                next_pushed = False
                next_pushed_move = Move.NONE
            if pushed:
                link.pushed = True
                link.move = pushed_move
            else:
                link.pushed = False
            pushed = next_pushed
            pushed_move = next_pushed_move

    def check_collision(self, board):
        achain_collision_box = self.get_collision_box()
        board_collision_box = board.get_collision_box()
        if achain_collision_box.collision_with(board_collision_box):
            self.back()
            self.update()

    def check_rock(self, rock):
        self_collision_box = self.get_collision_box()
        rock_collision_box = rock.get_collision_box()
        if self_collision_box.collision_with(rock_collision_box):
            self.add_link()
            return True
        return False

    def back(self):
        if self.head.move == Move.UP:
            self.move_to(Move.DOWN, forced=True)
        elif self.head.move == Move.DOWN:
            self.move_to(Move.UP, forced=True)
        elif self.head.move == Move.RIGHT:
            self.move_to(Move.LEFT, forced=True)
        elif self.head.move == Move.LEFT:
            self.move_to(Move.RIGHT, forced=True)

    def move_to(self, move, forced=True):
        if forced or Move.allowed(self.head.move, move):
            self.head.pushed = True
            self.head.move = move

    def get_collision_box(self):
        collision_box = CollisionBox()
        x = self.head.x
        y = self.head.y
        # if self.head.move == Move.UP:
        #     y -= 1
        # elif self.head.move == Move.DOWN:
        #     y += 1
        # elif self.head.move == Move.RIGHT:
        #     x += 1
        # elif self.head.move == Move.LEFT:
        #     x -= 1
        collision_box.add(Point(x, y))
        return collision_box

    # def wall_collision(self, max_y, max_x):
    #     if (self.head.move == Move.UP) and (self.head.y == 1):
    #         if self.head.x == 1:
    #             self.move_to(Move.RIGHT)
    #         else:
    #             self.move_to(Move.left_or_right())
    #         return True
    #     elif (self.head.move == Move.DOWN) and (self.head.y == max_y - 2):
    #         if self.head.x == 1:
    #             self.move_to(Move.RIGHT)
    #         else:
    #             self.move_to(Move.left_or_right())
    #         return True
    #     elif (self.head.move == Move.LEFT) and (self.head.x == 1):
    #         if self.head.y == 1:
    #             self.move_to(Move.DOWN)
    #         else:
    #             self.move_to(Move.up_or_down())
    #         return True
    #     elif (self.head.move == Move.RIGHT) and (self.head.x == max_x - 2):
    #         if self.head.y == 1:
    #             self.move_to(Move.DOWN)
    #         else:
    #             self.move_to(Move.up_or_down())
    #         return True
    #     return False

    # def check_collision(self, screen, collisions):
    #     obj = chr(screen.inch(self.head.y, self.head.x) & 255)
    #     if obj in collisions:
    #         self.add_link()
    #         return obj
    #     return None

    def render(self, surface, color):
        for link in self.shape:
            link.render(surface, color)


class Board:
    def __init__(self, x, y, xsize, ysize, gsize):
        self.x = x
        self.y = y
        self.dx = xsize
        self.dy = ysize
        self.gsize = gsize
        self.pos = []
        for x in range(self.dx):
            self.pos.append(Point(self.x + x, self.y))
            self.pos.append(Point(self.x + x, self.y + self.dy))
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
        for x in range(self.dx):
            pygame.draw.line(
                surface,
                RED,
                ((self.x + x) * BSIZE, (self.y * BSIZE)),
                ((self.x + x) * BSIZE, (self.y + self.dy) * BSIZE),
                1,
            )
        for y in range(self.dy):
            pygame.draw.line(
                surface,
                RED,
                (self.x * BSIZE, (self.y + y) * BSIZE),
                ((self.x + self.dx) * BSIZE, (self.y + y) * BSIZE),
                1,
            )


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
    return None, False


def main():
    global GRAVITY_TIMEOUT
    pygame.init()
    pygame.display.set_caption("SNAKE")
    screen = pygame.display.set_mode((600, 400))
    clock = pygame.time.Clock()
    board = Board(2, 2, 30, 20, BSIZE)
    x = random.randint(3, 30)
    y = random.randint(3, 20)
    rock = Entity().add(Link(pygame.Rect(x, y, 16, 16)))
    achain = Chain(1, pygame.Rect(5, 5, 16, 16))
    achain.start_at(Move.RIGHT, Point(5, 5))
    pygame.key.set_repeat(500, 500)
    enable_keys = True
    allow_space = False
    end_game = False
    # level = 0
    pygame.time.set_timer(SNAKE_UPDATE, 250)
    while True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == SNAKE_UPDATE:
                achain.update()
            elif event.type == pygame.KEYDOWN:
                if enable_keys:
                    if event.key == pygame.K_LEFT:
                        achain.move_to(Move.LEFT)
                    if event.key == pygame.K_RIGHT:
                        achain.move_to(Move.RIGHT)
                    if event.key == pygame.K_UP:
                        achain.move_to(Move.UP)
                    if event.key == pygame.K_DOWN:
                        achain.move_to(Move.DOWN)
                    if allow_space and event.key == pygame.K_SPACE:
                        pass

        # Clear the screen
        screen.fill(WHITE)

        if not end_game:
            pass

        # achain.update(5, board)
        achain.check_collision(board)
        if achain.check_rock(rock):
            x = random.randint(3, 30)
            y = random.randint(3, 20)
            rock = Entity().add(Link(pygame.Rect(x, y, 16, 16)))

        # Draw objects
        achain.render(screen, BLUE)
        if end_game:
            message_display(screen, "END GAME", Point(20 * BSIZE, 18 * BSIZE))
        rock.render(screen, BLACK)
        board.render(screen, RED)

        # Update the screeen
        pygame.display.flip()
        # pygame.display.update()


if __name__ == "__main__":
    main()
