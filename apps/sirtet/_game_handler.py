from pyplay import GHandler, Color
from pyplay.gobject import GText
from pyplay.gobject.grid import GridEvent
from _game_stat import GameStat


class GameHandler(GHandler):
    """GameHandler implements all custom functionality for the actual game.
    """

    def __init__(self, name, surface, **kwargs):
        super(GameHandler, self).__init__(name, surface, **kwargs)
        self.gstat = GameStat()
        self.console = GText("console", 10, 800, f"> {' ' * 50}")

    def handle_completed_lines(self, lines):
        """handle_completed_lines handles lines that have been completed in the
        play cells area.
        """
        for _, line in lines:
            for cell in line:
                self.gstat.add_to_color(cell.color)
        self.gstat.add_to_lines(len(lines))

    def handle_custom_event(self, event):
        """handle_custom_event should process pygame custom event given.
        Any object in the game, like, scene, graphic objects, ... can post
        customs events, and those should be handled at this time.
        """
        if event.type == GridEvent.COMPLETED:
            self.handle_completed_lines(event.source)
        elif event.type == GridEvent.END:
            self.console.message = f"> GAME OVER"
            self.running = False
        elif event.type == GridEvent.PAUSE:
            if event.source:
                self.console.message = f"> PAUSED"
                self.running = False
            else:
                self.console.message = f">"
                self.running = True
        super(GameHandler, self).handle_custom_event(event)
