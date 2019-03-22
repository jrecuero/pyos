from typing import Dict, List, Any
from logging import FileHandler
from tools.loggar import get_loggar
from grafo.ider import next_ider
from grafo.vertex import Vertex, Edge, Path, new_static_edge, Link


log = get_loggar("grafo", handler=FileHandler("loggar.log", mode="w"))


class Grafo:
    def __init__(self, label: str):
        self.ider: int = next_ider
        self.label: str = label
        self.root: Vertex = Vertex("root/0")
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

    def add_edge(self, parent: Vertex, edge: Edge):
        if parent is None:
            parent = self.root
            edge.parent = parent
        if not parent.hooked:
            raise Exception("Parent {} not found in grafo".format(parent))
        edge.parent.add_edge(edge)
        edge.child.add_edge(edge)
        edge.child.hooked = True
        self.vertices[edge.child.ider] = edge.child
        self.edges[edge.ider] = edge

    def add_vertex(self, parent: Vertex, child: Vertex):
        if parent is None:
            parent = self.root
        edge: Edge = new_static_edge(parent, child)
        self.add_edge(parent, edge)

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
        if src is None:
            src = self._anchor
        for edge in src.edges:
            if edge.child == dst and edge.link in [Link.DOWN, Link.BI]:
                return edge
            elif edge.parent == dst and edge.link in [Link.UP, Link.BI]:
                return edge
        return None

    def check_edge_from_to(self, src: Vertex, dst: Vertex, **kwargs) -> [Any, bool]:
        if src is None:
            src = self._anchor
        edge = self.exit_edge_to(src, dst)
        if edge:
            return edge.check_with_vertex(src, dst, **kwargs)
        return None, False

    def links_from(self, src: Vertex, vertex_or_edge: bool, **kwargs) -> List[Any]:
        children: List[Any] = []
        if src is None:
            src = self._anchor
        log.Info("[EDGES] {} : {}".format(src, [str(e) for e in src.edges])).call()
        for edge in src.edges:
            dst = edge.peer(src)
            _, ok = self.check_edge_from_to(src, dst, **kwargs)
            if ok:
                if vertex_or_edge:
                    children.append(dst)
                else:
                    children.append(edge)
        return children

    def vertices_from(self, src: Vertex, **kwargs) -> List[Vertex]:
        return self.links_from(src, True, **kwargs)

    def edges_from(self, src: Vertex, **kwargs) -> List[Edge]:
        return self.links_from(src, False, **kwargs)

    def paths_from_v_to_v(
        self, src: Vertex, dst: Vertex, path: List[Edge] = None, **kwargs
    ) -> List[Path]:
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

    def to_mermaid(self) -> str:
        result: str = "graph LR\n"
        for edge in self.edges.values():
            result += "{}\n".format(edge.to_mermaid())
        return result
