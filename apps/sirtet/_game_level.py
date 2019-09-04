class GameLevel:
    """GameLevel implements any level/experience instance to be used in any
    game object.
    """

    def __init__(self, **kwargs):
        self.level = kwargs.get("level", 0)
        self.max_level = kwargs.get("max_level", 100)
        self.exp = kwargs.get("exp", 0)
        self.exp_next = kwargs.get("exp_next", 0)
        self.exp_to_give = kwargs.get("to_give", 0)

    def get_next_exp(self):
        """get_next_exp generated the new value for the exp_next attribute.
        """
        self.exp_next += 100

    def add_exp(self, exp):
        """add_exp adds the given experience. Level will be increased
        properly.
        """
        self.exp += exp
        while self.exp > self.exp_next:
            self.level += 1
            self.exp_next = self.get_next_exp()

    def add_level(self, level):
        """add_level adds the given level. Experience will be adjusted
        properly.
        """
        while level > 0:
            level -= 1
            self.level += 2
            self.exp = self.exp_next
            self.exp_next = self.get_next_exp()
