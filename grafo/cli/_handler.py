from typing import List, Union
from grafo import Grafo, Edge, Link
from ._node import Node
from ._content import END_TOKEN, Kontent
from ._context import Context


class Handler(object):
    def __init__(self, **kwargs):
        self.grafo: Grafo = kwargs.get("grafo", Grafo("cli", root="cli"))
        self.context: Context = Context()

    def add_node(self, parent: Node, child: Node, loop: bool = False) -> bool:
        edge: Edge = Edge("", parent, child, Link.DOWN)
        ok = self.grafo.add_edge(parent, edge, loop)
        if not ok:
            assert "Error add_node {} -> {}".format(parent, child)
        edge.auto_label()
        return True

    def add_node_to_context(self, node: Node, token: str) -> Node:
        self.context.add(node, token)
        return node

    def find_path(
        self, tokens: List[str], index: int, path: List[Node]
    ) -> Union[bool, int, List[Node]]:
        anchor: Node = self.grafo.root if len(path) == 0 else path[-1]
        for child in anchor.children:
            match, next_index = child.match(tokens, index)
            if match:
                path.append(self.add_node_to_context(child, tokens[index]))
                if next_index == len(tokens):
                    self.context.end()
                    return True, next_index, path
                else:
                    return self.find_path(tokens, next_index, path)
        return False, index, path

    def _match(self, tokens: List) -> Union[bool, int, List[Node]]:
        self.context = Context()
        match, index, path = self.find_path(tokens, 0, [])
        return match, index, path

    def match(self, line: str) -> Union[bool, int, List[Node]]:
        tokens = line.split()
        tokens.append(END_TOKEN)
        return self._match(tokens)

    def run(self, line: str):
        tokens = line.split()
        tokens.append(END_TOKEN)
        match, index, path = self._match(tokens)
        if match and path[-1].content.klass == Kontent.END:
            command, _ = self.context.last_command[0]
            if command.content.klass == Kontent.COMMAND:
                cargs = self.context.last_command_args()
                command.content.call(**cargs)

    def exit_mode(self):
        pass
