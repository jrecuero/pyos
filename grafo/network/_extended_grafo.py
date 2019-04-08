from typing import List, Any
from grafo import log, Grafo, Vertex
from ._extended_vertex import XEdge
from ._content import Content


class XGrafo(Grafo):

    __slots__ = []

    def __init__(self, label: str):
        super(XGrafo, self).__init__(label)

    def check_edge_from_to(self, src: Vertex, dst: Vertex, **kwargs) -> [Any, bool]:
        """check_edge_from_to verifies if there is an edge between given
        vertices and there is valid link and clearance for that edge for
        those vertices.
        """
        if src is None:
            src = self._anchor
        edge = self.exit_edge_to(src, dst)
        if edge:
            return edge.check_with_vertices(src, dst, **kwargs)
        return None, False

    def connections_from(
        self, src: Vertex, vertex_or_edge: bool, **kwargs
    ) -> List[Any]:
        children: List[Any] = []
        if src is None:
            src = self.anchor
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

    def content_in_path(self, src: Vertex, path: List[XEdge]) -> List[Content]:
        return [e.content for e in path]
