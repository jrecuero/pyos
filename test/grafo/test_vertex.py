# import pytest

from grafo import Vertex, Edge, Link, Path


def test_new_vertex():
    label = "vertex/0"
    vertex = Vertex(label)
    assert vertex.label == label, "Error: new vertex : label got {} exp {}".format(
        vertex.label, label
    )


def test_add():
    vertex = Vertex("vertex/0")
    p_vertex = Vertex("parent/0")
    vertex.add_parent(p_vertex)
    got = len(vertex.parents)
    assert got == 1, "Error: add parent: len got {} exp {}".format(got, 1)
    got, exp = vertex.parents[-1], p_vertex
    assert got == exp, "Error: add parent: got {} exp {}".format(got, exp)
    c_vertex = Vertex("child/0")
    vertex.add_child(c_vertex)
    got, exp = len(vertex.children), 1
    assert got == exp, "Error: add child: len got {} exp {}".format(got, exp)
    got, exp = vertex.children[-1], c_vertex
    assert got == exp, "Error: add child: got {} exp {}".format(got, exp)


def test_add_edge():
    parent_v = Vertex("root/1")
    child_v = Vertex("child/1")
    edge = Edge("edge", parent_v, child_v)
    parent_v.add_edge(edge)
    child_v.add_edge(edge)
    got, exp = len(parent_v.edges), 1
    assert got == exp, "Error: add_edge : parent len got {} exp {}".format(got, exp)
    got, exp = len(child_v.edges), 1
    assert got == exp, "Error: add_edge : child len got {} exp {}".format(got, exp)
    got, exp = len(parent_v.parents), 0
    assert got == exp, "Error: add edge: len parent got {} exp {}".format(got, exp)
    got, exp = parent_v.children[-1], child_v
    assert got == exp, "Error: add edge: child got {} exp {}".format(got, exp)
    got, exp = child_v.parents[-1], parent_v
    assert got == exp, "Error: add edge: child got {} exp {}".format(got, exp)
    got, exp = len(child_v.children), 0
    assert got == exp, "Error: add edge: len child got {} exp {}".format(got, exp)


def test_edge_peer():
    v1: Vertex = Vertex("vertex/0")
    v2: Vertex = Vertex("vertex/1")
    edge: Edge = Edge("edge", v1, v2)
    got, exp = edge.peer(v2), v1
    assert got == exp, "Error: peer got {} exp {}".format(got, exp)
    got, exp = edge.peer(v1), v2
    assert got == exp, "Error: peer got {} exp {}".format(got, exp)


def test_new_edge():
    parent: Vertex = Vertex("parent/0")
    child: Vertex = Vertex("child/0")
    edge: Edge = Edge("edge", parent, child)
    assert edge.parent == parent, "Error: new edge: parent got {} exp {}".format(
        edge.parent, parent
    )
    assert edge.child == child, "Error: new edge: child got {} exp {}".format(
        edge.child, child
    )
    assert edge.link == Link.BI, "Error: new edge: link got {} exp {}".format(
        edge.link, Link.BI
    )


def test_allow():
    parent: Vertex = Vertex("parent/0")
    child: Vertex = Vertex("child/0")
    edge: Edge = Edge("edge", parent, child)
    assert edge.is_allow_down(), "Error: is allow down failed"
    assert edge.is_allow_up(), "Error: is allow up failed"
    assert edge.is_allow_bi(), "Error: is allow bi failed"
    assert not edge.is_cut(), "Error: is cut failed"
    assert edge.is_allow(parent, child), "Error: is allow parent-to-child failed"
    assert edge.is_allow(child, parent), "Error: is allow child-to-parent failed"

    edge: Edge = Edge("edge", parent, child, link=Link.BI)
    assert edge.is_allow_down(), "Error: is allow down failed"
    assert edge.is_allow_up(), "Error: is allow up failed"
    assert edge.is_allow_bi(), "Error: is allow bi failed"
    assert not edge.is_cut(), "Error: is cut failed"
    assert edge.is_allow(parent, child), "Error: is allow parent-to-child failed"
    assert edge.is_allow(child, parent), "Error: is allow child-to-parent failed"

    edge: Edge = Edge("edge", parent, child, link=Link.DOWN)
    assert edge.is_allow_down(), "Error: is allow down failed"
    assert not edge.is_allow_up(), "Error: is allow up failed"
    assert not edge.is_allow_bi(), "Error: is allow bi failed"
    assert not edge.is_cut(), "Error: is cut failed"
    assert edge.is_allow(parent, child), "Error: is allow parent-to-child failed"
    assert not edge.is_allow(child, parent), "Error: is allow child-to-parent failed"

    edge: Edge = Edge("edge", parent, child, link=Link.UP)
    assert not edge.is_allow_down(), "Error: is allow down failed"
    assert edge.is_allow_up(), "Error: is allow up failed"
    assert not edge.is_allow_bi(), "Error: is allow bi failed"
    assert not edge.is_cut(), "Error: is cut failed"
    assert not edge.is_allow(parent, child), "Error: is allow parent-to-child failed"
    assert edge.is_allow(child, parent), "Error: is allow child-to-parent failed"

    edge: Edge = Edge("edge", parent, child, link=Link.NONE)
    assert not edge.is_allow_down(), "Error: is allow down failed"
    assert not edge.is_allow_up(), "Error: is allow up failed"
    assert not edge.is_allow_bi(), "Error: is allow bi failed"
    assert edge.is_cut(), "Error: is cut failed"
    assert not edge.is_allow(parent, child), "Error: is allow parent-to-child failed"
    assert not edge.is_allow(child, parent), "Error: is allow child-to-parent failed"


