from ._grafo import XGrafo


class Network(XGrafo):
    def __init__(self, label: str):
        super(Network, self).__init__(label)
