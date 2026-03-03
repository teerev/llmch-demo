from __future__ import annotations

import math
import random
from typing import Any, Dict, List, Sequence, Tuple

from .config import TrainConfig


def sigmoid(x: float) -> float:
    # Numerically stable sigmoid for scalar x
    if x >= 0:
        z = math.exp(-x)
        return 1.0 / (1.0 + z)
    z = math.exp(x)
    return z / (1.0 + z)


def _tanh(x: float) -> float:
    return math.tanh(x)


def _is_3d_batch(X: Any) -> bool:
    # Accepts nested lists/tuples: (batch, H, W)
    return (
        isinstance(X, (list, tuple))
        and len(X) > 0
        and isinstance(X[0], (list, tuple))
        and len(X[0]) > 0
        and isinstance(X[0][0], (list, tuple))
    )


def _is_2d_batch(X: Any) -> bool:
    # Accepts nested lists/tuples: (batch, input_size)
    return (
        isinstance(X, (list, tuple))
        and len(X) > 0
        and isinstance(X[0], (list, tuple))
        and (len(X[0]) == 0 or not isinstance(X[0][0], (list, tuple)))
    )


def _flatten_batch(X: Any) -> List[List[float]]:
    """Convert X into a 2D batch list: (batch, input_size)."""
    if _is_3d_batch(X):
        out: List[List[float]] = []
        for sample in X:
            flat: List[float] = []
            for row in sample:
                flat.extend([float(v) for v in row])
            out.append(flat)
        return out
    if _is_2d_batch(X):
        return [[float(v) for v in row] for row in X]
    raise TypeError(
        "X must be a nested list/tuple with shape (batch, H, W) or (batch, input_size)"
    )


def _matmul(A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
    # A: (n, d), B: (d, m) => (n, m)
    n = len(A)
    d = len(A[0]) if n else 0
    if d == 0:
        return [[] for _ in range(n)]
    if len(B) != d:
        raise ValueError(f"matmul shape mismatch: A is (n,{d}) but B is ({len(B)},m)")
    m = len(B[0]) if d else 0
    out = [[0.0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        Ai = A[i]
        for k in range(d):
            aik = Ai[k]
            Bk = B[k]
            for j in range(m):
                out[i][j] += aik * Bk[j]
    return out


def _add_bias(Z: List[List[float]], b: List[float]) -> List[List[float]]:
    # Z: (n, m), b: (m,)
    n = len(Z)
    m = len(Z[0]) if n else 0
    if len(b) != m:
        raise ValueError(f"bias length mismatch: got {len(b)} expected {m}")
    return [[Z[i][j] + b[j] for j in range(m)] for i in range(n)]


def _apply_elemwise(M: List[List[float]], fn) -> List[List[float]]:
    return [[fn(v) for v in row] for row in M]


class MLP:
    """A simple MLP for binary classification.

    Uses tanh activations for hidden layers and sigmoid for the output.

    Notes:
      - Implemented without numpy to satisfy environments where numpy is unavailable.
      - Weights are initialized with small normal values using a deterministic seed.
    """

    def __init__(self, config: TrainConfig):
        self.config = config

        layer_sizes: List[int] = [config.input_size, *list(config.hidden_sizes), 1]

        rng = random.Random(config.seed)

        self.weights: List[List[List[float]]] = []  # list of (in_dim x out_dim)
        self.biases: List[List[float]] = []  # list of (out_dim,)

        # Small normal initialization via Box-Muller
        def randn() -> float:
            # Avoid log(0)
            u1 = max(rng.random(), 1e-12)
            u2 = rng.random()
            return math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)

        scale = 0.01
        for in_dim, out_dim in zip(layer_sizes[:-1], layer_sizes[1:]):
            W = [[scale * randn() for _ in range(out_dim)] for _ in range(in_dim)]
            b = [0.0 for _ in range(out_dim)]
            self.weights.append(W)
            self.biases.append(b)

    def forward(self, X: Any) -> List[List[float]]:
        probs, _ = self.forward_with_cache(X)
        return probs

    def forward_with_cache(self, X: Any) -> Tuple[List[List[float]], Dict[str, Any]]:
        X2d = _flatten_batch(X)

        activations: List[List[List[float]]] = [X2d]
        pre_activations: List[List[List[float]]] = []

        A = X2d
        num_layers = len(self.weights)
        for layer_idx in range(num_layers):
            W = self.weights[layer_idx]
            b = self.biases[layer_idx]

            Z = _add_bias(_matmul(A, W), b)
            pre_activations.append(Z)

            is_last = layer_idx == (num_layers - 1)
            if is_last:
                A = _apply_elemwise(Z, sigmoid)
            else:
                A = _apply_elemwise(Z, _tanh)
            activations.append(A)

        cache: Dict[str, Any] = {
            "activations": activations,
            "pre_activations": pre_activations,
        }
        return A, cache
