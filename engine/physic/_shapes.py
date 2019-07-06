from typing import Any, List
from engine import Event, Point, BB, Move, Shape


class StaticShape(Shape):
    def __init__(self, **kwargs):
        super(StaticShape, self).__init__(**kwargs)
        self.movable = False


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
        self.moved: bool = False

    def update(self, screen: Any) -> List[Event]:
        result: List[Event] = []
        if self.movable and self.moved and self._update():
            for bb in self.shape:
                bb.next(self.next_position(bb))
            self.moved = False
        return result

    def move(self, move_to: int):
        def _move():
            self.head.pushed = True
            self.head.move = move_to
            self.moved = True
            return []

        return _move

    def out_of_bounds(self, y: int, x: int, max_y: int, max_x: int) -> bool:
        super(ActorShape, self).out_of_bounds(y, x, max_y, max_x)


class ShooterShape(ActorShape):
    def __init__(self, **kwargs):
        super(ShooterShape, self).__init__(**kwargs)
        self.name = "Actor"
        self.moved: bool = False

    def shoot(self):
        def _shoot():
            self.eventor("shoot", actor=self)
            return []

        return _shoot


class SnakeShape(ShooterShape):
    def __init__(self, **kwargs):
        super(SnakeShape, self).__init__(**kwargs)
        self.name = "Snake"
        self.moved: bool = False

    def append(self, bb):
        if len(self):
            last_bb = self[-1]
            bb.move = last_bb.move
        return super(SnakeShape, self).append(bb)

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


class BulletShape(MoveShape):
    def __init__(self, **kwargs):
        super(BulletShape, self).__init__(**kwargs)
        self.name = "Bullet"
        self.priority = 10
        self.parent: Shape = kwargs.get("parent", None)
        self.timeout: int = self.parent.timeout / 2
        parent_head = self.parent.head
        self.append(
            BB("*", pos=Point(parent_head.y, parent_head.x), move=parent_head.move)
        )

    def out_of_bounds(self, y: int, x: int, max_y: int, max_x: int) -> bool:
        if super(BulletShape, self).out_of_bounds(y, x, max_y, max_x):
            self.eventor("delete", actor=self)

    def collision_with(self, other: "Shape") -> bool:
        if (other != self.parent) and self._collision_with(other):
            if other.collision_callable:
                other.collisioned(self)
            self.eventor("delete", actor=self)
        return False
