from grafo.cli import Handler, Node
from grafo.cli import StrContent, IntContent, KeywordContent, CommandContent


def match(pattern: str):
    match, index, path = h.find_path(pattern.split(), 0, [])
    print(pattern)
    print("{:5} {} [".format(str(match), index), end=" ")
    for p in path:
        print(p.label, end=" ")
    print("]\n")


if __name__ == "__main__":
    n1 = Node("CONFIG", content=CommandContent("config"))
    n2 = Node("NAME", content=CommandContent("name"))
    n3 = Node("FNAME", content=KeywordContent("fname"))
    n4 = Node("LNAME", content=KeywordContent("lname"))
    n4str = Node("STR", content=StrContent("str"))
    n5 = Node("AGE", content=CommandContent("age"))
    n5str = Node("INT", content=IntContent(50))
    n6 = Node("STATUS", content=CommandContent("status"))
    n6str = Node("STR", content=StrContent("str"))
    h = Handler()
    h.add_node(None, n1)
    h.add_node(n1, n2)
    h.add_node(n2, n3)
    h.add_node(n3, n4)
    h.add_node(n4, n4str)
    h.add_node(n4str, n4str)
    h.add_node(n1, n5)
    h.add_node(n5, n5str)
    h.add_node(n1, n6)
    h.add_node(n6, n6str)
    print(h.grafo.to_mermaid())
    path = h.grafo.paths_from_v_to_v(n1, n3)
    for p in path:
        print(p.to_mermaid())
    match("config name fname lname")
    match("config lname fname")
    match("config name fname lname str")
    match("config name fname lname jose carlos recuero arias")
    match("config age 50")
    match("config age one")
    match("config status married")
