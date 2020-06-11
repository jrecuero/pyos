import sys
import os
import pygame
from pyengine import Scene, GSpriteSheet, GAniImage
import pytmx
from pyengine import Log


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
        for to in self.tmxdata.objects:
            Log.TmxObject(to.name).Position(f"{x}, {y}").Image(to.image).call()
            for k, v in to.properties.items():
                Log.TmxObjectx(to.name).Properties(f"{k}: {v}").call()
            if to.image:
                surface.blit(to.image, (to.x, to.y))

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
        # self.player_image = pygame.image.load(os.path.join(map_folder, "soldier.png"))
        self.player_sprite_sheet = GSpriteSheet(os.path.join(map_folder, "full_soldier.png"), 32)
        # self.player = GImage("player", os.path.join(map_folder, "soldier.png"), 64, 32)
        # self.player = GImage("player", self.player_sprite_sheet .image_at(pygame.Rect(5 * 32, 0, 32, 32), -1), 32, 32)
        self.player = GAniImage("player", self.player_sprite_sheet, 0, 0, 32, 32, 0, 3)
        self.add_gobject(self.player)

    def handle_keyboard_event(self, event, **kwargs):
        """handle_keyboard_event should process the keyboard event given.
        """
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_x]:
            sys.exit(0)
        if key_pressed[pygame.K_DOWN]:
            self.player.y += 32
            self.player.set_new_frames(0, 3)
        if key_pressed[pygame.K_UP]:
            self.player.y -= 32
            self.player.set_new_frames(4, 7)
        if key_pressed[pygame.K_RIGHT]:
            self.player.x += 32
            self.player.set_new_frames(8, 11)
        if key_pressed[pygame.K_LEFT]:
            self.player.x -= 32
            self.player.set_new_frames(12, 15)

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
        # self.surface.blit(self.player_image, (32, 32))
