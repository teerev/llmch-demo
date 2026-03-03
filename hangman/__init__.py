"""Hangman package.

This package exposes the pure game-state logic via :mod:`hangman.game`.
"""

from .game import GameState, display_word, guess_letter, init_game, is_lost, is_won

__all__ = [
    "GameState",
    "init_game",
    "guess_letter",
    "display_word",
    "is_won",
    "is_lost",
]
