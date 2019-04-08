from typing import Any, Optional
from grafo import Vertex, Edge, Link
from ._content import Content


class XVertex(Vertex):
    __slots__ = ["content", "pos"]

    def __init__(self, label: str, content: Optional[Any] = None):
        super(XVertex, self).__init__(label)
        self.content: Content = content
        self.pos: Any = None

    def call(self, **kwargs):
        return self.content.call(vertex=self, **kwargs)


class XEdge(Edge):
    __slots__ = ["content"]

    def __init__(
        self,
        label: str,
        parent: Vertex,
        child: Vertex,
        link: Optional[Link] = Link.BI,
        content: Optional[Content] = None,
    ):
        super(XEdge, self).__init__(label, parent, child, link)
        self.content: Content = content

    def call_with_link(self, link: Link = Link.DOWN, **kwargs) -> [Any, bool]:
        return self.content.call(link=link, **kwargs)

    def call(self, **kwargs) -> [Any, bool]:
        return self.call_with_link(self.link, **kwargs)

    def call_with_vertices(
        self, src: Vertex = None, dst: Vertex = None, **kwargs
    ) -> [Any, bool]:
        if src == self.parent and dst == self.child:
            return self.call_with_link(Link.DOWN)
        elif src == self.child and dst == self.parent:
            return self.call_with_link(Link.UP)
        elif src is None and dst is None:
            return self.call_with_link(Link.BI)
        else:
            return [None, False]

    def check_with_link(self, link=Link.DOWN, **kwargs) -> [Any, bool]:
        if self.is_allow_with_link(link):
            return self.call_with_link(link, **kwargs)

    def check(self, **kwargs) -> [Any, bool]:
        return self.check_with_link(self.link)

    def check_with_vertices(self, src: Vertex, dst: Vertex, **kwargs) -> [Any, bool]:
        if self.is_allow(src, dst):
            return self.call_with_vertices(src, dst, **kwargs)
