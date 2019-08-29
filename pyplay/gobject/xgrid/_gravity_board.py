import pygame

# from ..._gevent import GEvent
from ..._loggar import log
from ._grid_board import GridBoard
from ._grid_event import GridEvent


class GravityBoard(GridBoard):
    """GravityBoard implements a board with a timer that simulates downward
    gravity.
    """

    def __init__(self, name, x, y, dx, dy, xsize, ysize=None, **kwargs):
        super(GravityBoard, self).__init__(name, x, y, dx, dy, xsize, ysize, **kwargs)
        self.gravity_timer = kwargs.get("gravity_timer", 1000)
        pygame.time.set_timer(GridEvent.GRAVITY, self.gravity_timer)

    def add_shape_to_play_cells(self, shape):
        """add_shape_to_play_cells adds the given shape to the play_cells
        attribute. shape will be deleted from the gobjects list and an event
        to create a new shape will be sent to pygame.
        """
        super(GravityBoard, self).add_shape_to_play_cells(shape)
        create_shape = pygame.event.Event(GridEvent.CREATE, source=None)
        pygame.event.post(create_shape)

    def check_completed_line(self):
        """check_completed_line looks at play cells if there is a full line
        completed with cells.
        """
        completed_lines = []
        for index, row in enumerate(self.play_cells[::-1]):
            if all(row):
                self.play_cells.remove(row)
                # row = []
                # for icol in range(self.dx_play_cells):
                #     row.append(None)
                # self.play_cells.insert(0, row)
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

    def update(self, surface, **kwargs):
        """update provides any functionality to be done every tick.
        """
        for shape in self.gobjects:
            shape.update(surface, **kwargs)

        # Check all shapes are not out of bounds.
        for shape in self.gobjects:
            shape_collision_box = shape.get_collision_box()
            if shape_collision_box.check_out_of_bounds(
                0, 0, self.dx_play_cells, self.dy_play_cells
            ):
                shape.back_it()
                if shape.gravity_step:
                    self.add_shape_to_play_cells(shape)

        # Check all cells for collisions, between cells or with play cells.
        for shape in self.gobjects:
            if self.get_play_collision_box().collision_with(shape.get_collision_box()):
                result = shape.back_it()
                log.GravityBoard().Shape(f"{shape}").BackIt(f"{result}").call()
                backx, backy = result[-1]
                if backy:
                    self.add_shape_to_play_cells(shape)

        # After all shapes have been checked against out of bounds and
        # collisions, it is time to process if there is a line completed.
        self.check_completed_line()
