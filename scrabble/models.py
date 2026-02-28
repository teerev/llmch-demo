from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Tile:
    letter: str
    points: int


@dataclass
class Board:
    size: int = 15
    grid: list[list[Tile | None]] = field(
        default_factory=lambda: [[None for _ in range(15)] for _ in range(15)]
    )


@dataclass
class GameState:
    board: Board
    rack: list[Tile]
