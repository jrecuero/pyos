class Cell:
    def __init__(self, content):
        self._content = content

    @property
    def content(self):
        return self._content

    def equal(self, content):
        return self._content.equal(content)

    def match(self):
        return False

    def collision(self, other):
        return self.match() and other.match()

    def update_with(self, other):
        self._content = other._content

    def clone(self):
        return self.__class__(self._content)

    def randomize(self):
        return self
