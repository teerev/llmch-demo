from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GameState:
    """Immutable hangman game state."""

    word: str
    guessed_letters: set[str]
    remaining_attempts: int


def init_game(word: str, max_attempts: int) -> GameState:
    """Initialize a new game.

    The game logic is case-insensitive; the stored word is normalized to lowercase.
    """
    if max_attempts < 0:
        raise ValueError("max_attempts must be >= 0")
    normalized_word = (word or "").lower()
    return GameState(word=normalized_word, guessed_letters=set(), remaining_attempts=max_attempts)


def guess_letter(state: GameState, letter: str) -> GameState:
    """Return a new state after guessing a letter.

    Rules:
    - Normalizes the guess to lowercase.
    - If the letter was already guessed, state is unchanged.
    - If the letter is not in the word, remaining_attempts decreases by 1 (to a minimum of 0).
    - Non-single-character guesses raise ValueError.

    This function is pure: it never mutates the input state.
    """
    if len(letter) != 1:
        raise ValueError("letter must be a single character")

    ltr = letter.lower()

    if ltr in state.guessed_letters:
        return state

    new_guessed = set(state.guessed_letters)
    new_guessed.add(ltr)

    if ltr in state.word:
        return GameState(word=state.word, guessed_letters=new_guessed, remaining_attempts=state.remaining_attempts)

    new_remaining = state.remaining_attempts - 1
    if new_remaining < 0:
        new_remaining = 0
    return GameState(word=state.word, guessed_letters=new_guessed, remaining_attempts=new_remaining)


def display_word(state: GameState) -> str:
    """Return the display string for the current word.

    Shows guessed letters and '_' for unknowns, with no separators.
    """
    guessed = state.guessed_letters
    return "".join(ch if ch in guessed else "_" for ch in state.word)


def is_won(state: GameState) -> bool:
    """Return True if all letters in the word have been guessed."""
    if not state.word:
        return True
    return all(ch in state.guessed_letters for ch in state.word)


def is_lost(state: GameState) -> bool:
    """Return True if no attempts remain and the game is not won."""
    return state.remaining_attempts <= 0 and not is_won(state)
