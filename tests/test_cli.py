from __future__ import annotations

from scrabble.cli import build_parser


def test_parser_defaults():
    parser = build_parser()
    args = parser.parse_args([])
    assert args.players == "Player1,Player2"
    assert args.seed is None
    assert args.max_turns is None


def test_parser_custom_values():
    parser = build_parser()
    args = parser.parse_args(["--players", "Alice,Bob", "--seed", "123", "--max-turns", "10"])
    assert args.players == "Alice,Bob"
    assert args.seed == 123
    assert args.max_turns == 10
