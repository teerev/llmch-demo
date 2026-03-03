from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GameState:
    word: str
    guessed: frozenset[str]
    remaining_attempts: int
    max_attempts: int


def new_game(word: str, max_attempts: int) -> GameState:
    if not word:
        raise ValueError("word must be non-empty")
    if max_attempts <= 0:
        raise ValueError("max_attempts must be > 0")

    normalized_word = word.lower()
    return GameState(
        word=normalized_word,
        guessed=frozenset(),
        remaining_attempts=max_attempts,
        max_attempts=max_attempts,
    )
