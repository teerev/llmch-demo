from __future__ import annotations

import random
from typing import Any

from quadrl.config import TrainConfig


class RandomPolicy:
    def __init__(self, config: TrainConfig):
        self._rng = random.Random(config.seed)

    def act(self, obs: dict) -> float:
        _ = obs  # unused
        return self._rng.uniform(-1.0, 1.0)
