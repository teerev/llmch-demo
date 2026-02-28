from __future__ import annotations

import argparse

from .game import new_game
from .render import render_board


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m scrabble",
        description="Render a Scrabble board and rack.",
    )
    parser.parse_args(argv)

    state = new_game()
    print(render_board(state.board))
    rack_letters = " ".join(tile.letter for tile in state.rack)
    print(f"Rack: {rack_letters}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
