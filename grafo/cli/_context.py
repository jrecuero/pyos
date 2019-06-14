from typing import List
from ._node import Node
from ._content import Kontent


class Context(object):
    def __init__(self):
        self.commands: List = []
        self.last_command: List = []

    def add(self, node: Node, token: str):
        if len(self.last_command):
            if node.content.klass in [Kontent.COMMAND, Kontent.MODE]:
                self.commands.append(self.last_command)
                self.last_command = []
        else:
            if node.content.klass not in [Kontent.COMMAND, Kontent.MODE]:
                assert "Expectec COMMAND/MODE: {}".format(node.label)
        self.last_command.append((node, token))
        return node

    def end(self):
        self.commands.append(self.last_command)

    def last_command_args(self):
        cargs = {}
        for index in range(1, len(self.last_command)):
            node, token = self.last_command[index]
            if node.content.klass == Kontent.END:
                continue
            name = node.content.name
            if name in cargs:
                if not isinstance(cargs[name], list):
                    cargs[name] = [cargs[name]]
                cargs[name].append(token)
            else:
                cargs.update({node.content.name: token})
        return cargs
