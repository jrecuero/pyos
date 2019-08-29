import pygame
from ..._gevent import GEvent
from ..._loggar import log
from ._grid_board import GridBoard


class GravityBoard(GridBoard):
    """GravityBoard implements a board with a timer that simulates downward
    gravity.
    """

    def __init__(self, name, x, y, dx, dy, xsize, ysize=None, **kwargs):
        super(GravityBoard, self).__init__(name, x, y, dx, dy, xsize, ysize, **kwargs)
        pygame.time.set_timer(GEvent.GRAVITY, 1000)

    def update(self, surface, **kwargs):
        """update provides any functionality to be done every tick.
        """
        for shape in self.gobjects:
            shape.update(surface, **kwargs)

        for shape in self.gobjects:
            collision_box = shape.get_collision_box()
            if collision_box.check_out_of_bounds(
                0, 0, self.dx_play_cells, self.dy_play_cells
            ):
                shape.back_it()
                if shape.gravity_step:
                    for cell in shape.cells:
                        x, y = cell.gridx, cell.gridy
                        log.GravityBoard().PlayCellsAt(f"{x}, {y}").call()
                        self.play_cells[y][x] = cell
                        # log.GravityBoard().Gravity(self.play_cells).call()
                    # self.del_gobject(shape)
                    del_shape = pygame.event.Event(GEvent.DELETE, source=shape)
                    pygame.event.post(del_shape)
