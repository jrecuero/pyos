import os
import pygame

_image_db = {}
_sound_db = {}


def load_image(path, filename):
    """load_image loads an image. If the image has already been loaded, it
    returns the cached version instead of loading it again.
    """
    f_name = os.path.join(path, filename)
    if f_name not in _image_db:
        _image_db[f_name] = pygame.image.load(f_name)
    return _image_db[f_name]


def load_sound(path, filename):
    """load_sound loads a sound. If the sound has already been loaded, it
    returns the cached version instead of loading it again.
    """
    f_name = os.path.join(path, filename)
    if f_name not in _sound_db:
        _sound_db[f_name] = pygame.mixer.Sound(f_name)
    return _sound_db[f_name]


def load_music(path, filename):
    """load_music loads a music file.
    """
    pygame.mixer.music.load(os.path.join(path, filename))
