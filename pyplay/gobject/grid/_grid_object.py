from ..._gobject import GObject


class GridObject(GObject):
    """GridObject implements a graphical object in a grid.
    """

    def __init__(self, name, x, y, dx, dy, **kwargs):
        super(GridObject, self).__init__(name, x, y, dx, dy, **kwargs)
        self.gridx = x
        self.gridy = y
