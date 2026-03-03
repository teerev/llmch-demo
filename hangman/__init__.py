"""Hangman package.

This package is intentionally minimal and side-effect free.
"""

from .game import GameState, apply_guess, display_word, is_lost, is_won, new_game

__all__ = [
    "GameState",
    "new_game",
    "apply_guess",
    "display_word",
    "is_won",
    "is_lost",
]
