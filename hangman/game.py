from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GameState:
    word: str
    guessed: frozenset[str]
    remaining: int


def new_game(word: str, max_attempts: int = 6) -> GameState:
    """Create a new game state.

    Rules:
      - word is lowercased
      - word must be non-empty and alphabetic
      - max_attempts must be > 0
    """
    if not isinstance(word, str):
        raise TypeError("word must be a string")

    w = word.strip().lower()
    if not w or not w.isalpha():
        raise ValueError("word must be non-empty and alphabetic")

    if not isinstance(max_attempts, int):
        raise TypeError("max_attempts must be an int")
    if max_attempts <= 0:
        raise ValueError("max_attempts must be > 0")

    return GameState(word=w, guessed=frozenset(), remaining=max_attempts)


def guess(state: GameState, letter: str) -> GameState:
    """Apply a single-letter guess.

    Rules:
      - letter must be a single alphabetic character
      - letter is lowercased
      - if already guessed, return state unchanged
      - otherwise add to guessed and decrement remaining only if not in word
    """
    if not isinstance(letter, str):
        raise TypeError("letter must be a string")

    l = letter.strip().lower()
    if len(l) != 1 or not l.isalpha():
        raise ValueError("letter must be a single alphabetic character")

    if l in state.guessed:
        return state

    new_guessed = frozenset(set(state.guessed) | {l})
    new_remaining = state.remaining - (0 if l in state.word else 1)
    return GameState(word=state.word, guessed=new_guessed, remaining=new_remaining)


def display(state: GameState) -> str:
    """Return the display string with revealed letters and '_' for unknowns.

    Output format: characters separated by single spaces.
    """
    parts = [(ch if ch in state.guessed else "_") for ch in state.word]
    return " ".join(parts)


def is_won(state: GameState) -> bool:
    """Return True when all unique letters in the word have been guessed."""
    return set(state.word).issubset(state.guessed)
