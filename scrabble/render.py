from __future__ import annotations

from .models import Board


def render_board(board: Board) -> str:
    """Render a Board to a 15-line string.

    Each cell is rendered as '.' when empty and as the tile letter when present.
    Cells are separated by single spaces.
    """

    lines: list[str] = []
    for row in board.grid:
        rendered_row = [cell.letter if cell is not None else "." for cell in row]
        lines.append(" ".join(rendered_row))
    return "\n".join(lines)
