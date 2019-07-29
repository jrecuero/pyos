from collision import CollisionBox
from point import Point

# from cell import Cell


class Matrix:
    def __init__(self, m, pos, dx, dy):
        self.mat = []
        self.dim = 3
        self.cells = []
        self.pos = []
        self.dx, self.dy = dx, dy
        self.origin = pos
        self.set_mat(m)
        self.set_pos()

    def _check(self, m):
        if m is None or len(m) != self.dim or len(m[0]) != self.dim:
            return False
        return True

    def get_mat(self):
        return self.mat

    def set_mat(self, m):
        if not self._check(m):
            assert False, "wrong matrix dimension: {}".format(m)
        self.mat = m[:]
        self.cells = [y for x in self.mat for y in x]

    def set_pos(self):
        self.pos = []
        xo = self.origin.x
        yo = self.origin.y
        for _y in range(0, len(self.mat)):
            y = yo + _y * self.dy
            for _x in range(0, len(self.mat[0])):
                x = xo + _x * self.dx
                self.pos.append(Point(x, y))
            x = self.origin.x

    def get_dim(self):
        return len(self.mat), len(self.mat[0])

    def move(self, x, y):
        self.origin.x += x * self.dx
        self.origin.y += y * self.dy
        self.set_pos()

    def rotate_clockwise(self):
        """Rotate nxn matrix by 90 degrees clockwise.
        """
        result = [row[:] for row in self.mat]
        m = len(self.mat[0])
        for x in range(0, m):
            for j in range(0, m):
                result[j][m - 1 - x] = self.mat[x][j]
        return Matrix(result, self.origin, self.dx, self.dy)

    def rotate_anticlockwise(self):
        """Rotate nxn matrix by 90 degrees anti-clockwise.
        """
        result = [row[:] for row in self.mat]
        m = len(self.mat[0])
        for x in range(0, m):
            for j in range(0, m):
                result[x][j] = self.mat[j][m - 1 - x]
        return Matrix(result, self.origin, self.dx, self.dy)

    def get_collision_box(self):
        """get_collision_box returns an instance that will be used for any
        collision with this matrix.
        """
        collision_box = CollisionBox()
        for i, cell in enumerate(self.cells):
            cell_collision_box = cell.get_collision_box(self.pos[i])
            if cell_collision_box is not None:
                collision_box.add(cell_collision_box)
        return collision_box

    def collision_with_box(self, other_box):
        """collision_wit_box checks if the matrix collision box collision with
        the given collision box.
        """
        return self.get_collision_box().collision_with(other_box)

    def render(self, ctx, **kwargs):
        """render renders the matrix, calling render method for every cell.
        """
        for i, cell in enumerate(self.cells):
            cell.render_at(ctx, self.pos[i].x, self.pos[i].y, **kwargs)

    def get_collisions_with(self, mat):
        if not self._check(mat):
            assert False, "wrong matrix dimension: {}".format(mat)
        m = len(self.mat[0])
        collisions = []
        for x in range(m):
            for y in range(m):
                if self.mat[x][y].collision(mat[x][y]):
                    collisions.append((x, y))
        return collisions

    def is_collision_with(self, mat):
        return len(self.get_collisions_with(mat)) != 0

    def is_bottom_collision_with(self, mat):
        collisions = self.get_collisions_with(mat)
        m = len(self.mat)
        for entry in collisions:
            if entry[0] == (m - 1):
                return True
        return False

    def randomize(self):
        for row in self.mat:
            for col in row:
                col.randomize()
        return self
