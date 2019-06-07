from typing import List, Any
import random
import curses
from engine import (
    log,
    EVT,
    Handler,
    Scene,
    Event,
    # NObject,
    # Char,
    # String,
    # Box,
    # Caller,
    ArrowKeyHandler,
    update_scene,
    render_scene,
    # update_nobj,
    # render_nobj,
    Point,
    Move,
    BB,
    Shape,
    Arena,
)


# class MoveShape(Shape):
#     def __init__(self, **kwargs):
#         super(MoveShape, self).__init__(**kwargs)
#         # self.delta: Point = Point(1, 0)
#         self.delta: Point = Point(0, 1)

#     def back(self):
#         super(MoveShape, self).back()
#         self.delta = self.delta * -1

#     def next_position(self, bb: BB):
#         return bb.pos + self.delta

#     def move(self, move_to):
#         def _move():
#             return []

#         return _move


class MoveShape(Shape):
    def __init__(self, **kwargs):
        super(MoveShape, self).__init__(**kwargs)

    def next_position(self, bb: BB):
        new_pos: Point = Point(bb.y, bb.x)
        if bb.move == Move.UP:
            new_pos.y = bb.y - 1
        elif bb.move == Move.DOWN:
            new_pos.y = bb.y + 1
        elif bb.move == Move.RIGHT:
            new_pos.x = bb.x + 1
        elif bb.move == Move.LEFT:
            new_pos.x = bb.x - 1
        else:
            pass
        return new_pos


class ActorShape(MoveShape):
    def __init__(self, **kwargs):
        super(ActorShape, self).__init__(**kwargs)
        self.name = "Actor"

    def append(self, bb):
        if len(self):
            last_bb = self[-1]
            bb.move = last_bb.move
        return super(ActorShape, self).append(bb)

    def update(self, screen: Any) -> List[Event]:
        result: List[Event] = []
        if self.movable and self._update():
            pushed: bool = False
            pushed_move: int = Move.NONE
            next_pushed: bool = False
            next_pushed_move: int = Move.NONE
            for bb in self.shape:
                bb.next(self.next_position(bb))
                if bb.pushed:
                    next_pushed = bb.pushed
                    next_pushed_move = bb.move
                else:
                    next_pushed = False
                    next_pushed_move = Move.NONE
                if pushed:
                    bb.pushed = True
                    bb.move = pushed_move
                else:
                    bb.pushed = False
                pushed = next_pushed
                pushed_move = next_pushed_move
        return result

    def move(self, move_to: int):
        def _move():
            if Move.allowed(self.head.move, move_to):
                self.head.pushed = True
                self.head.move = move_to
            return []

        return _move

    def shoot(self):
        def _shoot():
            log.Shoot("").call()
            self.eventor("shooting", actor=self)
            return []

        return _shoot


class BulletShape(MoveShape):
    def __init__(self, **kwargs):
        super(BulletShape, self).__init__(**kwargs)
        self.parent: Shape = kwargs.get("parent", None)
        self.timeout: int = self.parent.timeout / 2
        parent_head = self.parent.head
        self.append(
            BB("*", pos=Point(parent_head.y, parent_head.x), move=parent_head.move)
        )


class CoinShape(Shape):
    def __init__(self, **kwargs):
        super(CoinShape, self).__init__(**kwargs)
        self.name = "Coin"
        self.max_y = kwargs.get("max_y", None)
        self.max_x = kwargs.get("max_x", None)
        self.money, pos = self.new_coin(self.max_y, self.max_x)
        self.append(BB(self.money, pos=pos))
        self.movable = False
        self.cash = kwargs.get("cash", None)
        self.collision_callable = True

    def new_coin(self, max_y: int, max_x: int) -> BB:
        return (
            "{}".format(random.randint(1, 9)),
            Point(random.randint(2, max_y), random.randint(2, max_x)),
        )

    def collisioned(self, other: Shape):
        if self.cash and self.cash(other, self.money):
            self.money, pos = self.new_coin(self.max_y, self.max_x)
            self[0].sprite = self.money
            self[0].pos = pos
            return False
        return True

    # def collision_with(self, other: "Shape") -> bool:
    #     if super(CoinShape, self).collision_with(other):
    #         return self.collisioned(other)
    #     return False


class GameHandler(Arena):
    def __init__(self, y: int, x: int, max_y: int, max_x: int, **kwargs):
        super(GameHandler, self).__init__(x, y, max_y, max_x)

    def eventor(self, event, **kwargs):
        actor = kwargs.get("actor", None)
        log.Event("{} is {}".format(actor.name, event)).call()
        self.add_shape(BulletShape(parent=actor), relative=False)


class BoardScene(Scene):
    def __init__(self):
        super(BoardScene, self).__init__("Board Scene")
        self.border = False
        self.max_y: int = curses.LINES - 1
        self.max_x: int = curses.COLS - 1

    def cash(self, bb, money):
        log.Money("{}".format(money)).call()
        return True

    def setup(self, screen: Any):
        self.ghandler = GameHandler(
            2, 2, self.max_y - 4, self.max_x - 4, border_fmt=curses.color_pair(3)
        )
        shape = ActorShape(timeout=5)
        phead = Point(1, 5)
        shape.append(BB("#", pos=phead, move=Move.RIGHT, fmt=curses.color_pair(1)))
        for i in range(2):
            shape.append(BB("-", pos=phead.decr(x=1 + i), fmt=curses.color_pair(2)))
        coin = CoinShape(max_y=self.max_y, max_x=self.max_x, cash=self.cash)
        self.ghandler.add_shape(shape)
        self.ghandler.add_shape(Shape(movable=False).append(BB("$", pos=Point(1, 20))))
        self.ghandler.add_shape(coin)
        self.add_object(self.ghandler)
        self.kh = ArrowKeyHandler(
            left=shape.move(Move.LEFT),
            right=shape.move(Move.RIGHT),
            up=shape.move(Move.UP),
            down=shape.move(Move.DOWN),
            space=shape.shoot(),
        )

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
