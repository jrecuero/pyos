from pyplay import Scene
from pyplay.gobject.grid import GridEvent


class GameScene(Scene):
    """GameScene implements all functionality for the scene that contains
    the board.
    """

    def __init__(self, surface, **kwargs):
        super(GameScene, self).__init__("game scene", surface, **kwargs)
        self.next_piece = None

    def handle_custom_event(self, event):
        """handle_custom_event should process pygame custom event given.
        Any object in the game, like, scene, graphic objects, ... can post
        customs events, and those should be handled at this time.
        """
        super(GameScene, self).handle_custom_event(event)
        if event.type == GridEvent.NEXT:
            if self.next_piece:
                self.del_gobject(self.next_piece)
            self.next_piece = event.source
            self.next_piece.x = 550
            self.next_piece.y = 50
            self.add_gobject(self.next_piece)
