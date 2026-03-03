from __future__ import annotations

from dataclasses import dataclass
from typing import FrozenSet


@dataclass(frozen=True)
class GameState:
    secret_word: str
    guessed_letters: FrozenSet[str]
    incorrect_guesses: int
    max_incorrect: int


def new_game(secret_word: str, max_incorrect: int = 6) -> GameState:
    """Create a new game state.

    The model is deterministic and immutable; all updates return a new GameState.
    """
    if not isinstance(secret_word, str) or not secret_word:
        raise ValueError("secret_word must be a non-empty string")
    if not isinstance(max_incorrect, int) or max_incorrect < 0:
        raise ValueError("max_incorrect must be a non-negative integer")

    return GameState(
        secret_word=secret_word,
        guessed_letters=frozenset(),
        incorrect_guesses=0,
        max_incorrect=max_incorrect,
    )


def guess(state: GameState, letter: str) -> GameState:
    """Return a new state after guessing a letter.

    Rules:
    - Only single alphabetic characters are accepted.
    - Guessing a previously guessed letter is a no-op.
    - Incorrect guesses increment incorrect_guesses.
    - If the game is already won or lost, guessing is a no-op.
    """
    if not isinstance(state, GameState):
        raise TypeError("state must be a GameState")

    if is_won(state) or is_lost(state):
        return state

    if not isinstance(letter, str):
        raise ValueError("letter must be a string")

    letter = letter.strip().lower()
    if len(letter) != 1 or not letter.isalpha():
        raise ValueError("letter must be a single alphabetic character")

    if letter in state.guessed_letters:
        return state

    new_guessed = set(state.guessed_letters)
    new_guessed.add(letter)

    incorrect = state.incorrect_guesses
    if letter not in state.secret_word.lower():
        incorrect += 1

    return GameState(
        secret_word=state.secret_word,
        guessed_letters=frozenset(new_guessed),
        incorrect_guesses=incorrect,
        max_incorrect=state.max_incorrect,
    )


def display_word(state: GameState) -> str:
    """Return the secret word with unguessed letters replaced by '_' characters."""
    if not isinstance(state, GameState):
        raise TypeError("state must be a GameState")

    guessed = {c.lower() for c in state.guessed_letters}
    out = []
    for ch in state.secret_word:
        if ch.isalpha() and ch.lower() not in guessed:
            out.append("_")
        else:
            out.append(ch)
    return "".join(out)


def is_won(state: GameState) -> bool:
    """A game is won when all alphabetic letters in the secret word are guessed."""
    if not isinstance(state, GameState):
        raise TypeError("state must be a GameState")

    guessed = {c.lower() for c in state.guessed_letters}
    for ch in state.secret_word:
        if ch.isalpha() and ch.lower() not in guessed:
            return False
    return True


def is_lost(state: GameState) -> bool:
    """A game is lost when incorrect_guesses reaches max_incorrect."""
    if not isinstance(state, GameState):
        raise TypeError("state must be a GameState")

    return state.incorrect_guesses >= state.max_incorrect
