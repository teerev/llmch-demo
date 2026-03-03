import math
import random
from typing import Iterable, List, Sequence, Tuple


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
