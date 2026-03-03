from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class TrainConfig:
    input_height: int = 256
    input_width: int = 256
    hidden_sizes: Tuple[int, ...] = (128,)
    learning_rate: float = 0.01
    epochs: int = 1
    seed: int = 0

    @property
    def input_size(self) -> int:
        return self.input_height * self.input_width
