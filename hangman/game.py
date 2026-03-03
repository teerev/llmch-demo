from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class GameState:
    secret_word: str
    guessed_letters: set[str] = field(default_factory=set)
    max_attempts: int = 0
    wrong_attempts: int = 0


def new_game(secret_word: str, max_attempts: int) -> GameState:
    """Create a new game state.

    - secret_word is stored lowercased
    - guessed_letters starts empty
    - wrong_attempts starts at 0
    """
    return GameState(
        secret_word=(secret_word or "").lower(),
        guessed_letters=set(),
        max_attempts=max_attempts,
        wrong_attempts=0,
    )


def guess_letter(state: GameState, letter: str) -> GameState:
    """Apply a letter guess to the given state.

    Behavior is deterministic and mutates the provided state in-place.

    Rules:
    - letter is lowercased
    - if len(letter) != 1: return state unchanged
    - if letter already guessed: return state unchanged
    - otherwise add to guessed_letters
    - if letter not in secret_word: increment wrong_attempts
    - return the same state object
    """
    if not isinstance(letter, str):
        return state

    letter = letter.lower()
    if len(letter) != 1:
        return state

    if letter in state.guessed_letters:
        return state

    state.guessed_letters.add(letter)
    if letter not in state.secret_word:
        state.wrong_attempts += 1

    return state


def masked_word(state: GameState) -> str:
    """Return the secret word with unguessed letters masked as '_' (no spaces)."""
    return "".join(ch if ch in state.guessed_letters else "_" for ch in state.secret_word)


def is_won(state: GameState) -> bool:
    """A game is won when every character in secret_word has been guessed."""
    return all(ch in state.guessed_letters for ch in state.secret_word)


def is_lost(state: GameState) -> bool:
    """A game is lost when wrong_attempts >= max_attempts."""
    return state.wrong_attempts >= state.max_attempts
