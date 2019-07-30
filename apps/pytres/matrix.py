from collision import CollisionBox
from point import Point

# from cell import Cell


class Matrix:
    def __init__(self, mat, pos, dx, dy):
        self.mat = []
        self.dim = 3
        self.cells = []
        self.pos = []
        self.dx, self.dy = dx, dy
        self.origin = pos
        self.set_mat(mat)
        self.set_pos()

    def _check(self, mat):
        if mat is None or len(mat) != self.dim or len(mat[0]) != self.dim:
            return False
        return True

    def render_pos(self, index, pos):
        return (
            (self.origin.x * self.dx) + (pos.x - self.origin.x) * self.dx,
            (self.origin.y * self.dy) + (pos.y - self.origin.y) * self.dy,
        )

    def get_mat(self):
        return self.mat

    def set_mat(self, mat):
        if not self._check(mat):
            assert False, "wrong matrix dimension: {}".format(mat)
        self.mat = mat[:]
        self.cells = [y for x in self.mat for y in x]

    def set_pos(self):
        self.pos = []
        xo = self.origin.x
        yo = self.origin.y
        for _y in range(0, len(self.mat)):
            y = yo + _y
            for _x in range(0, len(self.mat[0])):
                x = xo + _x
                self.pos.append(Point(x, y))
            x = self.origin.x

    def get_pos(self):
        result = []
        for i, cell in enumerate(self.cells):
            if cell.is_enable():
                result.append(self.pos[i])
        return result

    def get_dim(self):
        return len(self.mat), len(self.mat[0])

    def move(self, x, y):
        self.origin.x += x
        self.origin.y += y
        self.set_pos()

    def rotate_clockwise(self):
        """Rotate nxn matrix by 90 degrees clockwise.
        """
        result = [row[:] for row in self.mat]
        mat = len(self.mat[0])
        for x in range(0, mat):
            for j in range(0, mat):
                result[j][mat - 1 - x] = self.mat[x][j]
        return Matrix(result, self.origin, self.dx, self.dy)

    def rotate_anticlockwise(self):
        """Rotate nxn matrix by 90 degrees anti-clockwise.
        """
        result = [row[:] for row in self.mat]
        mat = len(self.mat[0])
        for x in range(0, mat):
            for j in range(0, mat):
                result[x][j] = self.mat[j][mat - 1 - x]
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

    def render(self, surface, **kwargs):
        """render renders the matrix, calling render method for every cell.
        """
        for i, cell in enumerate(self.cells):
            x, y = self.render_pos(i, self.pos[i])
            cell.render_at(surface, x, y, **kwargs)

    def randomize(self):
        for row in self.mat:
            for col in row:
                col.randomize()
        return self
