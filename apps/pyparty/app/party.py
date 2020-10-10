class Party:
    def __init__(self, members):
        self.members = {m: False for m in members}
        self.playing = False
        self.name = "Internet Party"

    def activate(self, member):
        if member in self.members:
            self.members[member] = True

    def play(self):
        if self.playing:
            return "You are in the game"
        elif all(self.members.values()):
            self.playing = True
            return "Now Playing"
        else:
            return f"missing players {[k for (k, v) in self.members.items() if not v]}"


party = Party(["JOSE", "MARCELA"])
