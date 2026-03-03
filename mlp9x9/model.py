import math
import random
from typing import Iterable, List, Sequence, Tuple

from mlp9x9.data import validate_flat_input


def _sigmoid(z: float) -> float:
    # Numerically stable sigmoid
    if z >= 0:
        ez = math.exp(-z)
        return 1.0 / (1.0 + ez)
    ez = math.exp(z)
    return ez / (1.0 + ez)


class MLP:
    """A small pure-Python MLP for forward inference on flat inputs.

    Uses sigmoid activations for all layers.
    """

    def __init__(
        self,
        input_size: int = 81,
        hidden_sizes: Tuple[int, ...] = (16,),
        output_size: int = 1,
        seed=None,
    ):
        if output_size != 1:
            raise ValueError("Only output_size==1 is supported")

        self.input_size = int(input_size)
        self.hidden_sizes = tuple(int(h) for h in hidden_sizes)
        self.output_size = int(output_size)

        layer_sizes: List[int] = [self.input_size, *self.hidden_sizes, self.output_size]

        rng = random.Random(seed)
        self.weights: List[List[List[float]]] = []
        self.biases: List[List[float]] = []

        for in_size, out_size in zip(layer_sizes[:-1], layer_sizes[1:]):
            w = [[rng.uniform(-0.5, 0.5) for _ in range(in_size)] for _ in range(out_size)]
            b = [rng.uniform(-0.5, 0.5) for _ in range(out_size)]
            self.weights.append(w)
            self.biases.append(b)

    def forward(self, x: Sequence[float]) -> float:
        if len(x) != self.input_size:
            raise ValueError(f"Expected input of length {self.input_size}, got {len(x)}")

        a: List[float] = [float(v) for v in x]

        for w, b in zip(self.weights, self.biases):
            next_a: List[float] = []
            for j in range(len(w)):
                z = b[j]
                row = w[j]
                for i in range(len(row)):
                    z += row[i] * a[i]
                next_a.append(_sigmoid(z))
            a = next_a

        # output_size is enforced to 1
        return float(a[0])

    def predict_proba(self, x: Sequence[float]) -> float:
        return self.forward(x)

    def predict(self, x: Sequence[float], threshold: float = 0.5) -> int:
        return 1 if self.forward(x) >= threshold else 0

    def train(
        self,
        X: Sequence[Iterable[float]],
        y: Sequence[int],
        epochs: int = 10,
        lr: float = 0.1,
    ) -> List[float]:
        """Train the network using batch gradient descent.

        - Sigmoid activations for all layers
        - Mean squared error loss

        Args:
            X: iterable of flat 81-length inputs (values in [0,1])
            y: iterable of targets (0 or 1)
            epochs: number of epochs
            lr: learning rate

        Returns:
            List of average loss values per epoch (length == epochs)

        Raises:
            ValueError: if len(X) != len(y) or targets are not 0/1
        """
        if len(X) != len(y):
            raise ValueError("X and y must have the same length")

        # Validate targets and inputs (validate_flat_input on each x)
        Xv: List[List[float]] = []
        yv: List[float] = []
        for i, (xi, yi) in enumerate(zip(X, y)):
            if yi not in (0, 1):
                raise ValueError("Targets must be 0 or 1")
            Xv.append(validate_flat_input(xi))
            yv.append(float(yi))

        n = len(Xv)
        if n == 0:
            # Nothing to train; still return epochs losses (all 0.0) to match contract.
            return [0.0 for _ in range(int(epochs))]

        epochs_i = int(epochs)
        history: List[float] = []

        for _ in range(epochs_i):
            # Initialize accumulators for gradients
            grad_w: List[List[List[float]]] = []
            grad_b: List[List[float]] = []
            for w, b in zip(self.weights, self.biases):
                grad_w.append([[0.0 for _ in range(len(w[0]))] for _ in range(len(w))])
                grad_b.append([0.0 for _ in range(len(b))])

            total_loss = 0.0

            for x, target in zip(Xv, yv):
                # Forward pass with caches
                activations: List[List[float]] = []
                zs: List[List[float]] = []

                a: List[float] = [float(v) for v in x]
                activations.append(a)

                for w, b in zip(self.weights, self.biases):
                    z_layer: List[float] = []
                    a_next: List[float] = []
                    for j in range(len(w)):
                        z = b[j]
                        row = w[j]
                        for i in range(len(row)):
                            z += row[i] * a[i]
                        z_layer.append(z)
                        a_next.append(_sigmoid(z))
                    zs.append(z_layer)
                    activations.append(a_next)
                    a = a_next

                out = activations[-1][0]
                err = out - target
                total_loss += err * err

                # Backward pass
                # delta for output layer: dL/da * da/dz
                # L = (out - t)^2 => dL/da = 2*(out - t)
                # sigmoid' = a*(1-a)
                delta: List[float] = [2.0 * err * out * (1.0 - out)]

                # Accumulate gradients for last layer
                last = len(self.weights) - 1
                a_prev = activations[last]
                for j in range(len(delta)):
                    grad_b[last][j] += delta[j]
                    for i in range(len(a_prev)):
                        grad_w[last][j][i] += delta[j] * a_prev[i]

                # Propagate backwards through hidden layers (if any)
                for layer in range(len(self.weights) - 2, -1, -1):
                    w_next = self.weights[layer + 1]
                    a_layer = activations[layer + 1]

                    new_delta: List[float] = [0.0 for _ in range(len(a_layer))]
                    for j in range(len(a_layer)):
                        s = 0.0
                        for k in range(len(delta)):
                            s += w_next[k][j] * delta[k]
                        new_delta[j] = s * a_layer[j] * (1.0 - a_layer[j])

                    delta = new_delta

                    a_prev = activations[layer]
                    for j in range(len(delta)):
                        grad_b[layer][j] += delta[j]
                        for i in range(len(a_prev)):
                            grad_w[layer][j][i] += delta[j] * a_prev[i]

            # Average loss and gradients
            avg_loss = total_loss / float(n)
            history.append(avg_loss)

            inv_n = 1.0 / float(n)
            for layer in range(len(self.weights)):
                for j in range(len(self.weights[layer])):
                    self.biases[layer][j] -= lr * (grad_b[layer][j] * inv_n)
                    for i in range(len(self.weights[layer][j])):
                        self.weights[layer][j][i] -= lr * (grad_w[layer][j][i] * inv_n)

        return history
