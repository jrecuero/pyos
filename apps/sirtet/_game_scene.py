from pyplay import Scene, GEvent


class GameScene(Scene):
    """GameScene implements all functionality for the scene that contains
    the board.
    """

    def __init__(self, surface, **kwargs):
        super(GameScene, self).__init__("game scene", surface, **kwargs)
        self.next_piece = None
        self.gtext_actor = None
        self.gtext_target = None

    def handle_custom_event(self, event):
        """handle_custom_event should process pygame custom event given.
        Any object in the game, like, scene, graphic objects, ... can post
        customs events, and those should be handled at this time.
        """
        super(GameScene, self).handle_custom_event(event)
        if event.type == GEvent.ENGINE and event.subtype == GEvent.NEXT:
            if self.next_piece:
                self.del_gobject(self.next_piece)
            self.next_piece = event.source
            self.next_piece.x = 550
            self.next_piece.y = 50
            self.add_gobject(self.next_piece)
        elif event.type == GEvent.ENGINE and event.subtype == GEvent.DISPLAY:
            if event.actor == "actor":
                if self.gtext_actor:
                    self.del_gobject(self.gtext_actor)
                self.gtext_actor = event.source.gdisplay()
                self.gtext_actor.x = 550
                self.gtext_actor.y = 500
                self.add_gobject(self.gtext_actor)
            elif event.actor == "target":
                if event.source is None:
                    if self.gtext_target:
                        self.del_gobject(self.gtext_target)
                else:
                    if self.gtext_target:
                        self.del_gobject(self.gtext_target)
                    self.gtext_target = event.source.gdisplay()
                    self.gtext_target.x = 550
                    self.gtext_target.y = 550
                    self.add_gobject(self.gtext_target)

    def render(self, **kwargs):
        """render calls render method for all scene graphical objects.
        """
        super(GameScene, self).render(**kwargs)
