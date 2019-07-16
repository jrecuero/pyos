from typing import Any, List, Dict
from engine import Event, Point, BB, Move, Shape


class StaticShape(Shape):
    def __init__(self, **kwargs):
        super(StaticShape, self).__init__(**kwargs)
        self.movable = False


class MoveShape(Shape):
    def __init__(self, **kwargs):
        super(MoveShape, self).__init__(**kwargs)

    def next_position(self, bb: BB) -> Point:
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

    def update(self, screen: Any) -> List[Event]:
        result: List[Event] = []
        if self.movable and self._update():
            for bb in self.shape:
                bb.next(self.next_position(bb))
        return result


class ActorShape(MoveShape):
    def __init__(self, **kwargs):
        super(ActorShape, self).__init__(**kwargs)
        self.name = "Actor"
        # If timeout is zero, it means actor does not move until movemeent is
        # called again.
        self.moved: bool = bool(self.timeout)

    def update(self, screen: Any) -> List[Event]:
        result: List[Event] = []
        if self.movable and self.moved and self._update():
            for bb in self.shape:
                bb.next(self.next_position(bb))
            self.moved = bool(self.timeout)
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
        self.name = "Shooter"

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


class PathShape(MoveShape):
    def __init__(self, **kwargs):
        super(PathShape, self).__init__(**kwargs)
        self.path: List = kwargs.get("path", [])
        self.loop: bool = kwargs.get("loop", False)
        self.bounce: bool = kwargs.get("bounce", False)
        self.single: bool = kwargs.get("single", False)
        self.repeated: int = kwargs.get("repeated", 0)
        self.path_index: int = 0
        self.path_next: Dict = {}
        self.path_step: int = 1
        if len(self.path):
            self.path_next = dict(self.path[self.path_index])
        if self.bounce:
            for p in reversed(self.path):
                new_segment = {"move": Move.reverse(p["move"]), "cycle": p["cycle"]}
                self.path.append(new_segment)

    def next_position(self, bb: BB) -> Point:
        bb.move = self.path_next["move"]
        new_pos = super(PathShape, self).next_position(bb)
        self.path_next["cycle"] = self.path_next["cycle"] - 1
        if self.path_next["cycle"] == 0:
            self.path_index += self.path_step
            self.path_index %= len(self.path)
            if self.single and self.path_index == 0:
                self.movable = False
            elif self.repeated and self.path_index == 0:
                self.repeated -= 1
                if self.repeated == 0:
                    self.movable = False
            self.path_next = dict(self.path[self.path_index])
        return new_pos


class BulletShape(MoveShape):
    def __init__(self, **kwargs):
        super(BulletShape, self).__init__(**kwargs)
        self.name = "Bullet"
        self.priority = 10
        self.bulleter = True
        self.parent: Shape = kwargs.get("parent", None)
        self.timeout: int = self.parent.timeout / 2
        parent_head = self.parent.head
        move = kwargs.get("move", parent_head.move)
        self.append(BB("*", pos=Point(parent_head.y, parent_head.x), move=move))

    def out_of_bounds(self, y: int, x: int, max_y: int, max_x: int) -> bool:
        if super(BulletShape, self).out_of_bounds(y, x, max_y, max_x):
            self.eventor("delete", actor=self)

    def collisioned(self, other: "Shape") -> bool:
        self.eventor("delete", actor=self)
        return True

    def collision_with(self, other: "Shape") -> bool:
        if (other != self.parent) and self._collision_with(other):
            # if other.collision_callable:
            #     other.collisioned(self)
            # self.eventor("delete", actor=self)
            return True
        return False


class BreakableShape(StaticShape):
    def __init__(self, **kwargs):
        super(BreakableShape, self).__init__(**kwargs)
        self.breakable = True

    def collisioned(self, other: "Shape"):
        if other.bulleter:
            self.eventor("delete", actor=self)
        return True
