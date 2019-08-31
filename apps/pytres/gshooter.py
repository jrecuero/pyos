import sys
import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
from pyplay import GHandler, Scene, Color, Move
from pyplay.gobject.xgrid import Cell, Shape, GridBoard, GridEvent


colors = [Color.BLACK, Color.BLUE, Color.GREEN, Color.RED]


class Target(Shape):
    def __init__(self, x, y, **kwargs):
        super(Target, self).__init__("target", x, y, 3, 3, 50, 50, **kwargs)
        self.add_cell(Cell("t-1", 0, 0, 50, 50, color=Color.RED))
        self.add_cell(Cell("t-1", 1, 1, 50, 50, color=Color.RED))
        self.add_cell(Cell("t-1", 2, 2, 50, 50, color=Color.RED))
        self.add_cell(Cell("t-1", 2, 0, 50, 50, color=Color.RED))
        self.add_cell(Cell("t-1", 0, 2, 50, 50, color=Color.RED))

    def collide_with(self, other, collision):
        """collide_with processes a collision with other object.
        """
        for (x, y) in collision:
            for cell in self.cells[:]:
                if x == cell.gridx and y == cell.gridy:
                    self.del_cell(cell)
        if not self.cells:
            del_self = pygame.event.Event(GridEvent.DELETE, source=self)
            pygame.event.post(del_self)


class Actor(Shape):
    def __init__(self, x, y, **kwargs):
        super(Actor, self).__init__("actor", x, y, 3, 3, 50, 50, hkey=True, **kwargs)
        self.add_cell(Cell("c-1", 1, 0, 50, 50, color=Color.BLUE))
        self.add_cell(Cell("c-2", 0, 1, 50, 50, color=Color.BLUE))
        self.add_cell(Cell("c-3", 1, 1, 50, 50, color=Color.BLUE))
        self.add_cell(Cell("c-4", 2, 1, 50, 50, color=Color.BLUE))

    def handle_keyboard_event(self, event):
        """handle_keyboard_event should process the keyboard event given.
        """
        if not self.allow_key_handle:
            return
        self.gravity_step = False
        if event.key == pygame.K_LEFT:
            self.move_it(-1, 0)
        if event.key == pygame.K_RIGHT:
            self.move_it(1, 0)
        if event.key == pygame.K_UP:
            self.move_it(0, -1)
        if event.key == pygame.K_DOWN:
            self.move_it(0, 1)
        if event.key == pygame.K_SPACE:
            create_bullet = pygame.event.Event(
                GridEvent.CREATE,
                source="bullet",
                posx=self.gridx + 1,
                posy=self.gridy - 1,
            )
            pygame.event.post(create_bullet)


class GameBoard(GridBoard):
    """GameBoard implements all custom functionality for the game board being
    played.
    """

    # def __init__(self, name, x, y, dx, dy, xsize, ysize=None, **kwargs):
    #     super(GameBoard, self).__init__(name, x, y, dx, dy, xsize, ysize, **kwargs)

    def handle_custom_event(self, event):
        """handle_custom_event should process pygame custom event given.
        Any object in the game, like, scene, graphic objects, ... can post
        customs events, and those should be handled at this time.
        """
        # First we have to handle the event before calling the super, because
        # some object could be added or created at this time.
        if event.type == GridEvent.CREATE:
            if event.source == "bullet":
                bullet = Shape(
                    "bullet",
                    event.posx,
                    event.posy,
                    1,
                    1,
                    50,
                    50,
                    move=Move(0, -10),
                    transient=True,
                )
                bullet.add_cell(Cell("bullet", 0, 0, 50, 50))
                self.add_gobject(bullet)
        elif event.type == GridEvent.DELETE:
            if event.source in self.gobjects:
                self.del_gobject(event.source)
        super(GameBoard, self).handle_custom_event(event)


class GameHandler(GHandler):
    """GameHandler implements all custom functionality for the actual game.
    """

    def __init__(self, name, surface, **kwargs):
        super(GameHandler, self).__init__(name, surface, **kwargs)
        self.total_lines = 0
        self.console = None
        self.color_cells = {
            Color.color_to_str(Color.BLACK): 0,
            Color.color_to_str(Color.BLUE): 0,
            Color.color_to_str(Color.RED): 0,
            Color.color_to_str(Color.GREEN): 0,
        }


def _create_game(surface):
    """_create_game creates all custom instances required for handling the
    actual game implementation.
    """
    gh = GameHandler("app", surface)
    scene = Scene("main", surface)
    board = GameBoard("grid-board", 50, 50, 450, 700, 50, outline=1)
    actor = Actor(3, 11)
    board.add_gobject(actor)
    target = Target(3, 1)
    board.add_gobject(target)
    scene.add_gobject(board)
    gh.add_scene(scene)
    gh.hscene.active()
    return gh


def main():
    """main implements the full game application.
    """
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption("B-GRID")
    surface = pygame.display.set_mode((550, 800))
    clock = pygame.time.Clock()
    # -> Create game handler, scenes and graphical objects.
    gh = _create_game(surface)
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
                gh.handle_custom_event(event)

        # -> update objects
        gh.update()
        # text.message = f"({actor.gridx}, {actor.gridy})"
        # <-

        # -> render objects
        surface.fill((255, 255, 255))
        gh.render()
        pygame.display.flip()
        # <-


if __name__ == "__main__":
    main()