# def test_check():
#     parent: Vertex = Vertex("parent/0")
#     child: Vertex = Vertex("child/0")
#     edge: Edge = Edge("edge", parent, child, lambda p, c, l: ("OK", True))
#     got = edge.check()
#     assert got == ("OK", True), "Error: check got {} exp {}".format(got, ("OK", True))
#     got = edge.check_bi()
#     assert got == ("OK", True), "Error: check got {} exp {}".format(got, ("OK", True))
#     got = edge.check_down()
#     assert got == ("OK", True), "Error: check got {} exp {}".format(got, ("OK", True))
#     got = edge.check_up()
#     assert got == ("OK", True), "Error: check got {} exp {}".format(got, ("OK", True))
#     got = edge.check_with_vertex(parent, child)
#     assert got == ("OK", True), "Error: check got {} exp {}".format(got, ("OK", True))
#     got = edge.check_with_vertex(child, parent)
#     assert got == ("OK", True), "Error: check got {} exp {}".format(got, ("OK", True))

#     edge: Edge = Edge("edge", parent, child, lambda p, c, l: ("OK", True), link=Link.BI)
#     got = edge.check()
#     assert got == ("OK", True), "Error: check got {} exp {}".format(got, ("OK", True))
#     got = edge.check_bi()
#     assert got == ("OK", True), "Error: check got {} exp {}".format(got, ("OK", True))
#     got = edge.check_down()
#     assert got == ("OK", True), "Error: check got {} exp {}".format(got, ("OK", True))
#     got = edge.check_up()
#     assert got == ("OK", True), "Error: check got {} exp {}".format(got, ("OK", True))
#     got = edge.check_with_vertex(parent, child)
#     assert got == ("OK", True), "Error: check got {} exp {}".format(got, ("OK", True))
#     got = edge.check_with_vertex(child, parent)
#     assert got == ("OK", True), "Error: check got {} exp {}".format(got, ("OK", True))

#     edge: Edge = Edge(
#         "edge", parent, child, lambda p, c, l: ("OK", True), link=Link.DOWN
#     )
#     got = edge.check()
#     assert got == ("OK", True), "Error: check got {} exp {}".format(got, ("OK", True))
#     got = edge.check_bi()
#     assert got == (None, False), "Error: check got {} exp {}".format(got, (None, False))
#     got = edge.check_down()
#     assert got == ("OK", True), "Error: check got {} exp {}".format(got, ("OK", True))
#     got = edge.check_up()
#     assert got == (None, False), "Error: check got {} exp {}".format(got, (None, False))
#     got = edge.check_with_vertex(parent, child)
#     assert got == ("OK", True), "Error: check got {} exp {}".format(got, ("OK", True))
#     got = edge.check_with_vertex(child, parent)
#     assert got == (None, False), "Error: check got {} exp {}".format(got, (None, False))

#     edge: Edge = Edge("edge", parent, child, lambda p, c, l: ("OK", True), link=Link.UP)
#     got = edge.check()
#     assert got == (None, False), "Error: check got {} exp {}".format(got, (None, False))
#     got = edge.check_bi()
#     assert got == (None, False), "Error: check got {} exp {}".format(got, (None, False))
#     got = edge.check_down()
#     assert got == (None, False), "Error: check got {} exp {}".format(got, (None, False))
#     got = edge.check_up()
#     assert got == ("OK", True), "Error: check got {} exp {}".format(got, ("OK", True))
#     got = edge.check_with_vertex(parent, child)
#     assert got == (None, False), "Error: check got {} exp {}".format(got, (None, False))
#     got = edge.check_with_vertex(child, parent)
#     assert got == ("OK", True), "Error: check got {} exp {}".format(got, ("OK", True))

