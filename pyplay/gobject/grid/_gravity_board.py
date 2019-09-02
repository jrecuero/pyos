import pygame

from ..._loggar import log
from ..._color import Color
from ..._gevent import GEvent
from ._grid_board import GridBoard


class GravityBoard(GridBoard):
    """GravityBoard implements a board with a timer that simulates downward
    gravity.
    """

    def __init__(self, name, x, y, dx, dy, xsize, ysize=None, **kwargs):
        super(GravityBoard, self).__init__(name, x, y, dx, dy, xsize, ysize, **kwargs)
        self.gravity_timer = kwargs.get("gravity_timer", 500)
        self.threshold_level = kwargs.get("threshold", 11)
        pygame.time.set_timer(GEvent.T_GRAVITY, self.gravity_timer)

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
                GEvent.ENGINE, subtype=GEvent.COMPLETED, source=completed_lines
            )
            pygame.event.post(completed_event)
        return completed_lines

    # def handle_keyboard_event(self, event):
    #     """handle_keyboard_event should process the keyboard event given.
    #     """
    #     super(GravityBoard, self).handle_keyboard_event(event)
    #     # Check all shapes are not out of bounds.
    #     for shape in self.gobjects:
    #         if shape.get_collision_box().check_out_of_bounds(
    #             0, 0, self.dx_play_cells, self.dy_play_cells
    #         ):
    #             shape.back_it()
    #             # TODO: To Be Tested if this resolve the problem with merging
    #             # pieces when they are being rotated and getting out of bounds.
    #             # if shape.get_collision_box().check_out_of_bounds(
    #             #     0, 0, self.dx_play_cells, self.dy_play_cells
    #             # ):
    #             #     shape.move_it(0, -1)
    #
    #     # Check all cells for collisions, between cells or with play cells.
    #     for shape in self.gobjects:
    #         if self.get_play_collision_box().collision_with(shape.get_collision_box()):
    #             shape.back_it()

    def handle_custom_event(self, event):
        """handle_custom_event should process pygame custom event given.
        Any object in the game, like, scene, graphic objects, ... can post
        customs events, and those should be handled at this time.
        """
        if event.type == GEvent.ENGINE and event.subtype == GEvent.END:
            pygame.time.set_timer(GEvent.T_GRAVITY, 0)
            self.running = False
        super(GravityBoard, self).handle_custom_event(event)

    def handle_add_shape_to_play_cells(self):
        if self.check_threshold_level():
            # pygame.time.set_timer(GEvent.T_GRAVITY, 0)
            # self.running = False
            end_event = pygame.event.Event(
                GEvent.ENGINE, subtype=GEvent.END, winner="target"
            )
            pygame.event.post(end_event)
        else:
            create_shape = pygame.event.Event(
                GEvent.ENGINE, subtype=GEvent.CREATE, source=None
            )
            pygame.event.post(create_shape)
            log.Post(create_shape).call()

    def update(self, surface, **kwargs):
        """update provides any functionality to be done every tick.
        """
        for shape in self.gobjects:
            log.Update(shape.move_actions).call()
            for ma in shape.move_actions:
                ma["call"](*ma["args"])
                shape_collision_box = shape.get_collision_box()
                if shape_collision_box.check_out_of_bounds(
                    0, 0, self.dx_play_cells, self.dy_play_cells
                ):
                    shape.back_it()
                    if shape.gravity_step:
                        self.add_shape_to_play_cells(shape)
                        self.handle_add_shape_to_play_cells()
                        # if self.check_threshold_level():
                        #     pygame.time.set_timer(GEvent.T_GRAVITY, 0)
                        #     end_event = pygame.event.Event(
                        #         GEvent.ENGINE, subtype=GEvent.END, source=None
                        #     )
                        #     pygame.event.post(end_event)
                        #     self.running = False
                        # else:
                        #     create_shape = pygame.event.Event(
                        #         GEvent.ENGINE, subtype=GEvent.CREATE, source=None
                        #     )
                        #     pygame.event.post(create_shape)
                        #     log.Post(create_shape).call()
                        break

                if self.get_play_collision_box().collision_with(shape_collision_box):
                    result = shape.back_it()
                    log.GravityBoard().Shape(f"{shape}").BackIt(f"{result}").call()
                    result_set = list(set(result))
                    backx, backy = result[-1]
                    # if backy:
                    if len(result_set) == 1 and backy:
                        log.Result(result).call()
                        # Check if the last piece is out of the threshold level.
                        self.add_shape_to_play_cells(shape)
                        self.handle_add_shape_to_play_cells()
                        # if self.check_threshold_level():
                        #     pygame.time.set_timer(GEvent.T_GRAVITY, 0)
                        #     end_event = pygame.event.Event(
                        #         GEvent.ENGINE, subtype=GEvent.END, source=None
                        #     )
                        #     pygame.event.post(end_event)
                        #     self.running = False
                        # else:
                        #     create_shape = pygame.event.Event(
                        #         GEvent.ENGINE, subtype=GEvent.CREATE, source=None
                        #     )
                        #     pygame.event.post(create_shape)
                        #     log.Post(create_shape).call()
                        break

        for shape in self.gobjects:
            shape.update(surface, **kwargs)

        # # Check all shapes are not out of bounds.
        # for shape in self.gobjects:
        #     if shape.get_collision_box().check_out_of_bounds(
        #         0, 0, self.dx_play_cells, self.dy_play_cells
        #     ):
        #         shape.back_it()
        #         if shape.gravity_step:
        #             # -> TODO: To Be Tested if resolve out of bounds pieces.
        #             if shape.get_collision_box().check_out_of_bounds(
        #                 0, 0, self.dx_play_cells, self.dy_play_cells
        #             ):
        #                 shape.move_it(0, -1)
        #             # <-
        #             self.add_shape_to_play_cells(shape)
        #             create_shape = pygame.event.Event(
        #                 GEvent.ENGINE, subtype=GEvent.CREATE, source=None
        #             )
        #             pygame.event.post(create_shape)
        #
        # # Check all cells for collisions, between cells or with play cells.
        # for shape in self.gobjects:
        #     if self.get_play_collision_box().collision_with(shape.get_collision_box()):
        #         result = shape.back_it()
        #         log.GravityBoard().Shape(f"{shape}").BackIt(f"{result}").call()
        #         backx, backy = result[-1]
        #         if backy:
        #             # Check if the last piece is out of the threshold level.
        #             self.add_shape_to_play_cells(shape)
        #             if self.check_threshold_level():
        #                 pygame.time.set_timer(GEvent.T_GRAVITY, 0)
        #                 end_event = pygame.event.Event(
        #                     GEvent.ENGINE, subtype=GEvent.END, source=None
        #                 )
        #                 pygame.event.post(end_event)
        #                 self.running = False
        #             else:
        #                 create_shape = pygame.event.Event(
        #                     GEvent.ENGINE, subtype=GEvent.CREATE, source=None
        #                 )
        #                 pygame.event.post(create_shape)

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
