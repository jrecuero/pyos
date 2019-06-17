from grafo.cli import Handler, Node
from grafo.cli import EndContent, StrContent, IntContent, KeywordContent, CommandContent


def match(pattern: str):
    match, index, path = h.match(pattern)
    print(pattern)
    print("{:5} {} [".format(str(match), index), end=" ")
    for p in path:
        print(p.label, end=" ")
    print("]")
    for commands in h.context.commands:
        for c, t in commands:
            print(c.label, t, end=" ")
        print()
    print("-------")
    print()


def run_config(**kwargs):
    print("command config ...")


def run_name(**kwargs):
    # print("command 'name' callback with: {}".format(kwargs))
    print("your name is {}".format(" ".join(kwargs["name_str"])))


def create_config_command(h: Handler) -> Node:
    node = Node("CONFIG", content=CommandContent("config", command=run_config))
    h.add_node(None, node)
    h.add_node(node, Node("END", content=EndContent()))
    return node


def create_name_command(h: Handler, parent: Node) -> Node:
    node_name = Node("NAME", content=CommandContent("name", command=run_name))
    node_fname = Node("FNAME", content=KeywordContent("fname"))
    node_lname = Node("LNAME", content=KeywordContent("lname"))
    node_str = Node("STR", content=StrContent("name_str"))
    h.add_node(parent, node_name)
    h.add_node(node_name, node_fname)
    h.add_node(node_fname, node_lname)
    h.add_node(node_lname, node_str)
    h.add_node(node_str, node_str, loop=True)
    h.add_node(node_str, Node("END", content=EndContent()))
    return node_str


def create_age_command(h: Handler, parent: Node) -> Node:
    node_age = Node("AGE", content=CommandContent("age"))
    node_int = Node("INT", content=IntContent("age_int"))
    h.add_node(parent, node_age)
    h.add_node(node_age, node_int)
    h.add_node(node_int, Node("END", content=EndContent()))
    return node_int


def create_status_command(h: Handler, parent: Node) -> Node:
    node_status = Node("STATUS", content=CommandContent("status"))
    node_str = Node("STR", content=StrContent("status_str"))
    h.add_node(parent, node_status)
    h.add_node(node_status, node_str)
    h.add_node(node_str, Node("END", content=EndContent()))
    return node_str


if __name__ == "__main__":
    h = Handler()
    node_config = create_config_command(h)
    create_name_command(h, node_config)
    create_age_command(h, node_config)
    create_status_command(h, node_config)

    print(h.grafo.to_mermaid())
    # match("config name fname lname")
    # match("config lname fname")
    # match("config name fname lname jose")
    # match("config name fname lname jose carlos recuero arias")
    # match("config age 50")
    # match("config age one")
    # match("config status married")
    h.run("config")
    h.run("config name fname lname jose carlos recuero arias")
