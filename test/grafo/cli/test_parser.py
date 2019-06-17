"""test_parser module test parser version 2.0.

version: 2.0
"""

import pytest
from grafo.cli.parser import Parser, Token, Syntax
from grafo.cli.parser.lex import CliLexer


@pytest.fixture
def parser(request):
    lexer = CliLexer()
    return Parser(lexer)


def test_parser_new_parser(parser):
    assert parser.buffer is not None
    assert parser.buffer.token is None
    assert parser.buffer.literal is None
    assert parser.buffer.size == 0


def test_parser_unscan(parser):
    parser.unscan()
    assert parser.buffer.size == 1


@pytest.mark.parametrize(
    ("inputs", "results"),
    [
        ("SELECT table", (Token.IDENT, "SELECT")),
        ("[data]", (CliLexer.OPENBRACKET, "[")),
        ("  table", (Token.WS, "  ")),
    ],
)
def test_parser_scan(parser, inputs, results):
    parser.set_line(inputs)
    got = parser.scan()
    assert got == results


@pytest.mark.parametrize(
    ("inputs", "results"),
    [
        ("SELECT table", (Token.IDENT, "SELECT")),
        ("[data]", (CliLexer.OPENBRACKET, "[")),
        ("  table", (Token.IDENT, "table")),
    ],
)
def test_parser_scan_ignore_white_space(parser, inputs, results):
    parser.set_line(inputs)
    got = parser.scan_ignore_white_space()
    assert got == results


@pytest.mark.parametrize(
    ("inputs", "results"),
    [
        ("SELECT table", Syntax("SELECT", ["table"], [Token.IDENT])),
        (
            "SELECT [table]?",
            Syntax(
                "SELECT",
                ["[", "table", "]", "?"],
                [
                    CliLexer.OPENBRACKET,
                    Token.IDENT,
                    CliLexer.CLOSEBRACKET,
                    CliLexer.QUESTION,
                ],
            ),
        ),
    ],
)
def test_parser_parse(parser, inputs, results):
    parser.set_line(inputs)
    got, error = parser.parse()
    assert got is not None
    assert error is None
    assert got.command == results.command
    assert got.arguments == results.arguments
    assert got.tokens == results.tokens
