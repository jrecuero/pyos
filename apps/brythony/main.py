from browser import document
from engine import Handler, set_plugin, Scene
from engine.dplugs import BrythonPlugin
from engine.nobject import String


class BrythonScene(Scene):
    def __init__(self):
        super(BrythonScene, self).__init__("Brython Scene")

    def setup(self, screen):
        self.add_object(String(10, 10, "hello world"))


canvas = document["the_canvas"]
set_plugin(BrythonPlugin(canvas=canvas))
h = Handler()
h.add_scene(BrythonScene)
h.run()
