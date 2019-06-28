from typing import List, Any
import curses
from .._nobject import NObject, update, render
from .._event import Event, Timer, EVT
from ._string import String


class HPath(NObject):
    """HPath class identifies a horizontal path to draw in the screen.
    """

    def __init__(self, y: int, x: int, path: List[int], fmt=curses.A_NORMAL):
        super(HPath, self).__init__(y, x, -1, -1, fmt)
        self.path: List[int] = path

    @render
    def render(self, screen) -> List[Event]:
        y = self.y
        x = self.x
        for index, weight in enumerate(self.path):
            prev_w = self.path[index - 1] if index > 0 else 0
            next_w = self.path[index + 1] if index < (len(self.path) - 1) else 0
            if prev_w == weight == next_w:
                screen.addstr(y, x, chr(9473), self.fmt)
            elif weight > prev_w and weight > next_w:
                screen.addstr(y, x, chr(9499), self.fmt)
                delta_p = weight - prev_w
                for dy in range(delta_p):
                    screen.addstr(y - dy - 1, x, chr(9475), self.fmt)
                y = y - delta_p
                delta_n = weight - next_w
                for dy in range(delta_n):
                    screen.addstr(y + dy, x, chr(9475), self.fmt)
                screen.addstr(y + delta_n, x, chr(9495), self.fmt)
                y = y + delta_n
            elif weight > prev_w:
                delta_p = weight - prev_w
                screen.addstr(y, x, chr(9499), self.fmt)
                for dy in range(delta_p - 1):
                    screen.addstr(y - dy - 1, x, chr(9475), self.fmt)
                screen.addstr(y - delta_p, x, chr(9487), self.fmt)
                y = y - delta_p
            elif weight > next_w:
                delta_n = weight - next_w
                screen.addstr(y, x, chr(9491), self.fmt)
                for dy in range(delta_n - 1):
                    screen.addstr(y + dy + 1, x, chr(9475), self.fmt)
                screen.addstr(y + delta_n, x, chr(9495), self.fmt)
                y = y + delta_n
            elif weight < next_w and weight == prev_w:
                screen.addstr(y, x, chr(9473), self.fmt)
            elif weight < prev_w and weight == next_w:
                screen.addstr(y, x, chr(9473), self.fmt)
            elif weight < prev_w and weight < next_w:
                screen.addstr(y, x, chr(9473), self.fmt)
            x = x + 1

        return []


class HPathCover(NObject):
    """HPathCover class identifies a horizontal path to draw in the screen.
    """

    def __init__(self, y: int, x: int, path: List[int], fmt=curses.A_NORMAL):
        super(HPathCover, self).__init__(y, x, -1, -1, fmt)
        self.path: List[int] = path

    @render
    def render(self, screen) -> List[Event]:
        y = self.y
        x = self.x
        for index, weight in enumerate(self.path):
            prev_w = self.path[index - 1] if index > 0 else 0
            next_w = self.path[index + 1] if index < (len(self.path) - 1) else 0
            if prev_w == weight == next_w:
                screen.addstr(y, x, chr(9473), self.fmt)
            elif weight < prev_w and weight < next_w:
                delta_p = prev_w - weight
                screen.addstr(y, x, chr(9491), self.fmt)
                for dy in range(delta_p):
                    screen.addstr(y + dy + 1, x, chr(9475), self.fmt)
                y = y + delta_p
                delta_n = next_w - weight
                for dy in range(delta_n):
                    screen.addstr(y - dy, x, chr(9475), self.fmt)
                screen.addstr(y - delta_n, x, chr(9487), self.fmt)
                y = y - delta_n
            elif weight < prev_w:
                delta_p = prev_w - weight
                screen.addstr(y, x, chr(9491), self.fmt)
                for dy in range(delta_p - 1):
                    screen.addstr(y + dy + 1, x, chr(9475), self.fmt)
                screen.addstr(y + delta_p, x, chr(9495), self.fmt)
                y = y + delta_p
            elif weight < next_w:
                delta_n = next_w - weight
                screen.addstr(y, x, chr(9499), self.fmt)
                for dy in range(delta_n - 1):
                    screen.addstr(y - dy - 1, x, chr(9475), self.fmt)
                screen.addstr(y - delta_n, x, chr(9487), self.fmt)
                y = y - delta_n
            elif weight == prev_w:
                screen.addstr(y, x, chr(9473), self.fmt)
            elif weight == next_w:
                screen.addstr(y, x, chr(9473), self.fmt)
            elif weight > prev_w and weight > next_w:
                screen.addstr(y, x, chr(9473), self.fmt)
            x = x + 1

        return []


