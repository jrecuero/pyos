from typing import List
from ._node import Node
from ._content import Kontent


class Context(object):
    __slots__ = ["match_commands", "match_last_command", "_modes"]

    def __init__(self):
        self.match_commands: List = []
        self.match_last_command: List = []
        self._modes: List = []

    @property
    def modes(self):
        return self._modes

    def add_node(self, node: Node, token: str):
        if len(self.match_last_command):
            if node.content.klass in [Kontent.COMMAND, Kontent.MODE]:
                self.match_commands.append(self.match_last_command)
                self.match_last_command = []
        else:
            if node.content.klass not in [Kontent.COMMAND, Kontent.MODE]:
                assert "Expected COMMAND/MODE: {}".format(node.label)
        self.match_last_command.append((node, token))
        return node

    def last_command_matched_entry(self):
        return self.match_last_command[0]

    def last_command_matched_node(self):
        return self.match_last_command[0][0]

    def active_mode_node(self):
        if self.modes:
            return self.modes[-1][0][0]
        return None

    def push_mode(self):
        self._modes.append(self.match_last_command[:-1])

    def pop_mode(self):
        if len(self._modes):
            self.match_last_command = self._modes.pop()
            return self.match_last_command
        return None

    def flat_modes(self):
        return [token for mode in self._modes for _, token in mode]

    def new_match(self):
        self.match_commands = []
        self.match_last_command = []

    def end(self):
        self.match_commands.append(self.match_last_command)

    def last_command_matched_args(self):
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
