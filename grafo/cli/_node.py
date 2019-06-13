from typing import Optional, List, Tuple
from grafo import Vertex
from ._content import Content


class Node(Vertex):
    def __init__(self, label: str, content: Optional[Content] = None):
        super(Node, self).__init__(label)
        self.content: Content = content

    def match(self, tokens: List[str], tindex: int, **kwargs) -> Tuple:
        return self.content.match(tokens, tindex, **kwargs)

    def help(self, tokens: List[str], tindex: int, **kwargs) -> List[str]:
        return self.content.help(tokens, tindex, **kwargs)

    def complete(self, tokens: List[str], tindex: int, **kwargs) -> List[str]:
        return self.content.complete(tokens, tindex, **kwargs)
