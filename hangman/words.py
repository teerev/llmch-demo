from __future__ import annotations

import random
from typing import Optional

# Fixed word list used by the game.
WORDS = [
    "python",
    "hangman",
    "terminal",
    "game",
    "testing",
    "random",
]


def choose_word(rng: Optional[random.Random] = None) -> str:
    """Choose a word from WORDS.

    If an RNG is provided, it is used for deterministic selection in tests.
    """
    chooser = rng.choice if rng is not None else random.choice
    return chooser(WORDS)
