"""Hangman package."""

from .game import GameState, guess, is_lost, is_won, new_game, progress_string

__all__ = [
    "GameState",
    "new_game",
    "guess",
    "is_won",
    "is_lost",
    "progress_string",
]
