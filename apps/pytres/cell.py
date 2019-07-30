class Cell:
    def __init__(self, content, pos=None):
        self.content = content
        self.pos = pos

    def equal(self, content):
        return self.content.equal(content)

    def match(self):
        return False

    def collision(self, other):
        return self.match() and other.match()

    def update_with(self, other):
        self.content = other.content

    def clone(self):
        return self.__class__(self.content)

    def randomize(self):
        return self

    def enable(self):
        self.content.enable()

    def disable(self):
        self.content.disable()

    def is_enable(self):
        return self.content.is_enable()

    def get_collision_box(self, pos=None):
        if self.content.is_enable():
            return self.pos if pos is None else pos
        else:
            return None

    def render(self, surface, **kwargs):
        if self.pos is not None:
            self.render_at(surface, self.pos.x, self.pos.y, **kwargs)

    def render_at(self, surface, x, y, **kwargs):
        self.content.render_at(surface, x, y, **kwargs)
