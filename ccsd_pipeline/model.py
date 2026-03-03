from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Sequence


def _validate_density(density: Sequence[float], input_dim: int) -> List[float]:
    if len(density) != input_dim:
        raise ValueError(f"density length {len(density)} != input_dim {input_dim}")
    return [float(x) for x in density]


@dataclass
class EquivariantEnergyModel:
    """Minimal deterministic model stub.

    Pure Python implementation:
      - weights: list[float]
      - bias: float

    forward(density): dot(weights, density) + bias

    train_step(density, target, lr):
      - computes MSE loss: (pred - target)^2
      - performs one gradient descent step on weights and bias
      - returns loss (float)
    """

    input_dim: int
    weights: List[float] | None = None
    bias: float = 0.0

    def __post_init__(self) -> None:
        if self.input_dim <= 0:
            raise ValueError("input_dim must be positive")
        if self.weights is None:
            self.weights = [0.0 for _ in range(self.input_dim)]
        else:
            if len(self.weights) != self.input_dim:
                raise ValueError(
                    f"weights length {len(self.weights)} != input_dim {self.input_dim}"
                )
            self.weights = [float(w) for w in self.weights]
        self.bias = float(self.bias)

    def forward(self, density: Sequence[float]) -> float:
        x = _validate_density(density, self.input_dim)
        return sum(w * xi for w, xi in zip(self.weights, x)) + self.bias

    def train_step(self, density: Sequence[float], target: float, lr: float = 1e-2) -> float:
        """Single-step gradient descent on MSE loss.

        loss = (pred - target)^2
        dloss/dpred = 2*(pred-target)
        dpred/dw_i = x_i
        dpred/db = 1
        """
        x = _validate_density(density, self.input_dim)
        y = float(target)
        lr = float(lr)
        if lr <= 0:
            raise ValueError("lr must be positive")

        pred = self.forward(x)
        err = pred - y
        loss = err * err

        grad_common = 2.0 * err
        # Update weights and bias
        self.weights = [w - lr * grad_common * xi for w, xi in zip(self.weights, x)]
        self.bias = self.bias - lr * grad_common

        return float(loss)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "input_dim": int(self.input_dim),
            "weights": [float(w) for w in self.weights],
            "bias": float(self.bias),
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "EquivariantEnergyModel":
        if not isinstance(d, dict):
            raise TypeError("from_dict expects a dict")
        input_dim = int(d["input_dim"])
        weights = d.get("weights", None)
        bias = d.get("bias", 0.0)
        if weights is not None:
            weights = [float(w) for w in list(weights)]
        return cls(input_dim=input_dim, weights=weights, bias=float(bias))
