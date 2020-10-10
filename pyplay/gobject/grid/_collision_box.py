class CollisionBox:
    def __init__(self):
        self.box = set()

    def add(self, x, y):
        """add adds a new entry in the collision box.
        """
        self.box.add((x, y))

    def update(self, collision_box):
        """update adds all given entries to the collision box.
        """
        self.box.update(collision_box.box)

    def collision_with(self, other_box):
        """collision_with checks if there is a collision with the given
        collision box. There is a collision if there are common entries in
        both collision box instances.
        """
        return self.box.intersection(other_box.box)

    def collision_with_upper(self, collision_box):
        """collision_wit_upper checks if there is a collision with the upper
        entries in the given collision box.
        """
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

    def check_out_of_width_bounds(self, x, dx):
        """check_out_of_width_bounds returns if the collision box is out of
        bounds in the X axis.
        """
        for (px, _) in self.box:
            if not (x <= px < (x + dx)):
                return True
        return False

    def check_out_of_heigh_bounds(self, y, dy):
        """check_out_of_heigh_bounds returns if the collision box is out of
        bounds in the Y axis.
        """
        for (_, py) in self.box:
            if not (y <= py < (y + dy)):
                return True
        return False

    def __str__(self):
        return str(self.box)
