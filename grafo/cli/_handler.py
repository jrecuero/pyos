from typing import List, Union
from grafo import Grafo, Edge, Link
from ._node import Node
from ._content import END_TOKEN
from ._context import Context


class Handler(object):
    def __init__(self, **kwargs):
        self.grafo: Grafo = kwargs.get("grafo", Grafo("cli", root="cli"))
        self.context: Context = Context()

    def add_node(
        self, parent: Node, child: Node, loop: bool = False, first: bool = False
    ) -> bool:
        # Grafo adds next node to the previous node if parent is set to None,
        # but for CLI node has to be attached to the root when parent is set to
        # None.
        parent = parent if parent else self.grafo.root
        edge: Edge = Edge("", parent, child, Link.DOWN)
        ok = self.grafo.add_edge(parent, edge, loop, first)
        if not ok:
            assert "Error add_node {} -> {}".format(parent, child)
        edge.auto_label()
        return True

    def add_node_to_context(self, node: Node, token: str) -> Node:
        self.context.add_node(node, token)
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
        self.context.new_match()
        match, index, path = self.find_path(tokens, 0, [])
        return match, index, path

    def match(self, line: str) -> Union[bool, int, List[Node]]:
        tokens = line.split()
        tokens.append(END_TOKEN)
        return self._match(tokens)

    def pop_mode(self):
        if self.context.pop_mode():
            mode_node = self.context.last_command_matched_node()
            cargs = self.context.last_command_matched_args()
            if mode_node.content.builtin:
                cargs["__handler__"] = self
            mode_node.content.the_rcall(**cargs)
            return mode_node.content
        return None

    def run(self, line: str):
        tokens = self.context.flat_modes() if self.context.modes else []
        tokens.extend(line.split())
        tokens.append(END_TOKEN)
        match, index, path = self._match(tokens)
        if match and path[-1].content.is_end():
            command, _ = self.context.match_last_command[0]
            if command.content.is_command():
                cargs = self.context.last_command_matched_args()
                if command.content.builtin:
                    cargs["__handler__"] = self
                command.content.the_call(**cargs)
            if command.content.is_mode():
                self.context.push_mode()

    def exit_mode(self):
        pass
