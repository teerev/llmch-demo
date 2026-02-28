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

    def train_epoch(self, dataset: Dataset, lr: float) -> float:
        """Train for one epoch using SGD and binary cross-entropy.

        Updates parameters in-place: w2, b2, w1, b1.

        Returns:
            Average loss over the dataset.
        """
        if lr <= 0:
            raise ValueError("lr must be positive")
        if len(dataset) == 0:
            raise ValueError("dataset must be non-empty")

        total_loss = 0.0
        n = 0

        # Small epsilon to avoid log(0)
        eps = 1e-12

        for x, y in dataset:
            self._validate_input(x)
            if y not in (0, 1):
                raise ValueError("Labels must be 0 or 1")

            # Forward pass (keep activations for backprop)
            hidden: list[float] = [0.0] * self.hidden_size
            for i in range(self.hidden_size):
                s = self.b1[i]
                wi = self.w1[i]
                for j in range(self.input_size):
                    s += wi[j] * x[j]
                hidden[i] = self._sigmoid(s)

            out_logit = self.b2
            for i in range(self.hidden_size):
                out_logit += self.w2[i] * hidden[i]
            output = self._sigmoid(out_logit)

            # Binary cross-entropy loss
            o = min(1.0 - eps, max(eps, output))
            total_loss += -(y * math.log(o) + (1 - y) * math.log(1.0 - o))
            n += 1

            # Backprop
            # For sigmoid + BCE, dL/d(out_logit) = output - y
            error_out = output - float(y)

            # Use a copy of current w2 to compute hidden errors before updating w2
            w2_old = self.w2[:]

            # Gradients for output layer
            for i in range(self.hidden_size):
                self.w2[i] -= lr * (error_out * hidden[i])
            self.b2 -= lr * error_out

            # Hidden layer errors and updates
            for i in range(self.hidden_size):
                # dL/d(hidden_pre) = (dL/d(out_logit) * w2_old[i]) * sigmoid'(hidden_pre)
                # where sigmoid'(a) = h*(1-h)
                h = hidden[i]
                error_h = (error_out * w2_old[i]) * (h * (1.0 - h))

                wi = self.w1[i]
                for j in range(self.input_size):
                    wi[j] -= lr * (error_h * x[j])
                self.b1[i] -= lr * error_h

        return total_loss / float(n)

    def train(self, dataset: Dataset, epochs: int = 1, lr: float = 0.1) -> list[float]:
        """Train for multiple epochs.

        Returns:
            List of average losses, one per epoch.
        """
        if epochs <= 0:
            raise ValueError("epochs must be positive")
        losses: list[float] = []
        for _ in range(int(epochs)):
            losses.append(self.train_epoch(dataset=dataset, lr=lr))
        return losses