class HorizontalPath(NObject):
    def __init__(self, y: int, x: int, dy: int, path: List[int], fmt=curses.A_NORMAL):
        super(HorizontalPath, self).__init__(y, x, dy, -1, fmt)
        self.lower_path = HPath(y, x, path, fmt)
        self.upper_path = HPathCover(y - dy, x, path, fmt)

    @render
    def render(self, screen) -> List[Event]:
        self.lower_path.render(screen)
        self.upper_path.render(screen)
        return []


class VPath(NObject):
    """VPath class identifies a vertical path to draw in the screen.
    """

    def __init__(self, y: int, x: int, path: List[int], fmt=curses.A_NORMAL):
        super(VPath, self).__init__(y, x, -1, -1, fmt)
        self.path: List[int] = path

    @render
    def render(self, screen) -> List[Event]:
        y = self.y
        x = self.x
        for index, weight in enumerate(self.path):
            prev_w = self.path[index - 1] if index > 0 else 0
            next_w = self.path[index + 1] if index < (len(self.path) - 1) else 0
            if prev_w == weight == next_w:
                screen.addstr(y, x, chr(9475), self.fmt)
            elif weight < prev_w and weight < next_w:
                screen.addstr(y, x, chr(9475), self.fmt)
            elif weight > prev_w and weight > next_w:
                delta_p = weight - prev_w
                screen.addstr(y, x, chr(9499), self.fmt)
                for dx in range(delta_p):
                    screen.addstr(y, x + dx + 1, chr(9473), self.fmt)
                x = x + delta_p
                delta_n = weight - next_w
                for dx in range(delta_n - 1):
                    screen.addstr(y, x - dx - 1, chr(9473), self.fmt)
                screen.addstr(y, x - delta_n, chr(9487), self.fmt)
                x = x - delta_n
            elif weight <= prev_w and weight > next_w:
                delta_n = weight - next_w
                screen.addstr(y, x, chr(9499), self.fmt)
                for dx in range(delta_n - 1):
                    screen.addstr(y, x - dx - 1, chr(9473), self.fmt)
                screen.addstr(y, x - delta_n, chr(9487), self.fmt)
                x = x - delta_n
            elif weight == prev_w:
                screen.addstr(y, x, chr(9475), self.fmt)
            elif weight > prev_w:
                delta_p = weight - prev_w
                screen.addstr(y, x, chr(9495), self.fmt)
                for dx in range(delta_p - 1):
                    screen.addstr(y, x + dx + 1, chr(9473), self.fmt)
                screen.addstr(y, x + delta_p, chr(9491), self.fmt)
                x = x + delta_p
            elif next_w == weight:
                screen.addstr(y, x, chr(9475), self.fmt)
            y = y + 1

        return []


