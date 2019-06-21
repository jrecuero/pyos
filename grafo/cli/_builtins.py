from ._decorator import builtin, command


@builtin
@command("exit [all]?")
def _exit(**kwargs):
    h = kwargs.get("__handler__", None)
    if kwargs.get("all", False) or h.pop_mode() is None:
        exit(0)
    return None


@builtin
@command("help")
def _help(**kwargs):
    h = kwargs.get("__handler__", None)
    if h.context.modes:
        children = h.context.active_mode_node().children
    else:
        children = h.grafo.root.children
    for m in children:
        print(str(m))
