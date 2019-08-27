class CollisionBox:
    def __init__(self):
        self.box = set()

    def add(self, x, y):
        self.box.add((x, y))

    def update(self, collision_box):
        self.box.update(collision_box.box)

    def collision_with(self, other_box):
        return self.box.intersection(other_box.box)

    def collision_with_upper(self, collision_box):
        upper_box = CollisionBox()
        for x, y in collision_box:
            upper_box.add((x, y - 1))
        return self.collision_with(upper_box)

    def check_out_of_bounds(self, x, y, dx, dy):
        """check_out_of_bounds returns if the collision box is out of bounds,
        returning True, or it is inside bounds returning False.
        """
        for (px, py) in self.box:
            if not (x <= px < (x + dx)):
                return True
            if not (y <= py < (y + dy)):
                return True
        return False

    def __str__(self):
        return str(self.box)
