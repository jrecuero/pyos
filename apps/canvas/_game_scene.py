from pyengine import Scene, GCanvas, GLoader
from _game_player import GamePlayer


class GameScene(Scene):

    def __init__(self, surface, **kwargs):
        super(GameScene, self).__init__("Canvas", surface, **kwargs)
        canvas = GCanvas("My Canvas", 2, 2, surface.get_width() - 4, surface.get_height() - 4, 2)
        self.gloader = GLoader("canvas loader")
        plane_img = self.gloader.load_image("apps/canvas/images", "plane.png")
        gplane = GamePlayer(plane_img, 32, 32)
        canvas.add_gobject(gplane, 1)
        self.add_gobject(canvas)
