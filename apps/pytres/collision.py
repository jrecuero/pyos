from point import Point


class CollisionBox:
    def __init__(self):
        self.box = set()

    def add(self, item):
        self.box.add(item)

    def collision_with(self, other_box):
        return self.box.intersection(other_box.box)

    def collision_with_upper(self, other_box):
        upper_box = CollisionBox()
        collision = self.collision_with(other_box)
        for pos in collision:
            upper_box.add(Point(pos.x, pos.y - 1))
        return self.collision_with(upper_box)
