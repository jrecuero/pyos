from pyplay import Color
from pyplay.gobject import GText


class GameStat:
    """GameStat implements all stats values handled by the game.
    """

    def __init__(self):
        self.total_lines = 0
        self.color_cells = {
            Color.color_to_str(Color.BLACK): 0,
            Color.color_to_str(Color.BLUE): 0,
            Color.color_to_str(Color.RED): 0,
            Color.color_to_str(Color.GREEN): 0,
        }
        self.gtext_total_lines = GText(
            "total lines", 550, 50, f"Lines Completed : 0 {' ' * 50}"
        )
        self.gtext_colors = {
            Color.color_to_str(Color.BLACK): GText(
                "black", 550, 70, f"black : 0 {' ' * 50}"
            ),
            Color.color_to_str(Color.BLUE): GText(
                "blue", 550, 90, f"blue : 0 {' ' * 50}"
            ),
            Color.color_to_str(Color.RED): GText(
                "red", 550, 110, f"red : 0 {' ' * 50}"
            ),
            Color.color_to_str(Color.GREEN): GText(
                "green", 550, 130, f"green : 0 {' ' * 50}"
            ),
        }

    def add_to_color(self, color, value=1):
        """add_color adds the given value to the given color.
        """
        text_color = Color.color_to_str(color)
        self.color_cells[text_color] += value
        self.gtext_colors[
            text_color
        ].message = f"{text_color} : {self.color_cells[text_color]}"

    def add_to_lines(self, lines):
        """add_to_lines adds the given lines to the total.
        """
        self.total_lines += lines
        self.gtext_total_lines.message = f"Lines Completed: {self.total_lines}"
