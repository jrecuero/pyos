import pygame
from pyengine import GObject, GImage


class GameBullet(GObject):
    """GameBullet class implements all bullet instances.
    """

    def __init__(self, x, y, radius, **kwargs):
        """__init__ initializes GameBullet instance.

        Args:
            x (int): GameBullet instance X-axis center position.
            y (int): GameBullet instance Y-axis center position
            radius (int): GameBullet instance radius.
            **kwargs (dict): GamePlayer dictionary with custom arguments.
        """
        super(GameBullet, self).__init__("Game Bullet", x - radius, y - radius, radius * 2, radius * 2, **kwargs)
        self.center = pygame.Vector2(x, y)
        self.radius = radius
        # pygame.draw.rect(self.image, Color.RED, self.image.get_rect(), self.outline)
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.speed = 10
        self.vx = 0
        self.vy = -self.speed

    def update(self, surface, **kwargs):
        """update method update the GameBullet instance.

        Args:
            surface (Surface): Surface where instance will be displayed
            **kwargs (dict): custom instance arguments.

        Returns:
            None: no return
        """
        self.x += self.vx
        self.y += self.vy
        result, collision = self.parent.can_move_to(self)
        if collision:
            self.parent.del_gobject(collision)
        if not result:
            self.parent.del_gobject(self)


class GameEnemy(GImage):
    """GameEnemy class implements the game enemy image for the game.
    """

    def __init__(self, image, x, y, **kwargs):
        """__init__ initializes GameEnemy instance.

        Args:
            image (Image): GameEnemy instance image to be used.
            x (int): GameEnemy instance initial X-axis position.
            y (int): GameEnemy instance initial Y-axis position.
            **kwargs (dict): GameEnemy dictionary with custom arguments.
        """
        super(GameEnemy, self).__init__("Canvas enemy", image, x, y, **kwargs)
        self.speed = 2
        self.vx = self.speed
        self.vy = 0

    def update(self, surface, **kwargs):
        """update method update the GameEnemy instance.

        Args:
            surface (Surface): Surface where instance will be displayed
            **kwargs (dict): custom instance arguments.

        Returns:
            None: no return
        """
        self.x += self.vx
        self.y += self.vy
        result, collision = self.parent.can_move_to(self)
        if collision:
            self.parent.del_gobject(collision)
        if not result:
            self.x -= self.vx
            self.y -= self.vy
            self.vx = -self.vx
            self.vy = -self.vy
