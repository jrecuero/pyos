from ._decorator import builtin, command
from ._streamer import STREAM


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
    ret_value = [str(m) for m in children]
    STREAM.out("\n".join(ret_value))
    return ret_value
