"""parser module provides all character parsing functionality in order to
parse any lexical language.

version: 2.0
"""

from ._scanner import Scanner
from ._token import Token


class Syntax(object):
    __slots__ = ["command", "arguments", "tokens"]

    def __init__(self, command=None, argos=None, tokens=None):
        self.command = command
        self.arguments = argos if argos else []
        self.tokens = tokens if tokens else []


class Buffer(object):
    __slots__ = ["token", "literal", "size"]

    def __init__(self):
        self.token = None
        self.literal = None
        self.size = 0


class Parser(object):
    __slots__ = ["lexer", "scanner", "buffer"]

    def __init__(self, lexer, line=None):
        self.lexer = lexer
        self.scanner = Scanner(lexer, line)
        self.buffer = Buffer()

    def set_line(self, line):
        self.scanner.set_reader(line)

    def parse(self):
        index = 1
        self.lexer.new_syntax()
        while True:
            tok, lit = self.scan_ignore_white_space()
            if tok == Token.ILLEGAL:
                return None, "found {0}, expected argument\n".format(lit)
            elif tok == Token.EOF:
                break
            self.lexer.parse(index, tok, lit)
            index += 1
        return self.lexer.result(), None

    def scan(self):
        if self.buffer.size:
            self.buffer.size = 0
            return (self.buffer.token, self.buffer.literal)

        self.buffer.token, self.buffer.literal = self.scanner.scan()
        return self.buffer.token, self.buffer.literal

    def scan_ignore_white_space(self):
        tok, lit = self.scan()
        if tok == Token.WS:
            tok, lit = self.scan()
        return tok, lit

    def unscan(self):
        self.buffer.size = 1
