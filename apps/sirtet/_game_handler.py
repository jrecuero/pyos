from pyplay import GHandler, Color
from pyplay.gobject.xgrid import GridEvent


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

    def handle_completed_lines(self, lines):
        """handle_completed_lines handles lines that have been completed in the
        play cells area.
        """
        for _, line in lines:
            for cell in line:
                self.color_cells[Color.color_to_str(cell.color)] += 1
            print(f"{[Color.color_to_str(x.color) for x in line]}")
            print(f"{self.color_cells}")
        self.total_lines += len(lines)
        self.console.message = f"Lines Completed: {self.total_lines}"

    def handle_custom_event(self, event):
        """handle_custom_event should process pygame custom event given.
        Any object in the game, like, scene, graphic objects, ... can post
        customs events, and those should be handled at this time.
        """
        if event.type == GridEvent.COMPLETED:
            self.handle_completed_lines(event.source)
        elif event.type == GridEvent.END:
            self.console.message = f"GAME OVER"
            self.running = False
        super(GameHandler, self).handle_custom_event(event)
