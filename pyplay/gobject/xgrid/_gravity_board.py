import pygame

from ..._loggar import log
from ..._color import Color
from ._grid_board import GridBoard
from ._grid_event import GridEvent


class GravityBoard(GridBoard):
    """GravityBoard implements a board with a timer that simulates downward
    gravity.
    """

    def __init__(self, name, x, y, dx, dy, xsize, ysize=None, **kwargs):
        super(GravityBoard, self).__init__(name, x, y, dx, dy, xsize, ysize, **kwargs)
        self.gravity_timer = kwargs.get("gravity_timer", 500)
        self.threshold_level = kwargs.get("threshold", 11)
        pygame.time.set_timer(GridEvent.GRAVITY, self.gravity_timer)

    def add_shape_to_play_cells(self, shape):
        """add_shape_to_play_cells adds the given shape to the play_cells
        attribute. shape will be deleted from the gobjects list and an event
        to create a new shape will be sent to pygame.
        """
        super(GravityBoard, self).add_shape_to_play_cells(shape)

    def check_threshold_level(self):
        """check_threshold_level checks if the play cells are is over the
        threshold level. Return True if there is a piece that is over the
        threshold, False in other case.
        """
        threshold = len(self.play_cells) - self.threshold_level - 1
        for row in self.play_cells[threshold::-1]:
            if any(row):
                return True
        return False

    def check_completed_line(self):
        """check_completed_line looks at play cells if there is a full line
        completed with cells.
        """
        completed_lines = []
        for index, row in enumerate(self.play_cells[::-1]):
            if all(row):
                self.play_cells.remove(row)
                self.play_cells.insert(0, [None] * self.dx_play_cells)
                completed_lines.append((index, row))
                log.GravityBoard("Completed Line").Line(index).Row(row).call()
            else:
                for cell in [c for c in row if c]:
                    cell.move_it(0, len(completed_lines))
        if completed_lines:
            completed_event = pygame.event.Event(
                GridEvent.COMPLETED, source=completed_lines
            )
            pygame.event.post(completed_event)
        return completed_lines

    def handle_keyboard_event(self, event):
        """handle_keyboard_event should process the keyboard event given.
        """
        super(GravityBoard, self).handle_keyboard_event(event)

        # Check all shapes are not out of bounds.
        for shape in self.gobjects:
            if shape.get_collision_box().check_out_of_bounds(
                0, 0, self.dx_play_cells, self.dy_play_cells
            ):
                shape.back_it()

        # Check all cells for collisions, between cells or with play cells.
        for shape in self.gobjects:
            if self.get_play_collision_box().collision_with(shape.get_collision_box()):
                shape.back_it()

    def update(self, surface, **kwargs):
        """update provides any functionality to be done every tick.
        """
        for shape in self.gobjects:
            shape.update(surface, **kwargs)

        # Check all shapes are not out of bounds.
        for shape in self.gobjects:
            if shape.get_collision_box().check_out_of_bounds(
                0, 0, self.dx_play_cells, self.dy_play_cells
            ):
                shape.back_it()
                if shape.gravity_step:
                    self.add_shape_to_play_cells(shape)
                    create_shape = pygame.event.Event(GridEvent.CREATE, source=None)
                    pygame.event.post(create_shape)

        # Check all cells for collisions, between cells or with play cells.
        for shape in self.gobjects:
            if self.get_play_collision_box().collision_with(shape.get_collision_box()):
                result = shape.back_it()
                log.GravityBoard().Shape(f"{shape}").BackIt(f"{result}").call()
                backx, backy = result[-1]
                if backy:
                    # Check if the last piece is out of the threshold level.
                    self.add_shape_to_play_cells(shape)
                    if self.check_threshold_level():
                        pygame.time.set_timer(GridEvent.GRAVITY, 0)
                        end_event = pygame.event.Event(GridEvent.END, source=None)
                        pygame.event.post(end_event)
                        self.running = False
                    else:
                        create_shape = pygame.event.Event(GridEvent.CREATE, source=None)
                        pygame.event.post(create_shape)

        # After all shapes have been checked against out of bounds and
        # collisions, it is time to process if there is a line completed.
        self.check_completed_line()

    def render(self, surface, **kwargs):
        """render should draws the instance on the given surface.
        """
        super(GravityBoard, self).render(surface, **kwargs)
        threshold = len(self.play_cells) - self.threshold_level
        pygame.draw.line(
            self.image,
            Color.RED,
            (0, threshold * self.ysize),
            (self.dx, threshold * self.ysize),
            5,
        )
