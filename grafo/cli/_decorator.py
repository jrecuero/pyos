from typing import List
from functools import wraps
import os
from grafo.cli import Node


class Mapa(object):
    class Command(object):
        __slots__ = [
            "name",
            "cline",
            "parent",
            "call",
            "rcall",
            "node",
            "is_mode",
            "builtin",
        ]

        def __init__(self, name: str, cline: str, parent: str, call, is_mode: bool):
            self.name: str = name
            self.cline: str = cline
            self.parent: str = parent
            self.call = call
            self.rcall = None
            self.node: Node = None
            self.is_mode: bool = is_mode
            self.builtin: bool = False

        def __str__(self):
            return "[{}.{}] {} Node:{} <{}> {}".format(
                self.parent,
                self.name,
                self.cline,
                self.node,
                self.call.__name__,
                self.builtin,
            )

    __slots__ = ["name", "commands", "loader_parent"]

    def __init__(self, name: str = None):
        self.name: str = name
        self.commands: List[Mapa.Command] = []
        self.loader_parent: str = None

    def add(self, line: str, func, is_mode=False):
        cname = line.split()[0]
        self.commands.append(
            Mapa.Command(cname, line, self.loader_parent, func, is_mode)
        )

    def get(self, cname: str) -> "Mapa.Command":
        for c in self.commands:
            if c.name == cname:
                return c
        return None

    def get_call(self, cname: str):
        command = self.get(cname)
        if command:
            return command.call
        return None


__mapa = Mapa()


def builtin(func):
    last = __mapa.commands[-1]
    last.builtin = True

    @wraps(func)
    def _builtin_wrapper(**kwargs):
        return func(**kwargs)

    return _builtin_wrapper


def command(line):
    def _command(func):
        __mapa.add(line, func)

        @wraps(func)
        def _wrapper(**kwargs):
            return func(**kwargs)

        return _wrapper

    return _command


def mode(line):
    def _command(func):
        __mapa.add(line, func, is_mode=True)

        @wraps(func)
        def _wrapper(**kwargs):
            return func(**kwargs)

        return _wrapper

    return _command


def loader(path, baseline=None, top=None):
    __mapa.loader_parent = top
    all_mods = os.listdir(path)
    for mod in [m for m in all_mods if not m.startswith("__") and m.endswith(".py")]:
        module = (
            "{}.{}".format(baseline, mod[:-3]) if baseline else "{}".format(mod[:-3])
        )
        # print("importing {}...".format(module))
        __import__(module, locals(), globals())
    for mod in [m for m in all_mods if not (m.startswith(".") or m.startswith("__"))]:
        module = os.path.join(path, mod)
        if os.path.isdir(module):
            if baseline:
                loader(module, "{}.{}".format(baseline, mod), mod)
            else:
                loader(module, mod, mod)
    return __mapa
