from ._content import Content


class Weight(Content):
    __slots__ = ["weight"]

    def __init__(self, weight: int):
        super(Weight, self).__init__(lambda: [weight, True])
        self.weight: int = weight

    def __str__(self) -> str:
        return "{}".format(self.weight)
