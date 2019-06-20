from typing import List
from ._node import Node
from ._content import Kontent


class Context(object):
    def __init__(self):
        self.match_commands: List = []
        self.match_last_command: List = []
        self.modes: List = []

    def add_node(self, node: Node, token: str):
        if len(self.match_last_command):
            if node.content.klass in [Kontent.COMMAND, Kontent.MODE]:
                self.match_commands.append(self.match_last_command)
                self.match_last_command = []
        else:
            if node.content.klass not in [Kontent.COMMAND, Kontent.MODE]:
                assert "Expectec COMMAND/MODE: {}".format(node.label)
        self.match_last_command.append((node, token))
        return node

    def push_mode(self):
        self.modes.append(self.match_last_command[:-1])

    def pop_mode(self):
        return self.modes.pop()

    def flat_modes(self):
        return [token for mode in self.modes for _, token in mode]

    def new_match(self):
        self.match_commands = []
        self.match_last_command = []

    def end(self):
        self.match_commands.append(self.match_last_command)

    def last_command_args(self):
        cargs = {}
        for index in range(1, len(self.match_last_command)):
            node, token = self.match_last_command[index]
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
