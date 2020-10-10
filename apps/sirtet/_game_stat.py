from pyplay import Color, GObject
from pyplay.gobject import GText


class GameStat(GObject):
    """GameStat implements all stats values handled by the game.
    """

    COLORS = [Color.BLACK, Color.BLUE, Color.RED, Color.GREEN]

    @staticmethod
    def new_play_colors():
        """new_play_colors generates a new dictionary that containes cells
        being matched in a completed line.
        """
        return {Color.color_to_str(color): 0 for color in GameStat.COLORS}

    def __init__(self, **kwargs):
        super(GameStat, self).__init__("stats", 0, 0, 200, 200, **kwargs)
        self.total_lines = 0
        self.color_cells = GameStat.new_play_colors()
        self.gtext_colors = {}
        self.gtext_total_lines = GText(
            "total lines", 0, 0, f"Lines Completed : 0 {' ' * 50}"
        )
        self.image.blit(self.gtext_total_lines.image, (0, 0, 100, 50))
        row = 30
        for color in GameStat.COLORS:
            color_str = Color.color_to_str(color)
            self.gtext_colors[color_str] = GText(
                color_str,
                0,
                0,
                f"0     ",
                font_bold=True,
                color=Color.WHITE,
                bcolor=color,
            )
            self.image.blit(self.gtext_colors[color_str].image, (0, row, 100, 20))
            row += 20

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

    def update(self, surface, **kwargs):
        """update calls update method for all scenes and  graphical objects.
        """
        self.image.blit(self.gtext_total_lines.image, (0, 0, 100, 50))
        row = 30
        for color in GameStat.COLORS:
            color_str = Color.color_to_str(color)
            self.image.blit(self.gtext_colors[color_str].image, (0, row, 100, 20))
            row += 20
