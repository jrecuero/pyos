from _move import Move
from _collision import CollisionBox


class Shape:
    def __init__(self):
        self.cells = []

    @property
    def head(self):
        if len(self.cells):
            return self.cells[0]
        return None

    def add(self, cell):
        self.cells.append(cell)

    def update(self, **kwargs):
        pass

    def back(self):
        pass

    def move_to(self, move, forced=False):
        if forced or Move.allowed(self.head.move, move):
            self.head.pushed = True
            self.head.move = move

    def get_collision_box(self):
        collision_box = CollisionBox
        for cell in self.cells:
            collision_box.extend(cell.get_collision_box())
        return collision_box

    def render(self, surface, **kwargs):
        for cell in self.cells:
            cell.render(surface, **kwargs)
