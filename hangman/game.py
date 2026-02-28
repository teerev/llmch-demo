from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GameState:
    secret_word: str
    guessed_letters: set[str]
    remaining_attempts: int


def new_game(secret_word: str, max_attempts: int) -> GameState:
    return GameState(
        secret_word=secret_word,
        guessed_letters=set(),
        remaining_attempts=max_attempts,
    )


def guess(state: GameState, letter: str) -> GameState:
    # Normalize input
    letter = (letter or "").lower()

    # If empty input, treat as no-op
    if not letter:
        return state

    # Only consider the first character as the guessed letter
    letter = letter[0]

    # If already guessed, no change
    if letter in state.guessed_letters:
        return state

    new_guessed = set(state.guessed_letters)
    new_guessed.add(letter)

    if letter in state.secret_word.lower():
        return GameState(
            secret_word=state.secret_word,
            guessed_letters=new_guessed,
            remaining_attempts=state.remaining_attempts,
        )

    return GameState(
        secret_word=state.secret_word,
        guessed_letters=new_guessed,
        remaining_attempts=state.remaining_attempts - 1,
    )


def current_mask(state: GameState) -> str:
    secret = state.secret_word
    guessed = {c.lower() for c in state.guessed_letters}

    masked_chars: list[str] = []
    for ch in secret:
        if ch.lower() in guessed:
            masked_chars.append(ch)
        else:
            masked_chars.append("_")
    return "".join(masked_chars)


def is_won(state: GameState) -> bool:
    secret_letters = {c.lower() for c in state.secret_word if c.isalpha()}
    guessed = {c.lower() for c in state.guessed_letters}
    return secret_letters.issubset(guessed)


def is_lost(state: GameState) -> bool:
    return state.remaining_attempts <= 0
