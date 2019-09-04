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
            GEvent.engine_event(GEvent.COMPLETED, source=completed_lines)
        return completed_lines

    def blow_color(self, color):
        """blow_color removes all cells with the given color.
        """
        blows = [0 for _ in range(len(self.play_cells[0]))]
        for index, row in enumerate(self.play_cells[::-1]):
            rindex = len(self.play_cells) - index - 1
            for cindex, cell in enumerate(row):
                if cell and cell.color == color:
                    self.play_cells[rindex][cindex] = None
                    blows[cindex] += 1
                elif blows[cindex]:
                    self.play_cells[rindex][cindex] = None
                    if cell:
                        cell.move_it(0, blows[cindex])
                    self.play_cells[rindex + blows[cindex]][cindex] = cell
        return sum(blows)

    def blow_empty(self):
        """blow_empty removes all empty cells.
        """
        blows = [0 for _ in range(len(self.play_cells[0]))]
        for index, row in enumerate(self.play_cells[::-1]):
            rindex = len(self.play_cells) - index - 1
            for cindex, cell in enumerate(row):
                if not cell:
                    blows[cindex] += 1
                elif cell and blows[cindex]:
                    self.play_cells[rindex][cindex] = None
                    cell.move_it(0, blows[cindex])
                    self.play_cells[rindex + blows[cindex]][cindex] = cell
        return sum(blows)

    def copy_color(self, from_color, to_color):
        """copy_color copies the first color for all cells in the second
        color.
        """
        result = 0
        for cell in [
            c for row in self.play_cells for c in row if c and c.color == from_color
        ]:
            result += 1
            cell.color = to_color
        return result

    def color_to_empty(self, color):
        """color_to_move changes all cells with the given color to empty cells.
        """
        result = 0
        for rindex, row in enumerate(self.play_cells):
            for cindex, cell in enumerate(row):
                if cell and cell.color == color:
                    result += 1
                    self.play_cells[rindex][cindex] = None
        return result

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
            GEvent.engine_event(GEvent.END, winner="target")
        else:
            GEvent.board_event(GEvent.CREATE, source=None)

    def update(self, surface, **kwargs):
        """update provides any functionality to be done every tick.
        """
        for shape in self.gobjects:
            log.Update(shape.move_actions).call()
            for ma in shape.move_actions:
                ma["call"](*ma["args"])
                shape_collision_box = shape.get_collision_box()
                if shape_collision_box.check_out_of_width_bounds(0, self.dx_play_cells):
                    shape.back_it()

                shape_collision_box = shape.get_collision_box()
                if shape_collision_box.check_out_of_heigh_bounds(0, self.dy_play_cells):
                    shape.back_it()
                    if shape.gravity_step:
                        self.add_shape_to_play_cells(shape)
                        self.handle_add_shape_to_play_cells()
                        break

                shape_collision_box = shape.get_collision_box()
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
                        break

        for shape in self.gobjects:
            shape.update(surface, **kwargs)

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
