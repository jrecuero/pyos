import sys
import os
import pygame
from pyengine import Scene
import pytmx
# from pyengine import Log


class TileMap:

    def __init__(self, filename):
        self.tmxdata = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = self.tmxdata.width * self.tmxdata.tilewidth
        self.height = self.tmxdata.height * self.tmxdata.tileheight

    def render(self, surface):
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmxdata.get_tile_image_by_gid(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight))

    def make_map(self):
        temp_surface = pygame.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface


class GameScene(Scene):

    def __init__(self, surface, **kwargs):
        super(GameScene, self).__init__("Game Tiled Scene", surface, **kwargs)
        game_folder = os.path.dirname(__file__)
        map_folder = os.path.join(game_folder, "tilemap")
        self.map = TileMap(os.path.join(map_folder, "base.tmx"))
        self.map_img = self.map.make_map()
        self.map_img_rect = self.map_img.get_rect()

    def handle_keyboard_event(self, event, **kwargs):
        """handle_keyboard_event should process the keyboard event given.
        """
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_x]:
            sys.exit(0)

        super(GameScene, self).handle_keyboard_event(event, **kwargs)

    def update(self, **kwargs):
        """update calls update method for all scene graphical objects.
        """
        super(GameScene, self).update(**kwargs)

    def render(self, **kwargs):
        """render calls render method for all scene graphical objects.
        """
        self.surface.blit(self.map_img, (0, 0))
        super(GameScene, self).render(**kwargs)
