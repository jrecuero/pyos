from _move import Move
from _collision import CollisionBox


class Cell:
    def __init__(self, content, pos=None, move=Move.NONE, pushed=False):
        self.content = content
        self.pos = pos
        self.move = move
        self.pushed = pushed

    def __str__(self):
        return str(self.pos)

    @property
    def y(self):
        return self.pos.y

    @y.setter
    def y(self, val):
        self.pos.y = val

    @property
    def x(self):
        return self.pos.x

    @x.setter
    def x(self, val):
        self.pos.x = val

    def update_with(self, other_cell):
        self.content = other_cell.content

    def clone(self):
        return self.__class__(self.content, self.pos)

    def enable(self):
        self.content.enable()

    def disable(self):
        self.content.disable()

    def is_enable(self):
        return self.content.is_enable()

    def get_collision_box(self, pos=None):
        collision_box = CollisionBox()
        if self.content.is_enable():
            collision_box.add(self.pos if pos is None else pos)
        return collision_box

    def render(self, surface, **kwargs):
        if self.pos is not None:
            self.render_at(surface, self.pos.x, self.pox.y, **kwargs)

    def render_at(self, surface, x, y, **kwargs):
        self.content.render_at(surface, x, y, **kwargs)
