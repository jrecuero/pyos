from _point import Point


class CollisionBox:
    def __init__(self):
        self.box = set()

    def add(self, pos):
        self.box.add(pos.get())

    def extend(self, other_box):
        self.box.extend(other_box)

    def collision_with(self, other_box):
        return self.box.intersection(other_box.box)

    def collision_with_upper(self, collision):
        upper_box = CollisionBox()
        for x, y in collision:
            upper_box.add(Point(x, y - 1))
        return self.collision_with(upper_box)

    def __str__(self):
        return str(self.box)
