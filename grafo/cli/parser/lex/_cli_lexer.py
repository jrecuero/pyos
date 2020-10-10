from .._token import Token
from .._parser import Syntax


class Lexer(object):
    # OPENBRACKET token [. #3
    OPENBRACKET = Token.CUSTOM
    # CLOSEBRACKET token ]. #4
    CLOSEBRACKET = Token.CUSTOM + 1
    # PIPE token |. #5
    PIPE = Token.CUSTOM + 2
    # ASTERISK token *. #6
    ASTERISK = Token.CUSTOM + 3
    # PLUS token +. #7
    PLUS = Token.CUSTOM + 4
    # QUESTION mark token ?. #8
    QUESTION = Token.CUSTOM + 5
    # ADMIRATION mark token !. #9
    ADMIRATION = Token.CUSTOM + 6
    # AT token @. #10
    AT = Token.CUSTOM + 7
    # OPENMARK token <. #11
    OPENMARK = Token.CUSTOM + 8
    # CLOSEMARK token >. #12
    CLOSEMARK = Token.CUSTOM + 9
    # OPENCURLY token {. #13
    OPENCURLY = Token.CUSTOM + 10
    # CLOSECURLY token }. #14
    CLOSECURLY = Token.CUSTOM + 11

    LOGIC_MAP = {
        OPENBRACKET: {"opener": True, "closer": False, "segment": 1},
        CLOSEBRACKET: {"opener": False, "closer": True, "segment": 1},
        PIPE: {"opener": False, "closer": False},
        ASTERISK: {"opener": False, "closer": False},
        PLUS: {"opener": False, "closer": False},
        QUESTION: {"opener": False, "closer": False},
        ADMIRATION: {"opener": False, "closer": False},
        AT: {"opener": False, "closer": False},
        OPENMARK: {"opener": True, "closer": False, "segment": 2},
        CLOSEMARK: {"opener": False, "closer": True, "segment": 2},
        OPENCURLY: {"opener": True, "closer": False, "segment": 3},
        CLOSECURLY: {"opener": False, "closer": True, "segment": 3},
    }

    __slots__ = ["syntax", "_char_map"]

    def __init__(self):
        self.syntax: Syntax = None
        self._char_map = {
            "[": Lexer.OPENBRACKET,
            "]": Lexer.CLOSEBRACKET,
            "|": Lexer.PIPE,
            "*": Lexer.ASTERISK,
            "+": Lexer.PLUS,
            "?": Lexer.QUESTION,
            "!": Lexer.ADMIRATION,
            "@": Lexer.AT,
            "<": Lexer.OPENMARK,
            ">": Lexer.CLOSEMARK,
            "{": Lexer.OPENCURLY,
            "}": Lexer.CLOSECURLY,
        }

    @staticmethod
    def is_opener(token: int) -> bool:
        token_map = Lexer.LOGIC_MAP.get(token, None)
        return token_map and token_map["opener"]

    @staticmethod
    def open_segment(token: int) -> bool:
        token_map = Lexer.LOGIC_MAP.get(token, None)
        if token_map and token_map["opener"]:
            return token_map["segment"]
        return 0

    @staticmethod
    def is_closer(token: int) -> bool:
        token_map = Lexer.LOGIC_MAP.get(token, None)
        return token_map and token_map["closer"]

    @staticmethod
    def close_segment(token: int) -> bool:
        token_map = Lexer.LOGIC_MAP.get(token, None)
        if token_map and token_map["closer"]:
            return token_map["segment"]
        return 0

    def new_syntax(self):
        self.syntax = Syntax()

    def parse(self, index, token, lit):
        if index == 1:
            assert token == Token.IDENT, "token:{} is not IDENT:{}".format(
                token, Token.IDENT
            )
            self.syntax.command = lit
        else:
            self.syntax.arguments.append(lit)
            self.syntax.tokens.append(token)
        return

    def result(self):
        return self.syntax

    def get_char_map(self):
        return self._char_map

    def get_ident_chars(self):
        return ["_", "-"]

    def is_ident_char(self, ch, scanner):
        return (
            scanner.is_letter(ch)
            or scanner.is_digit(ch)
            or ch in self.get_ident_chars()
        )

    def is_ident_prefix_char(self, ch, scanner):
        return scanner.is_letter(ch)
