from typing import List, Any

import curses
from engine import (
    # log,
    EVT,
    Handler,
    Scene,
    Event,
    # NObject,
    # Char,
    # String,
    # Box,
    # Caller,
    KeyHandler,
    update_scene,
    render_scene,
    # update_nobj,
    # render_nobj,
    Point,
    BB,
    Shape,
    Arena,
)


class BoardScene(Scene):
    def __init__(self):
        super(BoardScene, self).__init__("Board Scene")
        self.border = False
        self.max_y: int = curses.LINES - 1
        self.max_x: int = curses.COLS - 1

    def setup(self, screen: Any):
        self.arena = Arena(
            2, 2, self.max_y - 4, self.max_x - 4, border_fmt=curses.color_pair(3)
        )
        shape = Shape(timeout=5)
        phead = Point(1, 1)
        shape.append(BB("#", pos=phead, fmt=curses.color_pair(1)))
        for i in range(5):
            shape.append(BB("-", pos=phead.incr(x=1 + i), fmt=curses.color_pair(2)))
        # stone = Shape(movable=False).append(BB("$", Point(1, 20)))
        self.arena.add_shape(shape)
        # self.arena.add_shape(stone)
        self.arena.add_shape(Shape(movable=False).append(BB("$", pos=Point(1, 20))))
        self.add_object(self.arena)
        self.kh = KeyHandler({})
        self.kh.register("x", lambda: exit(0))

    @update_scene
    def update(self, screen: Any, *events: Event) -> List[Event]:
        event_to_return: List[Event] = []
        for event in events:
            if event.evt == EVT.ENG.KEY:
                event_to_return.extend(self.kh.update(event))
        return event_to_return

    @render_scene
    def render(self, screen: Any) -> List[Event]:
        return super(BoardScene, self).render(screen)


if __name__ == "__main__":
    h = Handler()
    board_scene = BoardScene()
    board_scene.colors(
        [
            (curses.COLOR_RED, curses.COLOR_BLACK),
            (curses.COLOR_YELLOW, curses.COLOR_BLACK),
            (curses.COLOR_BLACK, curses.COLOR_WHITE),
        ]
    )
    h.add_scene(board_scene)
    h.run()