class VPathCover(NObject):
    """VPathCover class identifies a vertical path to draw in the screen.
    """

    def __init__(self, y: int, x: int, path: List[int], fmt=curses.A_NORMAL):
        super(VPathCover, self).__init__(y, x, -1, -1, fmt)
        self.path: List[int] = path

    @render
    def render(self, screen) -> List[Event]:
        y = self.y
        x = self.x
        for index, weight in enumerate(self.path):
            prev_w = self.path[index - 1] if index > 0 else 0
            next_w = self.path[index + 1] if index < (len(self.path) - 1) else 0
            if prev_w == weight == next_w:
                screen.addstr(y, x, chr(9475), self.fmt)
            elif weight >= prev_w and weight < next_w:
                delta_n = next_w - weight
                screen.addstr(y, x, chr(9495), self.fmt)
                for dx in range(delta_n - 1):
                    screen.addstr(y, x + dx + 1, chr(9473), self.fmt)
                screen.addstr(y, x + delta_n, chr(9491), self.fmt)
                x = x + delta_n
            elif weight >= prev_w and weight >= next_w:
                screen.addstr(y, x, chr(9475), self.fmt)
            elif weight < prev_w and weight < next_w:
                delta_p = prev_w - weight
                screen.addstr(y, x, chr(9499), self.fmt)
                for dx in range(delta_p):
                    screen.addstr(y, x - dx - 1, chr(9473), self.fmt)
                screen.addstr(y, x - delta_p, chr(9487), self.fmt)
                x = x - delta_p
                delta_n = next_w - weight
                for dx in range(delta_n):
                    screen.addstr(y, x + dx, chr(9473), self.fmt)
                screen.addstr(y, x + delta_n, chr(9491), self.fmt)
                x = x + delta_n
            elif weight < prev_w:
                delta_p = prev_w - weight
                screen.addstr(y, x, chr(9499), self.fmt)
                for dx in range(delta_p):
                    screen.addstr(y, x - dx - 1, chr(9473), self.fmt)
                screen.addstr(y, x - delta_p, chr(9487), self.fmt)
                x = x - delta_p
            y = y + 1

        return []


class VerticalPath(NObject):
    def __init__(self, y: int, x: int, dx: int, path: List[int], fmt=curses.A_NORMAL):
        super(VerticalPath, self).__init__(y, x, -1, dx, fmt)
        self.lower_path = VPath(y, x, path, fmt)
        self.upper_path = VPathCover(y, x + dx, path, fmt)

    @render
    def render(self, screen) -> List[Event]:
        self.lower_path.render(screen)
        self.upper_path.render(screen)
        return []


class Path(NObject):
    """Path class identifies a path.
    """

    def __init__(
        self, y: int, x: int, path: List, closed: bool = False, fmt=curses.A_NORMAL
    ):
        super(Path, self).__init__(y, x, -1, -1, fmt)
        self.path: List = path
        self.closed: bool = closed
        self.motion: str = "none"

    @render
    def render(self, screen) -> List[Event]:
        y = self.y
        x = self.x
        self.motion: str = "none"
        for index, point in enumerate(self.path):
            weight_y = point[0]
            weight_x = point[1]
            if weight_y > 0:
                if self.motion == "x:plus":
                    screen.addstr(y, x, chr(9491), self.fmt)
                    weight_y -= 1
                    y += 1
                if self.motion == "x:minus":
                    screen.addstr(y, x, chr(9487), self.fmt)
                    weight_y -= 1
                    y += 1
                self.motion = "y:plus"
                for dy in range(weight_y):
                    screen.addstr(y + dy, x, chr(9475), self.fmt)
            elif weight_y < 0:
                if self.motion == "x:plus":
                    screen.addstr(y, x, chr(9499), self.fmt)
                    weight_y += 1
                    y -= 1
                if self.motion == "x:minus":
                    screen.addstr(y, x, chr(9495), self.fmt)
                    weight_y += 1
                    y -= 1
                self.motion = "y:minus"
                for dy in range(abs(weight_y)):
                    screen.addstr(y - dy, x, chr(9475), self.fmt)
            y = y + weight_y
            if weight_x > 0:
                if self.motion == "y:plus":
                    screen.addstr(y, x, chr(9495), self.fmt)
                    weight_x -= 1
                    x += 1
                if self.motion == "y:minus":
                    screen.addstr(y, x, chr(9487), self.fmt)
                    weight_x -= 1
                    x += 1
                self.motion = "x:plus"
                for dx in range(weight_x):
                    screen.addstr(y, x + dx, chr(9473), self.fmt)
            elif weight_x < 0:
                if self.motion in "y:plus":
                    screen.addstr(y, x, chr(9499), self.fmt)
                    weight_x += 1
                    x -= 1
                if self.motion in "y:minus":
                    screen.addstr(y, x, chr(9491), self.fmt)
                    weight_x += 1
                    x -= 1
                self.motion = "x:minus"
                for dx in range(abs(weight_x)):
                    screen.addstr(y, x - dx, chr(9473), self.fmt)
            x = x + weight_x
        return []


