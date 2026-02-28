from __future__ import annotations

import math
import random
from typing import TypeAlias

Dataset: TypeAlias = list[tuple[list[float], int]]


class MLP9:
    """Inference-only MLP for fixed 9x9 (81) float inputs.

    Architecture:
      - Input: 81
      - Hidden: configurable size, sigmoid activation
      - Output: single sigmoid unit

    Weights are deterministically initialized from a provided seed.
    """

    def __init__(self, hidden_size: int = 16, seed: int = 0):
        self.input_size = 81
        self.hidden_size = int(hidden_size)
        if self.hidden_size <= 0:
            raise ValueError("hidden_size must be positive")

        rng = random.Random(seed)

        # w1: hidden_size x 81
        self.w1: list[list[float]] = [
            [rng.uniform(-0.5, 0.5) for _ in range(self.input_size)]
            for _ in range(self.hidden_size)
        ]
        # b1: hidden_size
        self.b1: list[float] = [rng.uniform(-0.5, 0.5) for _ in range(self.hidden_size)]
        # w2: hidden_size
        self.w2: list[float] = [rng.uniform(-0.5, 0.5) for _ in range(self.hidden_size)]
        # b2: scalar
        self.b2: float = rng.uniform(-0.5, 0.5)

    @staticmethod
    def _sigmoid(x: float) -> float:
        # Numerically stable sigmoid
        if x >= 0:
            z = math.exp(-x)
            return 1.0 / (1.0 + z)
        z = math.exp(x)
        return z / (1.0 + z)

    def _validate_input(self, x: list[float]) -> None:
        if len(x) != self.input_size:
            raise ValueError(f"Expected input length {self.input_size}, got {len(x)}")

    def forward(self, x: list[float]) -> float:
        self._validate_input(x)

        hidden: list[float] = []
        for i in range(self.hidden_size):
            s = self.b1[i]
            wi = self.w1[i]
            for j in range(self.input_size):
                s += wi[j] * x[j]
            hidden.append(self._sigmoid(s))

        out = self.b2
        for i in range(self.hidden_size):
            out += self.w2[i] * hidden[i]
        return self._sigmoid(out)

    def predict_proba(self, x: list[float]) -> float:
        return self.forward(x)

    def predict(self, x: list[float], threshold: float = 0.5) -> int:
        proba = self.predict_proba(x)
        return 1 if proba >= threshold else 0
