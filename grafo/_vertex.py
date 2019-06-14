from typing import List, Optional
from ._ider import Iderable


class Link:
    NONE: int = 0
    DOWN: int = 1
    UP: int = 2
    BI: int = 3


class Vertex(Iderable):
    __slots__ = ["parents", "children", "edges", "hooked"]

    def __init__(self, label: str):
        super(Vertex, self).__init__(label)
        self.parents: List["Vertex"] = []
        self.children: List["Vertex"] = []
        self.edges: List["Edge"] = []
        self.hooked: bool = False

    def __str__(self) -> str:
        return self.label

    def add_parent(self, parent: "Vertex", loop: bool = False) -> None:
        """add_parent adds a parent vertex. This has to be added when the
        vertex belongs to an edge as child.
        """
        if (loop or self != parent) and (parent not in self.parents):
            self.parents.append(parent)

    def add_child(self, child: "Vertex", loop: bool = False) -> None:
        """add_child adds a child vertex. This has to be added when the
        vertex belongs to an edge as parent.
        """
        if (loop or self != child) and (child not in self.children):
            self.children.append(child)

    def add_edge(self, edge: "Edge", loop: bool = False) -> bool:
        """add_edge adds an edge to the vertex. This has to be added when the
        vertex belongs to an edge as parent or child.
        """
        if self not in [edge.parent, edge.child]:
            return False
        self.edges.append(edge)
        self.add_parent(edge.parent, loop)
        self.add_child(edge.child, loop)
        return True


class VtoV(Iderable):
    __slots__ = ["parent", "child", "vertices"]

    def __init__(self, label: str, parent: Vertex, child: Vertex):
        super(VtoV, self).__init__(label)
        self.parent: Vertex = parent
        self.child: Vertex = child
        self.vertices: List[Vertex] = [parent, child]

    def __str__(self) -> str:
        return "{} : {}".format(self.parent, self.child)


class Edge(VtoV):
    __slots__ = ["link", "src", "dst"]

    def __init__(self, label: str, parent: Vertex, child: Vertex, link: Link = Link.BI):
        super(Edge, self).__init__(label, parent, child)
        self.link: Link = link
        self.set_parent(parent)

    def set_parent(self, parent: Vertex):
        self.parent = parent
        self.src = self.parent if self.link != Link.UP else self.child
        self.dst = self.child if self.link != Link.UP else self.parent

    def auto_label(self):
        self.label = "{}-{}".format(self.parent.label, self.child.label)

    def peer(self, vertex: Vertex) -> Vertex:
        """peer looks for the other vertex in the edge
        """
        if vertex == self.parent:
            return self.child
        elif vertex == self.child:
            return self.parent
        return None

    def is_allow(self, src: Vertex, dst: Vertex) -> bool:
        """is_allow verifies if there is a valid link between given vertices.
        """
        if self.link == Link.NONE:
            return False
        elif self.link == Link.BI:
            return src in self.vertices or dst in self.vertices
        return src == self.src and dst == self.dst

    def is_allow_with_link(self, link=Link.DOWN) -> bool:
        if self.link == Link.BI:
            return True
        return self.link == link

    def is_allow_down(self) -> bool:
        return self.link in [Link.BI, Link.DOWN]

    def is_allow_up(self) -> bool:
        return self.link in [Link.BI, Link.UP]

    def is_allow_bi(self) -> bool:
        return self.link == Link.BI

    def is_cut(self) -> bool:
        return self.link == Link.NONE

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
            return "{} --> {}".format(self.src, self.dst)
        elif self.link == Link.UP:
            return "{} --> {}".format(self.src, self.dst)
        elif self.link == Link.BI:
            return "{} --- {}".format(self.src, self.dst)
        return ""


class Path(Iderable):
    __slots__ = ["edges", "sequential"]

    def __init__(
        self, label: str, edges: Optional[List[Edge]] = None, sequential: bool = True
    ):
        super(Path, self).__init__(label)
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
