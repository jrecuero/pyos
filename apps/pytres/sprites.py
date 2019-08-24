import sys
import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        # self.image.convert_alpha()
        # self.image.fill(pygame.Color(255, 0, 0))
        # self.image.set_alpha(0)
        # pygame.draw.rect(self.image, pygame.Color(0, 255, 0), (5, 5, 40, 40))
        pygame.draw.polygon(
            self.image, pygame.Color(255, 0, 0), [(0, 0), (25, 25), (50, 0), (25, 50)]
        )
        self.image = pygame.transform.flip(self.image, False, True)
        self.rect = self.image.get_rect()
        self.rect.center = (100, 100)
        self.counter = 0
        self.flag = True

    def reset_image(self):
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)

    def update(self):
        self.counter += 1
        if self.counter == 30:
            self.counter = 0
            self.flag = not self.flag
            self.reset_image()
            if self.flag:
                pygame.draw.polygon(
                    self.image,
                    pygame.Color(255, 0, 0),
                    [(0, 0), (25, 25), (50, 0), (25, 50)],
                )
                self.image = pygame.transform.flip(self.image, False, True)
            else:
                pygame.draw.rect(self.image, pygame.Color(0, 255, 0), (5, 5, 40, 40))


def main():
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption("PY-PLUS")
    surface = pygame.display.set_mode((600, 400))
    clock = pygame.time.Clock()
    player = Player()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    while True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

        # -> update objects
        all_sprites.update()
        # <-

        # -> render objects
        surface.fill(pygame.Color(0, 0, 255))
        all_sprites.draw(surface)
        pygame.display.flip()
        # <-


if __name__ == "__main__":
    main()
