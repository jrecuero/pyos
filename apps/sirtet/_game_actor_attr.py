class GameActorAttr:
    def __init__(self, name, max, **kwargs):
        self.name = name
        self._max = max
        self._real = max
        self._buffs = []

    @property
    def real(self):
        """real property returns the actual value for the attribute at any
        given time. It is the result to add the real component with all buffs.
        """
        return self._real + sum(self._buffs)

    @real.setter
    def real(self, value):
        """real setter sets the actual value for the property, which never
        should be greater than the maximum value.
        """
        self._real = value
        if self._real > self._max:
            self._real = self._max

    @property
    def max(self):
        """max property returns the maximum value for the attribute.
        """
        return self._max

    @max.setter
    def max(self, value):
        """max setter sets the maximum value for the attribute.
        """
        self._max = value

    def add_buff(self, buff):
        """add_buff adds a new buff value to the attribute.
        """
        self._buffs.append(buff)

    def del_buff(self, buff):
        """del_buff deletes a buff from the attribute.
        """
        self._buffs.remove(buff)
