from pyplay import Color
from _game_stat import GameStat


class GameActorStats:
    """GameActorStats implements stats used inside any game actor.
    """

    def __init__(self):
        self.total_lines = 0
        self.play_colors = GameStat.new_play_colors()

    def add_color_dict(self, color_dict):
        """add_color_dict adds the given colors dictionary to the total dictionary
        with all colors played.
        """
        for k, v in color_dict.items():
            self.play_colors[k] += v
