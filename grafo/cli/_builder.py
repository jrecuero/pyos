from typing import List
import os
from ._decorator import loader
from ._node import Node, HookNode
from ._content import CommandContent, StrContent, EndContent
from ._handler import Handler
from ._builtins import _exit, _help
from grafo.cli.parser import Parser, Syntax, Token
from grafo.cli.parser.lex import CliLexer

END_ID = "END"


class Hooker(object):
    __slots__ = ["handler", "hook_next"]

    def __init__(self, handler: Handler, parent_node: Node):
        self.handler: Handler = handler
        self.hook_next: Node = parent_node

    @property
    def type(self):
        return "chain"

    @property
    def next(self):
        return self.hook_next

    @next.setter
    def next(self, next_node):
        self.hook_next = next_node

    @property
    def start(self):
        return self.next

    @property
    def end(self):
        return self.next

    def add_next(self, next_node: Node):
        self.handler.add_node(self.hook_next, next_node)
        self.hook_next = next_node

    def add_to_top(self, next_node: Node):
        raise Exception("Invalid method")

    def add_skip(self):
        raise Exception("Invalid method")

    def add_loop(self):
        raise Exception("Invalid method")

    def terminate(self) -> Node:
        return self.hook_next


class SegmentHooker(Hooker):
    __slots = ["hook_start", "hook_end", "__hooked_end"]

    def __init__(self, handler: Handler, parent_node: Node):
        super(SegmentHooker, self).__init__(handler, parent_node)
        self.hook_start: Node = HookNode("Hook-Start")
        self.hook_next: Node = self.hook_start
        self.hook_end: Node = HookNode("Hook-End")
        self.handler.add_node(parent_node, self.hook_start)
        self.__hooked_end: bool = False

    @property
    def type(self):
        return "segment"

    @property
    def start(self):
        return self.hook_start

    @property
    def end(self):
        return self.hook_end

    def add_next(self, next_node: Node):
        self.handler.add_node(self.hook_next, next_node)
        self.hook_next = next_node

    def reset_next(self):
        self.handler.add_node(self.hook_next, self.hook_end)
        self.hook_next = self.hook_start

    def add_to_top(self, next_node: Node):
        self.handler.add_node(self.hook_next, self.hook_end)
        self.handler.add_node(self.hook_start, next_node)
        self.hook_next = next_node
        self.__hooked_end = True

    def add_skip(self):
        self.handler.add_node(self.hook_start, self.hook_end)
        if not self.__hooked_end:
            self.handler.add_node(self.hook_next, self.hook_end)
        self.__hooked_end = True

    def add_loop(self):
        self.handler.add_node(self.hook_next, self.hook_end)
        self.handler.add_node(self.hook_end, self.hook_start)
        self.__hooked_end = True

    def terminate(self) -> Node:
        if not self.__hooked_end:
            self.handler.add_node(self.hook_next, self.hook_end)
        self.hook_next = self.hook_end
        return self.hook_end


class Builder(object):
    __slots__ = ["lexer", "parser", "handler", "__modes"]

    def __init__(self):
        self.lexer: CliLexer = CliLexer()
        self.parser: Parser = Parser(self.lexer)
        self.handler = Handler()
        self.__modes: List[Node] = []

    def reset(self):
        self.lexer: CliLexer = CliLexer()
        self.parser: Parser = Parser(self.lexer)
        self.handler = Handler()

    def parse(self, line: str) -> Syntax:
        self.parser.set_line(line)
        result, error = self.parser.parse()
        if error is None:
            # print(result.command, result.arguments, result.tokens)
            return result
        print(error)
        return None

    def build(self, line: str, parent: Node = None) -> Node:
        syntax: Syntax = self.parse(line)
        command_node = Node(syntax.command, content=CommandContent(syntax.command))
        active_hooker: Hooker = Hooker(self.handler, parent)
        hookers: List[Hooker] = []
        active_hooker.add_next(command_node)
        closer: List[bool] = []
        # import pdb

        # pdb.set_trace()
        for index, token in enumerate(syntax.tokens):
            if token == Token.IDENT:
                if closer and closer[-1]:
                    closer.pop()
                    hookers[-1].next = active_hooker.terminate()
                    active_hooker = hookers.pop()
                arg_name: str = syntax.arguments[index]
                new_node = Node(arg_name, content=StrContent(arg_name))
                active_hooker.add_next(new_node)
            elif CliLexer.is_opener(token):
                hookers.append(active_hooker)
                active_hooker = SegmentHooker(self.handler, active_hooker.next)
                closer.append(False)
            elif CliLexer.is_closer(token):
                closer[-1] = True
            elif token == CliLexer.PIPE:
                active_hooker.reset_next()
            elif token == CliLexer.QUESTION:
                closer.pop()
                active_hooker.add_skip()
                hookers[-1].next = active_hooker.terminate()
                active_hooker = hookers.pop()
            elif token == CliLexer.ASTERISK:
                closer.pop()
                active_hooker.add_loop()
                active_hooker.add_skip()
                hookers[-1].next = active_hooker.terminate()
                active_hooker = hookers.pop()
            elif token == CliLexer.PLUS:
                closer.pop()
                active_hooker.add_loop()
                hookers[-1].next = active_hooker.terminate()
                active_hooker = hookers.pop()
        if closer and closer[-1]:
            closer.pop()
            hookers[-1].next = active_hooker.terminate()
            active_hooker = hookers.pop()
        end_node = active_hooker.terminate()
        self.handler.add_node(end_node, Node(END_ID, content=EndContent()), first=True)
        # print(self.handler.grafo.to_mermaid())
        return command_node, end_node

    def create_grafo(self, path):
        subdir = path.split(os.sep)[-1]
        _mapa = loader(path, subdir)

        parents = {}
        for map_cmd in [c for c in _mapa.commands if not c.builtin]:
            if map_cmd.parent is None:
                map_cmd.node, end_node = self.build(map_cmd.cline)
            else:
                map_cmd.node, end_node = self.build(
                    map_cmd.cline, parent=parents[map_cmd.parent]
                )
            if map_cmd.node.content.is_command():
                map_cmd.node.content.set_mode(map_cmd.is_mode)
                map_cmd.node.content.call = map_cmd.call
                parents[map_cmd.name] = end_node
            if map_cmd.node.content.is_mode():
                self.__modes.append(end_node)
        for map_cmd in [c for c in _mapa.commands if c.builtin]:
            for mode in [None] + self.__modes:
                map_cmd.node, _ = self.build(map_cmd.cline, parent=mode)
                map_cmd.node.content.builtin = True
                map_cmd.node.content.call = map_cmd.call

        return _mapa


if __name__ == "__main__":
    # TODO: Avoid vim:editor error messages.
    print(_exit, _help)

    b = Builder()
    # b.parse("login hostname [user username | id ider] password")
    # b.build("login hostname [user username | id ider] password")

    # b.build("login hostname username password")
    # b.reset()
    # b.build("login hostname [username password]?")
    # b.reset()
    # b.build("login hostname [username password]*")
    # b.reset()
    # b.build("login hostname [username password]+")
    # b.reset()
    # b.build("login hostname [username | password]")

    next_node = b.build("config")
    b.build("login hostname username password", parent=next_node)
