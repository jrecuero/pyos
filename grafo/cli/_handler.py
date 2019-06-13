from grafo import Grafo
from ._context import Context


class Handler(object):
    def __init__(self, **kwargs):
        self.grafo: Grafo = kwargs.get("grafo", Grafo("cli"))
        self.context: Context = Context()
