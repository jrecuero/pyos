from point import Point


class CollisionBox:
    def __init__(self):
        self.box = set()

    def add(self, item):
        self.box.add(item.hash())

    def collision_with(self, other_box):
        return self.box.intersection(other_box.box)

    def collision_with_upper(self, collision):
        upper_box = CollisionBox()
        for x, y in collision:
            upper_box.add(Point(x, y - 1))
        return self.collision_with(upper_box)
