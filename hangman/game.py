from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GameState:
    word: str
    guessed: frozenset[str]
    wrong_guesses: int
    max_wrong: int


def new_game(word: str, max_wrong: int = 6) -> GameState:
    """Create a new game state.

    The word is normalized to lowercase.
    """
    return GameState(word=word.lower(), guessed=frozenset(), wrong_guesses=0, max_wrong=max_wrong)


def guess_letter(state: GameState, letter: str) -> GameState:
    """Return a new state after guessing a single letter.

    Rules:
    - letter must be length 1, else ValueError
    - letter is lowercased
    - if already guessed, return state unchanged
    - if letter in word, add to guessed
    - else increment wrong_guesses
    """
    if len(letter) != 1:
        raise ValueError("letter must be a single character")

    ltr = letter.lower()

    if ltr in state.guessed:
        return state

    new_guessed = state.guessed | frozenset([ltr])

    if ltr in state.word:
        return GameState(
            word=state.word,
            guessed=new_guessed,
            wrong_guesses=state.wrong_guesses,
            max_wrong=state.max_wrong,
        )

    return GameState(
        word=state.word,
        guessed=new_guessed,
        wrong_guesses=state.wrong_guesses + 1,
        max_wrong=state.max_wrong,
    )


def is_won(state: GameState) -> bool:
    """A game is won when all unique letters in the word have been guessed."""
    return set(state.word) <= set(state.guessed)


def is_lost(state: GameState) -> bool:
    """A game is lost when wrong_guesses reaches or exceeds max_wrong."""
    return state.wrong_guesses >= state.max_wrong


def render_progress(state: GameState) -> str:
    """Render the word progress as letters and underscores separated by spaces."""
    parts = [(ch if ch in state.guessed else "_") for ch in state.word]
    return " ".join(parts)
