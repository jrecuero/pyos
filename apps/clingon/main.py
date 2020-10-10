from grafo.cli import Handler, Node, HookNode, STREAM
from grafo.cli import EndContent, StrContent, IntContent, KeywordContent, CommandContent


def match(h: Handler, pattern: str):
    match, index, path = h.match(pattern)
    print(pattern)
    print("{:5} {} [".format(str(match), index), end=" ")
    for p in path:
        print(p.label, end=" ")
    print("]")
    print()


def run_config(**kwargs):
    print("command config ...")


def run_name(**kwargs):
    # print("command 'name' callback with: {}".format(kwargs))
    print("your name is {}".format(" ".join(kwargs["name_str"])))


def run_login(**kwargs):
    if kwargs.get("username", None):
        print(
            "login {} with username: {} : {}".format(
                kwargs.get("hostname", None),
                kwargs.get("v_username", None),
                kwargs.get("password", None),
            )
        )
    elif kwargs.get("ider", None):
        print(
            "login {} with ider: {} : {}".format(
                kwargs.get("hostname", None),
                kwargs.get("v_username", None),
                kwargs.get("password", None),
            )
        )
    else:
        print("invalid login")


def create_config_command(h: Handler) -> Node:
    node = Node("CONFIG", content=CommandContent("config", call=run_config))
    h.add_node(None, node)
    h.add_node(node, Node("END", content=EndContent()))
    return node


def create_name_command(h: Handler, parent: Node) -> Node:
    node_name = Node("NAME", content=CommandContent("name", call=run_name))
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


def create_login_command(h: Handler, parent: Node) -> Node:
    node_login = Node("LOGIN", content=CommandContent("login", call=run_login))
    node_hostname = Node("HOSTNAME", content=StrContent("hostname"))
    node_start_hook = HookNode("START-HOOK")
    node_end_hook = HookNode("END-HOOK")
    node_kusername = Node("kUSERNAME", content=KeywordContent("username"))
    node_username = Node("USERNAME", content=StrContent("v_username"))
    node_kider = Node("kIDER", content=KeywordContent("ider"))
    node_ider = Node("IDER", content=StrContent("v_ider"))
    node_password = Node("PASSWORD", content=StrContent("password"))
    h.add_node(parent, node_login)
    h.add_node(node_login, node_hostname)
    h.add_node(node_hostname, node_start_hook)
    h.add_node(node_start_hook, node_kusername)
    h.add_node(node_kusername, node_username)
    h.add_node(node_start_hook, node_kider)
    h.add_node(node_kider, node_ider)
    h.add_node(node_username, node_end_hook)
    h.add_node(node_ider, node_end_hook)
    h.add_node(node_end_hook, node_password)
    h.add_node(node_password, Node("END", content=EndContent()))
    return node_end_hook


if __name__ == "__main__":
    # h = Handler()

    # node_config = create_config_command(h)
    # create_name_command(h, node_config)
    # create_age_command(h, node_config)
    # create_status_command(h, node_config)
    # create_login_command(h, node_config)

    # print(h.grafo.to_mermaid())
    # # match("config name fname lname")
    # # match("config lname fname")
    # # match("config name fname lname jose")
    # # match("config name fname lname jose carlos recuero arias")
    # # match("config age 50")
    # # match("config age one")
    # # match("config status married")
    # h.run("config")
    # h.run("config name fname lname jose carlos recuero arias")
    # # match("config login username jose")
    # h.run("config login localhost username jose 012345")
    # h.run("config login localhost ider 101 67890")

    import os
    from grafo.cli import Builder

    subdir = "commands"
    path = os.path.join(os.path.dirname(__file__), subdir)
    b = Builder()
    MAPA = b.create_grafo(path)

    for c in MAPA.commands:
        print("{}".format(c))

    # config = MAPA.get_call("config")
    # rconfig = config()
    # rconfig()
    # login = MAPA.get_call("login")
    # rlogin = login(hostname="localhost", user="jrecuero")
    # rlogin()

    # print("\n+-----+")
    # # match(b.handler, "config")
    # b.handler.run("config")
    # print(b.handler.context.modes)

    # print("\n+-----+")
    # # match(b.handler, "config login localhost jrecuero")
    # b.handler.run("config login localhost jrecuero")

    # print("\n+-----+")
    # b.handler.run("config set home")
    # print(b.handler.context.modes)
    # print(b.handler.context.flat_modes())
    # # b.handler.run("config set home speed 100")

    # line = "none"
    # while line:
    #     line = input("? ")
    #     b.handler.run(line)

    # print("\n+-----+")
    # # b.handler.run("exit")
    # b.handler.run("config")
    # b.handler.run("exit")
    # b.handler.run("config")
    # b.handler.run("set home")
    # b.handler.run("exit")
    # b.handler.run("config")
    # b.handler.run("set home")
    # b.handler.run("speed 256")
    # b.handler.run("speed 512")
    # b.handler.run("exit")
    # b.handler.run("exit")
    # # print([str(_) for _ in b._Builder__modes])

    line = "none"
    while line:
        line = input("? ")
        result = b.handler.run(line)
        STREAM.out("command {} returned: {}".format(line, result))

    # match(b.handler, "setup localhost")

    print("Running silence")
    STREAM.output = lambda x: x
    result = b.handler.run("help")
    print("silenced command help returned: {}".format(result))
