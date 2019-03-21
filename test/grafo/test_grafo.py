from grafo.grafo import Grafo
from grafo.vertex import Vertex, Edge, new_static_edge, Link


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


if __name__ == "__main__":
    v1: Vertex = Vertex("v/1")
    v2: Vertex = Vertex("v/2")
    v3: Vertex = Vertex("v/3")
    v4: Vertex = Vertex("v/4")
    v5: Vertex = Vertex("v/5")
    e1: Edge = new_static_edge(v1, v2, Link.DOWN)
    e2: Edge = new_static_edge(v2, v3)
    e3: Edge = new_static_edge(v1, v3, Link.DOWN)
    e4: Edge = new_static_edge(v2, v4, Link.DOWN)
    e5: Edge = new_static_edge(v3, v5, Link.DOWN)
    e6: Edge = new_static_edge(v4, v5, Link.DOWN)
    e7: Edge = new_static_edge(v5, v2, Link.DOWN)
    g: Grafo = Grafo("root/0")
    eroot: Edge = new_static_edge(None, v1, Link.DOWN)
    g.add_edge(None, eroot)
    g.add_edge(v1, e1)
    g.add_edge(v2, e2)
    g.add_edge(v1, e3)
    g.add_edge(v2, e4)
    g.add_edge(v3, e5)
    g.add_edge(v4, e6)
    g.add_edge(v5, e7)
    print(g.to_mermaid())
