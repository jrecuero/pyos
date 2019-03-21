from typing import List, Any, Optional
from grafo.ider import next_ider


class Link:
    NONE: int = 0
    DOWN: int = 1
    UP: int = 2
    BI: int = 3


class Vertex:
    def __init__(self, label: str):
        self.ider: int = next_ider()
        self.label: str = label
        self.parents: List["Vertex"] = []
        self.children: List["Vertex"] = []
        self.edges: List["Edge"] = []
        # self.traversed: List["VtoV"] = []
        self.content: Any = None
        self.hooked: bool = False
        self.pos: Any = None
        self.content: Any = None

    def __str__(self) -> str:
        return self.label

    def add_parent(self, parent: "Vertex") -> None:
        if self != parent:
            self.parents.append(parent)

    def add_child(self, child: "Vertex") -> None:
        if self != child:
            self.children.append(child)

    def add_edge(self, edge: "Edge") -> bool:
        if self not in [edge.parent, edge.child]:
            return False
        self.edges.append(edge)
        self.add_parent(edge.parent)
        self.add_child(edge.child)
        return True


class VtoV:
    def __init__(self, parent: Vertex, child: Vertex):
        self.ider: int = next_ider()
        self.parent: Vertex = parent
        self.child: Vertex = child
        self.vertices: List[Vertex] = [parent, child]

    def __str__(self) -> str:
        return "{} : {}".format(self.parent, self.child)


class Edge(VtoV):
    def __init__(
        self, parent: Vertex, child: Vertex, clearance_cb: Any, link: Link = Link.BI
    ):
        super(Edge, self).__init__(parent, child)
        self.clearance_cb: Any = clearance_cb
        self.link: Link = link
        self.content: Any = None

    def peer(self, vertex: Vertex) -> Vertex:
        if vertex == self.parent:
            return self.child
        elif vertex == self.child:
            return self.parent
        return None

    def is_allow(self, src: Vertex, dst: Vertex) -> bool:
        if self.link == Link.NONE:
            return False
        elif self.link == Link.BI:
            return src in self.vertices or dst in self.vertices
        elif self.link == Link.DOWN:
            return src == self.parent and dst == self.child
        elif self.link == Link.UP:
            return src == self.child and dst == self.parent
        return False

    def is_allow_down(self) -> bool:
        return self.link in [Link.BI, Link.DOWN]

    def is_allow_up(self) -> bool:
        return self.link in [Link.BI, Link.UP]

    def is_allow_bi(self) -> bool:
        return self.link == Link.BI

    def is_cut(self) -> bool:
        return self.link == Link.NONE

    def check_down(self, **kwargs) -> [Any, bool]:
        if self.is_allow_down():
            return self.clearance_cb(self.parent, self.child, Link.DOWN, **kwargs)
        return None, False

    def check_up(self, **kwargs) -> [Any, bool]:
        if self.is_allow_up():
            return self.clearance_cb(self.parent, self.child, Link.UP, **kwargs)
        return None, False

    def check_bi(self, **kwargs) -> [Any, bool]:
        if self.is_allow_bi():
            return self.clearance_cb(self.parent, self.child, Link.BI, **kwargs)
        return None, False

    def check(self, link: Link = Link.DOWN, **kwargs) -> [Any, bool]:
        if link == Link.DOWN:
            return self.check_down(**kwargs)
        elif link == Link.UP:
            return self.check_up(**kwargs)
        elif link == Link.BI:
            return self.check_bi(**kwargs)
        return None, False

    def check_with_vertex(
        self, src: Vertex = None, dst: Vertex = None, **kwargs
    ) -> [Any, bool]:
        if src == self.parent and dst == self.child:
            return self.check_down(**kwargs)
        elif src == self.child and dst == self.parent:
            return self.check_up(**kwargs)
        elif src is None and dst is None:
            return self.check_bi(**kwargs)
        else:
            return [None, False]

    def __str__(self) -> str:
        if self.link == Link.BI:
            return "{} <-> {}".format(self.parent, self.child)
        elif self.link == Link.DOWN:
            return "{} -> {}".format(self.parent, self.child)
        elif self.link == Link.UP:
            return "{} <- {}".format(self.parent, self.child)
        else:
            return "{} xxx {}".format(self.parent, self.child)

    def to_mermaid(self) -> str:
        if self.link == Link.DOWN:
            return "{} --> {}".format(self.parent, self.child)
        elif self.link == Link.UP:
            return "{} --> {}".format(self.child, self.parent)
        elif self.link == Link.BI:
            return "{} --- {}".format(self.parent, self.child)
        return ""


class Path:
    def __init__(
        self, label: str, edges: Optional[List[Edge]] = None, sequential: bool = True
    ):
        self.ider: int = next_ider()
        self.label: str = label
        self.edges: List[Edge] = edges if edges else []
        self.sequential: bool = sequential
        if self.sequential and len(self.edges) > 1:
            for index in range(len(self.edges) - 1):
                if self.edges[index].child != self.edges[index + 1].parent:
                    raise Exception("Path: Edges are not sequential")

    def add(self, edge: Edge) -> bool:
        if self.sequential and len(self.edges) and self.edges[-1].child != edge.parent:
            return False
        self.edges.append(edge)
        return True

    def __str__(self) -> str:
        result: str = ""
        if self.sequential:
            if len(self.edges):
                result = " -> ".join([e.parent.label for e in self.edges])
                result += " -> {}".format(self.edges[-1].child)
        else:
            result = " : ".join(
                ["{} -> {}".format(e.parent, e.child) for e in self.edges]
            )
        return result

    def to_mermaid(self) -> str:
        result: str = ""
        for edge in self.edges:
            result += "{} --> {}\n".format(edge.parent, edge.child)
        return result


def new_static_edge(parent: Vertex, child: Vertex, link: Link = Link.BI) -> Edge:
    return Edge(parent, child, lambda p, c, l: (None, True), link)