class TrackPath(String):
    def __init__(
        self, y: int, x: int, path: List, t: Timer, text_data: str, fmt=curses.A_NORMAL
    ):
        super(TrackPath, self).__init__(y, x, text_data, fmt)
        self.path: List = []
        self.timer: Timer = t
        self.tindex: int = 0
        y_pos = self.y
        x_pos = self.x
        self.path.append([y_pos, x_pos, self.fmt])
        for p in path:
            if len(p) == 2:
                y_val, x_val = p
                fmt = self.fmt
            elif len(p) == 3:
                y_val, x_val, fmt = p
            else:
                raise Exception("Improper path entry: {}".format(p))
            max_val = max(abs(y_val), abs(x_val))
            for i in range(max_val):
                if y_val != 0:
                    if y_val > 0:
                        y_val -= 1
                        y_pos += 1
                    else:
                        y_val += 1
                        y_pos -= 1
                if x_val != 0:
                    if x_val > 0:
                        x_val -= 1
                        x_pos += 1
                    else:
                        x_val += 1
                        x_pos -= 1
                self.path.append([y_pos, x_pos, fmt])

    @update
    def update(self, screen: Any, *events: Event) -> List[Event]:
        """update updates a flashing block of strings nobject.
        """
        for event in events:
            if event.evt == EVT.ENG.TIMER:
                if event.get_timer() == self.timer:
                    if self.tindex < len(self.path):
                        self.y = self.path[self.tindex][0]
                        self.x = self.path[self.tindex][1]
                        self.fmt = self.path[self.tindex][2]
                        self.tindex += 1
                    else:
                        self.tindex = 0
        return []


class Shape(String):
    def __init__(self, y: int, x: int, path: List, text_data: str, fmt=curses.A_NORMAL):
        super(Shape, self).__init__(y, x, text_data, fmt)
        self.path: List = []
        y_pos = self.y
        x_pos = self.x
        self.path.append([y_pos, x_pos, self.fmt])
        for p in path:
            if len(p) == 2:
                y_val, x_val = p
                fmt = self.fmt
            elif len(p) == 3:
                y_val, x_val, fmt = p
            else:
                raise Exception("Improper path entry: {}".format(p))
            max_val = max(abs(y_val), abs(x_val))
            for i in range(max_val):
                if y_val != 0:
                    if y_val > 0:
                        y_val -= 1
                        y_pos += 1
                    else:
                        y_val += 1
                        y_pos -= 1
                if x_val != 0:
                    if x_val > 0:
                        x_val -= 1
                        x_pos += 1
                    else:
                        x_val += 1
                        x_pos -= 1
                self.path.append([y_pos, x_pos, fmt])

    @render
    def render(self, screen) -> List[Event]:
        for y, x, fmt in self.path:
            screen.addstr(y, x, self.text_data, fmt)
        return []


class ShapeFromPath(Shape):
    def __init__(self, y: int, x: int, path: List, text_data: str, fmt=curses.A_NORMAL):
        shape_path: List = []
        init: int = 0
        for i, p in enumerate(path):
            shape_path.append(((init - p), 1))
            init = p
        super(ShapeFromPath, self).__init__(y, x, shape_path, text_data, fmt)
