class GameActorAttr:
    def __init__(self, name, max, **kwargs):
        self.name = name
        self._max = max
        self._real = max
        self._buffs = []

    @property
    def real(self):
        return self._real + sum(self._buffs)

    @real.setter
    def real(self, value):
        self._real = value
        if self._real > self._max:
            self._real = self._max

    @property
    def max(self):
        return self._max

    @max.setter
    def max(self, value):
        self._max = value

    def add_buff(self, buff):
        self._buffs.append(buff)