#     edge: Edge = Edge(
#         "edge", parent, child, lambda p, c, l: ("OK", True), link=Link.NONE
#     )
#     got = edge.check()
#     assert got == (None, False), "Error: check got {} exp {}".format(got, (None, False))
#     got = edge.check_bi()
#     assert got == (None, False), "Error: check got {} exp {}".format(got, (None, False))
#     got = edge.check_down()
#     assert got == (None, False), "Error: check got {} exp {}".format(got, (None, False))
#     got = edge.check_up()
#     assert got == (None, False), "Error: check got {} exp {}".format(got, (None, False))
#     got = edge.check_with_vertex(parent, child)
#     assert got == (None, False), "Error: check got {} exp {}".format(got, (None, False))
#     got = edge.check_with_vertex(child, parent)
#     assert got == (None, False), "Error: check got {} exp {}".format(got, (None, False))


def test_new_path():
    label = "path/0"
    path = Path(label)
    assert path.label == label, "Error: path: label got {} exp {}".format(
        path.label, label
    )
    assert path.edges == [], "Error: path: edges got {} exp {}".format(path.edges, [])
    assert path.sequential, "Error: path: sequential is False"

    label = "path/1"
    path = Path(label, [Edge("", None, None)])
    assert path.label == label, "Error: path: label got {} exp {}".format(
        path.label, label
    )
    got = len(path.edges)
    assert got == 1, "Error: path: len got {} exp {}".format(got, 1)
    assert path.sequential, "Error: path: sequential is False"

    label = "path/2"
    path = Path(label, sequential=False)
    assert path.label == label, "Error: path: label got {} exp {}".format(
        path.label, label
    )
    assert path.edges == [], "Error: path: edges got {} exp {}".format(path.edges, [])
    assert not path.sequential, "Error: path: sequential is True"

    label = "path/3"
    path = Path(label, [Edge("", None, None)], sequential=False)
    assert path.label == label, "Error: path: label got {} exp {}".format(
        path.label, label
    )
    got = len(path.edges)
    assert got == 1, "Error: path: len got {} exp {}".format(got, 1)
    assert not path.sequential, "Error: path: sequential is True"

    v1: Vertex = Vertex("v/1")
    v2: Vertex = Vertex("v/2")
    v3: Vertex = Vertex("v/3")
    path = Path("path/4", [Edge("", v1, v2), Edge("", v2, v3)])
    got = len(path.edges)
    assert got == 2, "Error: path: len got {} exp {}".format(got, 2)
    assert path.sequential, "Error: path: sequential is False"

    try:
        path = Path("path/4", [Edge("", v1, v2), Edge("", v3, v2)])
    except Exception:
        pass
    else:
        assert False, "Error: path: wrong edge sequence"

    path = Path("path/4", [Edge("", v1, v2), Edge("", v3, v2)], sequential=False)
    got = len(path.edges)
    assert got == 2, "Error: path: len got {} exp {}".format(got, 2)
    assert not path.sequential, "Error: path: sequential is True"


def test_path_add():
    path = Path("path/0")
    assert path.edges == [], "Error: add path: edges not empty {}".format(path.edges)
    v1: Vertex = Vertex("v/1")
    v2: Vertex = Vertex("v/2")
    v3: Vertex = Vertex("v/3")
    assert path.add(Edge("", v1, v2)), "Error: add path: failed"
    got = len(path.edges)
    assert got == 1, "Error: add path: len got {} exp {}".format(got, 1)
    assert path.add(Edge("", v2, v3)), "Error: add path: failed"
    got = len(path.edges)
    assert got == 2, "Error: add path: len got {} exp {}".format(got, 2)
    assert not path.add(Edge("", v2, v3)), "Error: add path: failed"

    path = Path("path/1", sequential=False)
    assert path.add(Edge("", v1, v2)), "Error: add path: failed"
    assert path.add(Edge("", v1, v2)), "Error: add path: failed"


if __name__ == "__main__":
    parent: Vertex = Vertex("vertex/0")
    child: Vertex = Vertex("vertex/1")
    gchild: Vertex = Vertex("vertex/2")
    print("create vertices: {}, {}, {}".format(parent, child, gchild))

    # def _weight(p: Vertex, c: Vertex, link: Link) -> [Any, bool]:
    #     if link == Link.DOWN:
    #         return "link down", True
    #     elif link == Link.UP:
    #         return "link up", True
    #     elif link == Link.BI:
    #         return "link bi", True
    #     else:
    #         return "not link", True

    edge: Edge = Edge("edge", parent, child)
    print("create edge: {}".format(edge))
    # print("check down result: {}".format(edge.check_down()))
    # print("check up result: {}".format(edge.check_up()))
    print("{}".format(edge.to_mermaid()))
    path: Path = Path("path/0", [edge])
    edge: Edge = Edge("edge", child, gchild, None)
    path.add(edge)
    print("create path: {}".format(path))
