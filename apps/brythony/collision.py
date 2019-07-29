class CollisionBox:
    def __init__(self):
        self.box = set()

    def add(self, item):
        self.box.add(item)

    def collision_with(self, other_box):
        return self.box.intersection(other_box.box)
