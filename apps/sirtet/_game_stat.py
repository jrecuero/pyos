from pyplay import Color
from pyplay.gobject import GText


class GameStat:
    """GameStat implements all stats values handled by the game.
    """

    def __init__(self):
        self.total_lines = 0
        self.colors = [Color.BLACK, Color.BLUE, Color.RED, Color.GREEN]
        # self.color_cells = {Color.color_to_str(color): 0 for color in self.colors}
        self.color_cells = self.get_color_dict()
        self.gtext_colors = {}
        row = 300
        for color in self.colors:
            color_str = Color.color_to_str(color)
            self.gtext_colors[color_str] = GText(
                color_str,
                550,
                row,
                f"0     ",
                font_bold=True,
                color=Color.WHITE,
                bcolor=color,
            )
            row += 20
        self.gtext_total_lines = GText(
            "total lines", 550, 250, f"Lines Completed : 0 {' ' * 50}"
        )

    def get_color_dict(self):
        return {Color.color_to_str(color): 0 for color in self.colors}

    def add_to_color(self, color, value=1):
        """add_color adds the given value to the given color.
        """
        text_color = Color.color_to_str(color)
        self.color_cells[text_color] += value
        self.gtext_colors[text_color].message = f"{self.color_cells[text_color]}"

    def add_color_dict(self, color_dict):
        """add_color_dict adds values for every color given in the dictionary.
        """
        for color, value in color_dict.items():
            self.color_cells[color] += value
            self.gtext_colors[color].message = f"{self.color_cells[color]}"

    def add_to_lines(self, lines):
        """add_to_lines adds the given lines to the total.
        """
        self.total_lines += lines
        self.gtext_total_lines.message = f"Lines Completed: {self.total_lines}"
