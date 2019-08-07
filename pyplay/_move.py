import random


class Move:

    NONE = 0
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4

    _reversed = {NONE: NONE, UP: DOWN, RIGHT: LEFT, DOWN: UP, LEFT: RIGHT}
    _to_str = {NONE: "none", UP: "up", RIGHT: "right", DOWN: "down", LEFT: "left"}

    @staticmethod
    def allowed(move, to_move):
        if (move in [Move.UP, Move.DOWN]) and (to_move in [Move.UP, Move.DOWN]):
            return False
        elif (move in [Move.LEFT, Move.RIGHT]) and (to_move in [Move.LEFT, Move.RIGHT]):
            return False
        return True

    @staticmethod
    def left_or_right():
        return random.choice([Move.RIGHT, Move.LEFT])

    @staticmethod
    def up_or_down():
        return random.choice([Move.DOWN, Move.UP])

    @staticmethod
    def any():
        return random.choice([Move.DOWN, Move.UP, Move.LEFT, Move.RIGHT])

    @staticmethod
    def reverse(self, move):
        return Move._reversed[move]

    @staticmethod
    def to_str(self, move):
        return Move._to_str[move]
