"""Command-line interface for the scrabble package.

This module provides:
- build_parser(): argparse configuration
- main(argv=None): entry point

The interactive loop is intentionally simple and uses input()/print().
"""

from __future__ import annotations

import argparse
import random
from typing import List, Optional

from .bag import TileBag
from .game import Game
from .player import Player


def build_parser() -> argparse.ArgumentParser:
    """Build and return the CLI argument parser."""

    parser = argparse.ArgumentParser(prog="scrabble", description="Play an interactive Scrabble-like game.")
    parser.add_argument(
        "--players",
        default="Player1,Player2",
        help="Comma-separated player names (default: 'Player1,Player2')",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Optional RNG seed for deterministic tile draws.",
    )
    parser.add_argument(
        "--max-turns",
        type=int,
        default=None,
        help="Optional maximum number of turns before quitting.",
    )
    return parser


def _parse_players(players_arg: str) -> List[str]:
    if not isinstance(players_arg, str):
        raise TypeError("--players must be a string")
    names = [p.strip() for p in players_arg.split(",")]
    names = [n for n in names if n]
    if not names:
        raise ValueError("--players must contain at least one non-empty name")
    return names


def _print_help() -> None:
    print("Commands:")
    print("  PLACE <WORD> <ROW> <COL> <H|V>  - place a word")
    print("  PASS                           - pass your turn")
    print("  QUIT                           - quit the game")
    print("  HELP                           - show this help")


def main(argv: Optional[List[str]] = None) -> int:
    """CLI entry point.

    Starts an interactive loop using input() and print().

    Returns
    -------
    int
        Process exit code.
    """

    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        player_names = _parse_players(args.players)
    except Exception as e:  # argparse-style error
        parser.error(str(e))
        return 2

    if args.max_turns is not None and args.max_turns <= 0:
        parser.error("--max-turns must be a positive integer")
        return 2

    rng = random.Random(args.seed) if args.seed is not None else random.Random()
    bag = TileBag(rng=rng)
    players = [Player(name=n) for n in player_names]
    for p in players:
        p.draw_tiles(bag, 7)

    game = Game(players=players, bag=bag)

    print("Interactive Scrabble")
    print(f"Players: {', '.join(player_names)}")
    _print_help()

    turns = 0
    while True:
        if args.max_turns is not None and turns >= args.max_turns:
            print("Reached maximum turns. Quitting.")
            break

        player = game.current_player
        print(f"\nTurn {turns + 1} - {player.name}")
        print(f"Score: {player.score}")
        print(f"Rack: {' '.join(player.rack)}")

        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nQUIT")
            break

        if not line:
            continue

        cmd, *rest = line.split()
        cmd_u = cmd.upper()

        if cmd_u in {"QUIT", "Q", "EXIT"}:
            print("Quitting.")
            break

        if cmd_u in {"HELP", "H", "?"}:
            _print_help()
            continue

        if cmd_u == "PASS":
            game.next_player()
            turns += 1
            continue

        if cmd_u == "PLACE":
            if len(rest) != 4:
                print("Usage: PLACE <WORD> <ROW> <COL> <H|V>")
                continue
            word, row_s, col_s, direction = rest
            try:
                row = int(row_s)
                col = int(col_s)
                direction_u = direction.upper()
                score = game.apply_move(word, row, col, direction_u)
            except Exception as e:
                print(f"Invalid move: {e}")
                continue

            print(f"Placed '{word.upper()}' for {score} points.")
            turns += 1
            continue

        print("Unknown command. Type HELP for commands.")

    print("\nFinal scores:")
    for p in game.players:
        print(f"  {p.name}: {p.score}")

    return 0
