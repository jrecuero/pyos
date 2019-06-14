from typing import List, Union
from grafo import Grafo, Edge, Link
from ._node import Node
from ._context import Context


class Handler(object):
    def __init__(self, **kwargs):
        self.grafo: Grafo = kwargs.get("grafo", Grafo("cli", root="cli"))
        self.context: Context = Context()

    def add_node(self, parent: Node, child: Node) -> bool:
        edge: Edge = Edge("", parent, child, Link.DOWN)
        ok = self.grafo.add_edge(parent, edge)
        if not ok:
            assert "Error add_node {} -> {}".format(parent, child)
        edge.auto_label()
        return True

    def find_path(
        self, tokens: List[str], index: int, path: List[Node]
    ) -> Union[bool, int, List[Node]]:
        anchor: Node = self.grafo.root if len(path) == 0 else path[-1]
        for child in anchor.children:
            match, next_index = child.match(tokens, index)
            if match:
                path.append(child)
                if next_index == len(tokens):
                    return True, next_index, path
                else:
                    return self.find_path(tokens, next_index, path)
        return False, index, path
