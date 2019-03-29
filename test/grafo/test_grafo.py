from grafo.grafo import Grafo
from grafo.vertex import Vertex, new_static_edge, Link
from tools.loggar import get_loggar


def test_new_grafo():
    label = "root/0"
    g = Grafo(label)
    root = g.root
    anchor = g.anchor
    assert g.label == label, "Error: grafo: label got {} exp {}".format(g.label, label)
    assert root is not None, "Error: grafo: root not None {}".format(root)
    assert root == anchor, "Error: grafo: root {} anchor {}".format(root, anchor)
    assert g.path is None, "Error: grafo: path is not None {}".format(g.path)
    got = len(g.vertices)
    assert got == 1, "Error: grafo: len vertices got {} exp {}".format(got, 1)


def test_add_edge():
    g = Grafo("root/0")
    root = g.root
    parent = Vertex("parent/1")
    root_edge = new_static_edge(None, parent)
    g.add_edge(None, root_edge)
    got = root_edge.parent
    assert got == root, "Error: add edge: parent got {} exp {}".format(got, root)
    got = len(parent.parents)
    assert got == 1, "Error: add edge: len parents got {} exp {}".format(got, 1)
    got = parent.parents[0]
    assert got == root, "Error: add edge: parent parent got {} exp {}".format(got, root)


def test_grafo_path():
    v1: Vertex = Vertex("v/1")
    v2: Vertex = Vertex("v/2")
    v3: Vertex = Vertex("v/3")
    v4: Vertex = Vertex("v/4")
    v5: Vertex = Vertex("v/5")
    v6: Vertex = Vertex("v/6")
    v7: Vertex = Vertex("v/7")
    g: Grafo = Grafo("root/0")
    g.add_edge(None, new_static_edge(None, v1, Link.DOWN))
    e_v1_v2 = new_static_edge(v1, v2, Link.DOWN)
    e_v1_v3 = new_static_edge(v1, v3, Link.DOWN)
    e_v2_v3 = new_static_edge(v2, v3, Link.DOWN)
    e_v2_v4 = new_static_edge(v2, v4, Link.DOWN)
    e_v2_v5 = new_static_edge(v2, v5, Link.DOWN)
    e_v3_v5 = new_static_edge(v3, v5, Link.DOWN)
    e_v3_v6 = new_static_edge(v3, v6, Link.DOWN)
    e_v4_v7 = new_static_edge(v4, v7, Link.DOWN)
    e_v6_v7 = new_static_edge(v6, v7, Link.DOWN)
    g.add_edge(v1, e_v1_v2)
    g.add_edge(v1, e_v1_v3)
    g.add_edge(v2, e_v2_v3)
    g.add_edge(v2, e_v2_v4)
    g.add_edge(v2, e_v2_v5)
    g.add_edge(v3, e_v3_v5)
    g.add_edge(v3, e_v3_v6)
    g.add_edge(v4, e_v4_v7)
    g.add_edge(v6, e_v6_v7)
    paths = g.paths_from_v_to_v(v1, v7)
    got = len(paths)
    assert got == 3, "Error: paths: len got {} exp {}".format(got, 3)
    exp = [
        [e_v1_v2, e_v2_v3, e_v3_v6, e_v6_v7],
        [e_v1_v2, e_v2_v4, e_v4_v7],
        [e_v1_v3, e_v3_v6, e_v6_v7],
    ]
    for p in paths:
        if p.edges not in exp:
            assert False, "Error:paths: path {} not found".format(p)


if __name__ == "__main__":
    log = get_loggar("grafo")
    v1: Vertex = Vertex("v/1")
    v2: Vertex = Vertex("v/2")
    v3: Vertex = Vertex("v/3")
    v4: Vertex = Vertex("v/4")
    v5: Vertex = Vertex("v/5")
    v6: Vertex = Vertex("v/6")
    v7: Vertex = Vertex("v/7")
    g: Grafo = Grafo("root/0")
    g.add_edge(None, new_static_edge(None, v1, Link.DOWN))
    g.add_edge(v1, new_static_edge(v1, v2, Link.DOWN))
    g.add_edge(v1, new_static_edge(v1, v3, Link.DOWN))
    g.add_edge(v2, new_static_edge(v2, v3, Link.DOWN))
    g.add_edge(v2, new_static_edge(v2, v4, Link.DOWN))
    g.add_edge(v2, new_static_edge(v2, v5, Link.DOWN))
    g.add_edge(v3, new_static_edge(v3, v5, Link.DOWN))
    g.add_edge(v3, new_static_edge(v3, v6, Link.DOWN))
    g.add_edge(v4, new_static_edge(v4, v7, Link.DOWN))
    g.add_edge(v6, new_static_edge(v6, v7, Link.DOWN))
    log.Test(g.to_mermaid()).call()
    paths = g.paths_from_v_to_v(v1, v7)
    # paths = g.paths_from_v_to_v(v5, v7)
    for p in paths:
        log.Test(p).call()
