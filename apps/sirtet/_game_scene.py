from pyplay import Scene, GEvent


class GameScene(Scene):
    """GameScene implements all functionality for the scene that contains
    the board.
    """

    def __init__(self, surface, **kwargs):
        super(GameScene, self).__init__("game scene", surface, **kwargs)
        self.gobj_next_piece = None
        self.gtext_actor = None
        self.gtext_target = None

    def handle_custom_event(self, event):
        """handle_custom_event should process pygame custom event given.
        Any object in the game, like, scene, graphic objects, ... can post
        customs events, and those should be handled at this time.
        """
        super(GameScene, self).handle_custom_event(event)
        if event.type == GEvent.ENGINE:
            if event.subtype == GEvent.NEXT:
                if self.gobj_next_piece:
                    self.del_gobject(self.gobj_next_piece)
                self.gobj_next_piece = event.source
                self.gobj_next_piece.x = 550
                self.gobj_next_piece.y = 50
                self.add_gobject(self.gobj_next_piece)
            elif event.subtype == GEvent.CREATE:
                if getattr(event, "dest", None) == GEvent.SCENE:
                    self.del_gobject(self.gobj_target)
                    self.gobj_target = event.source
                    self.gobj_target.x = 550
                    self.gobj_target.y = 550
                    self.add_gobject(self.gobj_target)

    def render(self, **kwargs):
        """render calls render method for all scene graphical objects.
        """
        super(GameScene, self).render(**kwargs)
