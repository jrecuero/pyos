from grafo import log, Link
from grafo.network import XVertex, XEdge, XGrafo, Weight


if __name__ == "__main__":
    v1: XVertex = XVertex("v/1")
    v2: XVertex = XVertex("v/2")
    v3: XVertex = XVertex("v/3")
    v4: XVertex = XVertex("v/4")
    g: XGrafo = XGrafo("network")
    g.add_edge(None, XEdge("edge", None, v1, Link.DOWN, Weight(0)))
    g.add_edge(v1, XEdge("edge", v1, v2, Link.DOWN, Weight(10)))
    g.add_edge(v1, XEdge("edge", v1, v3, Link.DOWN, Weight(5)))
    g.add_edge(v2, XEdge("edge", v2, v4, Link.DOWN, Weight(3)))
    g.add_edge(v3, XEdge("edge", v3, v4, Link.DOWN, Weight(5)))
    log.Test(g.to_mermaid()).call()
    paths = g.paths_from_v_to_v(v1, v4)
    for p in paths:
        log.Test(p).call()
