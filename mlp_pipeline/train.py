from __future__ import annotations

import math
from typing import Any, List, Sequence, Tuple

from .config import TrainConfig
from .model import MLP


def validate_inputs(X: Any, y: Any, config: TrainConfig) -> None:
    """Validate X and y against config.

    Accepts:
      - X shape (batch, H, W) where H/W match config
      - X shape (batch, input_size)

    Raises ValueError on mismatch.
    """
    if not isinstance(X, (list, tuple)) or len(X) == 0:
        raise ValueError("X must be a non-empty batch (list/tuple)")

    batch = len(X)

    # Validate y length
    if not isinstance(y, (list, tuple)):
        raise ValueError("y must be a list/tuple with length equal to batch")
    if len(y) != batch:
        raise ValueError(f"y length mismatch: got {len(y)} expected {batch}")

    first = X[0]
    if not isinstance(first, (list, tuple)):
        raise ValueError("X must be a nested list/tuple")

    # Determine whether 3D (batch,H,W) or 2D (batch,input_size)
    is_3d = (
        len(first) > 0
        and isinstance(first[0], (list, tuple))
    )

    if is_3d:
        # (batch, H, W)
        H = len(first)
        W = len(first[0]) if H else 0
        if H != config.input_height or W != config.input_width:
            raise ValueError(
                f"X spatial shape mismatch: got (H,W)=({H},{W}) expected ({config.input_height},{config.input_width})"
            )
        # Ensure rectangular and consistent
        for i, sample in enumerate(X):
            if not isinstance(sample, (list, tuple)) or len(sample) != H:
                raise ValueError(f"X[{i}] height mismatch")
            for r, row in enumerate(sample):
                if not isinstance(row, (list, tuple)) or len(row) != W:
                    raise ValueError(f"X[{i}][{r}] width mismatch")
    else:
        # (batch, input_size)
        d = len(first)
        if d != config.input_size:
            raise ValueError(
                f"X feature size mismatch: got {d} expected {config.input_size}"
            )
        for i, row in enumerate(X):
            if not isinstance(row, (list, tuple)) or len(row) != d:
                raise ValueError(f"X[{i}] feature length mismatch")


def binary_cross_entropy(y_true: Sequence[Sequence[float]], y_pred: Sequence[Sequence[float]]) -> float:
    """Binary cross entropy averaged over batch.

    y_true and y_pred are expected to be (batch, 1).
    """
    eps = 1e-12
    n = len(y_true)
    if n == 0:
        return 0.0
    total = 0.0
    for i in range(n):
        yt = float(y_true[i][0])
        yp = float(y_pred[i][0])
        yp = min(max(yp, eps), 1.0 - eps)
        total += -(yt * math.log(yp) + (1.0 - yt) * math.log(1.0 - yp))
    return total / n


def _tanh_deriv_from_activation(a: float) -> float:
    # If a = tanh(z), then d/dz tanh(z) = 1 - a^2
    return 1.0 - a * a


def train_epoch(model: MLP, X: Any, y: Sequence[Sequence[float]], lr: float) -> float:
    """Run one full-batch gradient descent epoch.

    Uses model.forward_with_cache to get activations and pre-activations.
    Backprop assumes tanh hidden activations and sigmoid output.

    Updates model.weights and model.biases in-place.
    Returns average BCE loss.
    """
    y_pred, cache = model.forward_with_cache(X)
    loss = binary_cross_entropy(y, y_pred)

    activations: List[List[List[float]]] = cache["activations"]
    # pre_activations not strictly needed for tanh derivative (we use activation), but kept for clarity
    _ = cache["pre_activations"]

    n = len(y)
    if n == 0:
        return 0.0

    # dZ for output layer with sigmoid + BCE: dZ = (A_L - y)
    dZ: List[List[float]] = [[(y_pred[i][0] - float(y[i][0])) for _ in range(1)] for i in range(n)]

    num_layers = len(model.weights)

    for layer_idx in range(num_layers - 1, -1, -1):
        A_prev = activations[layer_idx]  # (n, in_dim)
        W = model.weights[layer_idx]     # (in_dim, out_dim)
        b = model.biases[layer_idx]      # (out_dim,)

        in_dim = len(W)
        out_dim = len(W[0]) if in_dim else 0

        # Compute gradients: dW = A_prev^T @ dZ / n, db = sum(dZ)/n
        dW = [[0.0 for _ in range(out_dim)] for _ in range(in_dim)]
        db = [0.0 for _ in range(out_dim)]

        for i in range(n):
            for j in range(out_dim):
                db[j] += dZ[i][j]
            Ai = A_prev[i]
            for k in range(in_dim):
                aik = Ai[k]
                if aik == 0.0:
                    continue
                for j in range(out_dim):
                    dW[k][j] += aik * dZ[i][j]

        inv_n = 1.0 / n
        for j in range(out_dim):
            db[j] *= inv_n
        for k in range(in_dim):
            for j in range(out_dim):
                dW[k][j] *= inv_n

        # Compute dA_prev = dZ @ W^T
        if layer_idx > 0:
            dA_prev = [[0.0 for _ in range(in_dim)] for _ in range(n)]
            for i in range(n):
                for k in range(in_dim):
                    s = 0.0
                    Wk = W[k]
                    for j in range(out_dim):
                        s += dZ[i][j] * Wk[j]
                    dA_prev[i][k] = s

            # dZ_prev = dA_prev * tanh'(Z_prev) = dA_prev * (1 - A_prev^2)
            A_prev_act = activations[layer_idx]  # this is tanh output for hidden layers
            dZ_prev = [[0.0 for _ in range(in_dim)] for _ in range(n)]
            for i in range(n):
                for k in range(in_dim):
                    dZ_prev[i][k] = dA_prev[i][k] * _tanh_deriv_from_activation(float(A_prev_act[i][k]))
        else:
            dZ_prev = []

        # Gradient descent update
        for k in range(in_dim):
            for j in range(out_dim):
                W[k][j] -= lr * dW[k][j]
        for j in range(out_dim):
            b[j] -= lr * db[j]

        dZ = dZ_prev

    return loss


def train_mlp(X: Any, y: Sequence[float], config: TrainConfig) -> Tuple[MLP, List[float]]:
    """Train an MLP with simple full-batch gradient descent.

    Returns (model, loss_history).
    """
    validate_inputs(X, y, config)

    # Ensure y is (batch,1) float
    y2d: List[List[float]] = [[float(v)] for v in y]

    model = MLP(config)
    history: List[float] = []

    lr = float(config.learning_rate)
    for _epoch in range(int(config.epochs)):
        loss = train_epoch(model, X, y2d, lr)
        history.append(float(loss))

    return model, history
