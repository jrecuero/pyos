import random
import pygame

# from ._loggar import log


# class XMove:

#     NONE = 0
#     UP = 1
#     RIGHT = 2
#     DOWN = 3
#     LEFT = 4

#     _reversed = {NONE: NONE, UP: DOWN, RIGHT: LEFT, DOWN: UP, LEFT: RIGHT}
#     _to_str = {NONE: "none", UP: "up", RIGHT: "right", DOWN: "down", LEFT: "left"}

#     @staticmethod
#     def allowed(move, to_move):
#         if (move in [Move.UP, Move.DOWN]) and (to_move in [Move.UP, Move.DOWN]):
#             return False
#         elif (move in [Move.LEFT, Move.RIGHT]) and (to_move in [Move.LEFT, Move.RIGHT]):
#             return False
#         return True

#     @staticmethod
#     def left_or_right():
#         return random.choice([Move.RIGHT, Move.LEFT])

#     @staticmethod
#     def up_or_down():
#         return random.choice([Move.DOWN, Move.UP])

#     @staticmethod
#     def any():
#         return random.choice([Move.DOWN, Move.UP, Move.LEFT, Move.RIGHT])

#     @staticmethod
#     def reverse(self, move):
#         return Move._reversed[move]

#     @staticmethod
#     def to_str(self, move):
#         return Move._to_str[move]


class Move:
    """Move defines movement for any graphical object in the application.
    """

    def __init__(self, x=None, y=None, speed=None):
        x = x if x is not None else 0
        y = y if y is not None else 0
        self.vector = pygame.math.Vector2(x, y)
        self.speed = speed
        self._shadow_vector = None

    def __str__(self):
        return f"({self.vector.x}, {self.vector.y}) @ {self.speed}"

    @property
    def x(self):
        return self.vector.x

    @property
    def y(self):
        return self.vector.y

    @property
    def speed(self):
        return self.__speed

    @speed.setter
    def speed(self, speed):
        """speed sets a new speed value for the move instance. Vector will
        be updated to fit the new speed value.
        """
        if (self.vector.x == 0) and (self.vector.y == 0):
            self.__speed = 0
        elif speed:
            self.vector.scale_to_length(speed)
            self.__speed = speed
        elif speed is None:
            self.__speed = self.vector.length()
        else:
            self.__speed = 0
            self.vector.x = 0
            self.vector.y = 0

    def is_up(self):
        """is_up checks if movement has an UP component.
        """
        return self.vector.y < 0

    def is_down(self):
        """is_down checks if movement has an DOWN component.
        """
        return self.vector.y > 0

    def is_right(self):
        """is_right checks if movement has an RIGHT component.
        """
        return self.vector.x > 0

    def is_left(self):
        """is_left checks if movement has an LEFT component.
        """
        return self.vector.x < 0

    def reverse(self):
        """reverse changes the vector to the oposite direction and sense.
        """
        # vector = self.vector.reflect(self.vector)
        # self.vector.x = round(vector.x)
        # self.vector.y = round(vector.y)
        self.vector.x = self.vector.x * (-1)
        self.vector.y = self.vector.y * (-1)
        return self.vector

    def bounce_x(self):
        """bounce_x bounces against an X-plane, it means y-component will
        be reversed.
        """
        self.vector.x = self.vector.x * (-1)
        return self.vector

    def bounce_y(self):
        """bounce_y bounces against an Y-plane, it means x-component will
        be reversed.
        """
        self.vector.y = self.vector.y * (-1)
        return self.vector

    def any(self, speed=None):
        """any changes the direction to any other one.
        """
        self.vector = pygame.math.Vector2(random.randint(-5, 5), random.randint(-5, 5))
        self.speed = speed
        return self.vector

    def pause(self):
        """pause stops any movement. Vector value is stored in a shadow
        variable in order to be able to retrieve it later on.
        """
        self._shadow_vector = self.vector
        self.vector = pygame.math.Vector2(0, 0)

    def resume(self):
        """resume sets vector to the shadow vector value that was setup
        previously by a pause call.
        """
        if self._shadow_vector:
            self.vector = self._shadow_vector
            self._shadow_vector = None
