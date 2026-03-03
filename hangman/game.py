"""Core hangman game logic.

This module is intentionally deterministic and free of any I/O.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GameState:
    word: str
    guessed: set[str]
    wrong_guesses: int
    max_attempts: int


def new_game(word: str, max_attempts: int) -> GameState:
    """Create a new game state.

    Args:
        word: The target word to guess.
        max_attempts: Maximum number of wrong guesses allowed.

    Returns:
        A new GameState.
    """
    if not isinstance(word, str):
        raise TypeError("word must be a str")
    if not isinstance(max_attempts, int):
        raise TypeError("max_attempts must be an int")
    if max_attempts < 0:
        raise ValueError("max_attempts must be >= 0")

    return GameState(word=word, guessed=set(), wrong_guesses=0, max_attempts=max_attempts)


def guess(state: GameState, letter: str) -> GameState:
    """Apply a guess to the game state and return a new state.

    Rules:
      - Case-insensitive.
      - If `letter` is not a single alphabetic character, this is a no-op.
      - Re-guessing an already-guessed letter is a no-op.
      - If the letter is not in the word, wrong_guesses increments by 1.

    This function does not prevent guessing after win/loss; callers can decide.
    """
    if not isinstance(letter, str):
        return state

    if len(letter) != 1 or not letter.isalpha():
        return state

    ltr = letter.lower()
    if ltr in state.guessed:
        return state

    new_guessed = set(state.guessed)
    new_guessed.add(ltr)

    in_word = ltr in state.word.lower()
    new_wrong = state.wrong_guesses + (0 if in_word else 1)

    return GameState(
        word=state.word,
        guessed=new_guessed,
        wrong_guesses=new_wrong,
        max_attempts=state.max_attempts,
    )


def is_won(state: GameState) -> bool:
    """Return True if all alphabetic letters in the word have been guessed."""
    word_lower = state.word.lower()
    needed = {ch for ch in word_lower if ch.isalpha()}
    return needed.issubset(state.guessed)


def is_lost(state: GameState) -> bool:
    """Return True if wrong guesses have reached the maximum attempts."""
    return state.wrong_guesses >= state.max_attempts


def progress_string(state: GameState) -> str:
    """Render the word progress using '_' for unguessed alphabetic letters.

    Non-alphabetic characters are shown as-is.
    """
    guessed = state.guessed
    out: list[str] = []
    for ch in state.word:
        if ch.isalpha():
            out.append(ch if ch.lower() in guessed else "_")
        else:
            out.append(ch)
    return "".join(out)
