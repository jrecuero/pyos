from typing import Dict, List, Any
from ._loggar import log
from ._ider import Iderable
from ._vertex import Vertex, Edge, Path, Link


class Grafo(Iderable):
    __slots__ = ["root", "_anchor", "path", "vertices", "edges"]

    def __init__(self, label: str, **kwargs):
        super(Grafo, self).__init__(label)
        root_name: str = kwargs.get("root", "root/0")
        self.root: Vertex = Vertex(root_name)
        self.root.hooked = True
        self._anchor: Vertex = self.root
        self.path: Path = None
        self.vertices: Dict[int, Vertex] = {}
        self.vertices[self.root.ider] = self.root
        self.edges: Dict[int, Edge] = {}

    @property
    def anchor(self):
        return self._anchor

    @anchor.setter
    def anchor(self, vertex):
        if vertex is None:
            self._anchor = self.root
        elif vertex.ider in self.vertices:
            self._anchor = self.vertices[vertex.ider]
        else:
            raise Exception("Vertex {} not in grafo".format(vertex))

    def add_edge(
        self, parent: Vertex, edge: Edge, loop: bool = False, first: bool = False
    ):
        """add_edge adds a new edge to the grafo and hook it up to the given
        vertex.
        """
        if parent is None:
            parent = self.anchor
            edge.set_parent(parent)
        if not parent.hooked:
            raise Exception("Parent {} not found in grafo".format(parent))
        edge.parent.add_edge(edge, loop, first)
        edge.child.add_edge(edge, loop, first)
        edge.child.hooked = True
        self.vertices[edge.child.ider] = edge.child
        self.edges[edge.ider] = edge
        self.anchor = edge.child

    def add_vertex(self, parent: Vertex, child: Vertex, link: Link = Link.DOWN):
        """add_vertex creates an edge between give vertices and add it to the
        grafo.
        """
        if parent is None:
            parent = self.anchor
        edge: Edge = Edge("static", parent, child, link)
        self.add_edge(parent, edge)
        self.anchor = child

    def hook_edge(self, edge: Edge):
        """hook_edge appends the given edge to the grafo anchor.
        """
        if edge.parent is None:
            return self.add_edge(None, edge)
        return self.add_edge(edge.parent, edge)

    def hook_vertex(self, dst: Vertex, link: Link = Link.DOWN):
        """hook_vertex appends the given vertex to the grafo anchor, in the
        process it creates a static edge between the anchor and the given
        vertex.
        """
        return self.add_vertex(self.anchor, dst, link)

    # def add_vtov(self, edge: Edge):
    #     if edge.parent is None:
    #         edge.parent = self.root
    #     if self._anchor != edge.parent:
    #         raise Exception(
    #             "Edge parent {} is not the anchor".format(edge.parent, self._anchor)
    #         )
    #     self._anchor = edge.child
    #     self.path.edges.append(edge)

    # def set_anchor_to(self, dst: Vertex) -> Vertex:
    #     for edge in self._anchor.edges:
    #         if edge.child == dst:
    #             self.add_vtov(edge)
    #             return self._anchor
    #     return None

    def exit_edge_to(self, src: Vertex, dst: Vertex) -> Edge:
        """exit_edge_to checks if there is a valid link for give vertices
        as source/parent and destination/child
        """
        if src is None:
            src = self.anchor
        for edge in src.edges:
            if edge.child == dst and edge.link in [Link.DOWN, Link.BI]:
                return edge
            elif edge.parent == dst and edge.link in [Link.UP, Link.BI]:
                return edge
        return None

    def links_from(self, src: Vertex, vertex_or_edge: bool) -> List[Any]:
        """links_from returns all edges/vertices from the given vertex.
        """
        children: List[Any] = []
        if src is None:
            src = self.anchor
        log.Info("[EDGES] {} : {}".format(src, [str(e) for e in src.edges])).call()
        for edge in src.edges:
            dst = edge.peer(src)
            # _, ok = self.check_edge_from_to(src, dst, **kwargs)
            if self.exit_edge_to(src, dst):
                if vertex_or_edge:
                    children.append(dst)
                else:
                    children.append(edge)
        return children

    def vertices_from(self, src: Vertex) -> List[Vertex]:
        return self.links_from(src, True)

    def edges_from(self, src: Vertex) -> List[Edge]:
        return self.links_from(src, False)

    def paths_from_v_to_v(
        self, src: Vertex, dst: Vertex, path: List[Edge] = None, **kwargs
    ) -> List[Path]:
        """paths_from_v_to_v returns all valid paths between given vertices.
        """
        paths: List[Path] = []
        if path is None:
            path = []
        if src == dst:
            log.Info(
                "[FOUND] {} to {}, {}".format(src, dst, Path("", path, False))
            ).call()
            paths.append(Path("paths", path, sequential=False))
        else:
            for edge in [e for e in self.edges_from(src) if e not in path]:
                _path: List[Edge] = list(path)
                _path.append(edge)
                log.Info(
                    "[.....] {} to {}, {}, {}".format(
                        src, dst, edge, Path("", path, False)
                    )
                ).call()
                child_paths: List[Path] = self.paths_from_v_to_v(
                    edge.peer(src), dst, _path
                )
                if child_paths:
                    paths.extend(child_paths)
        return paths

    def vertices_in_path(self, src: Vertex, path: List[Edge]) -> List[Vertex]:
        """vertices_in_path returns all ordered vertices in a given path from
        a source vertex.
        """
        vertices: List[Vertex] = [src]
        next_vertex = src
        for edge in path:
            next_vertex = edge.peer(next_vertex)
            vertices.append(next_vertex)
        return vertices

    def to_mermaid(self) -> str:
        result: str = "graph LR\n"
        for edge in self.edges.values():
            result += "{}\n".format(edge.to_mermaid())
        return result
