from typing import Optional, List, Union
from grafo import Vertex
from ._content import Content, HookContent


class Node(Vertex):
    def __init__(self, label: str, content: Optional[Content] = None):
        super(Node, self).__init__(label)
        self.content: Content = content

    def match(self, tokens: List[str], tindex: int, **kwargs) -> Union[bool, int]:
        return self.content.match(tokens, tindex, **kwargs)

    def help(self, tokens: List[str], tindex: int, **kwargs) -> List[str]:
        return self.content.help(tokens, tindex, **kwargs)

    def complete(self, tokens: List[str], tindex: int, **kwargs) -> List[str]:
        return self.content.complete(tokens, tindex, **kwargs)


class HookNode(Node):
    def __init__(self, label):
        super(HookNode, self).__init__(label, content=HookContent())

    def help(self, tokens: List[str], tindex: int, **kwargs) -> List[str]:
        return []

    def complete(self, tokens: List[str], tindex: int, **kwargs) -> List[str]:
        return []


class LoopNode(HookNode):
    def __init__(self, label):
        super(LoopNode, self).__init__(label, content=None)
