from typing import Optional, List, Union
from grafo import Vertex
from ._content import Content


class Node(Vertex):
    def __init__(self, label: str, content: Optional[Content] = None):
        super(Node, self).__init__(label)
        self.content: Content = content

    def add_parent(self, parent: "Vertex") -> None:
        """add_parent adds a parent node. This has to be added when the
        node belongs to an edge as child.
        """
        self.parents.append(parent)

    def add_child(self, child: "Vertex") -> None:
        """add_child adds a child node. This has to be added when the
        node belongs to an edge as parent.
        """
        self.children.append(child)

    def match(self, tokens: List[str], tindex: int, **kwargs) -> Union[bool, int]:
        return self.content.match(tokens, tindex, **kwargs)

    def help(self, tokens: List[str], tindex: int, **kwargs) -> List[str]:
        return self.content.help(tokens, tindex, **kwargs)

    def complete(self, tokens: List[str], tindex: int, **kwargs) -> List[str]:
        return self.content.complete(tokens, tindex, **kwargs)
