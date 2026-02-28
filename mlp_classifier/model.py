import math
import random
from typing import List, Sequence, Tuple


class MLPClassifier:
    def __init__(self, input_size=81, hidden_sizes=None, output_size=2, seed=None):
        if hidden_sizes is None:
            hidden_sizes = [16]
        if not isinstance(hidden_sizes, list) or len(hidden_sizes) != 1:
            raise ValueError("Only a single hidden layer is supported: hidden_sizes must be a list of length 1")

        self.input_size = int(input_size)
        self.hidden_sizes = hidden_sizes
        self.hidden_size = int(hidden_sizes[0])
        self.output_size = int(output_size)
        self.seed = seed

        rng = random.Random(seed)

        # Weights: w1 (hidden x input), b1 (hidden), w2 (output x hidden), b2 (output)
        self.w1 = [
            [rng.uniform(-0.5, 0.5) for _ in range(self.input_size)]
            for _ in range(self.hidden_size)
        ]
        self.b1 = [rng.uniform(-0.5, 0.5) for _ in range(self.hidden_size)]

        self.w2 = [
            [rng.uniform(-0.5, 0.5) for _ in range(self.hidden_size)]
            for _ in range(self.output_size)
        ]
        self.b2 = [rng.uniform(-0.5, 0.5) for _ in range(self.output_size)]

    def train(self, X, y, epochs=100, lr=0.1):
        """Train using SGD + backpropagation for a single hidden layer.

        Uses cross-entropy loss with softmax output.
        Deterministic: iterates samples in fixed order for each epoch.
        """
        if len(X) != len(y):
            raise ValueError("X and y must have the same length")

        n = len(X)
        if n == 0:
            return

        for _ in range(int(epochs)):
            for x, y_true in zip(X, y):
                if len(x) != self.input_size:
                    raise ValueError(f"Expected input vector of length {self.input_size}, got {len(x)}")
                if not (0 <= int(y_true) < self.output_size):
                    raise ValueError(f"y value {y_true} out of range for output_size={self.output_size}")

                # Forward pass (explicitly compute pre-activations for backprop)
                z1 = [0.0] * self.hidden_size
                h = [0.0] * self.hidden_size
                for i in range(self.hidden_size):
                    s = self.b1[i]
                    wi = self.w1[i]
                    for j in range(self.input_size):
                        s += wi[j] * x[j]
                    z1[i] = s
                    h[i] = self._sigmoid(s)

                logits = [0.0] * self.output_size
                for k in range(self.output_size):
                    s = self.b2[k]
                    wk = self.w2[k]
                    for i in range(self.hidden_size):
                        s += wk[i] * h[i]
                    logits[k] = s

                probs = self._softmax(logits)

                # Output delta: dL/dlogits = probs - one_hot(y_true)
                delta2 = probs[:]  # copy
                delta2[int(y_true)] -= 1.0

                # Gradients for w2, b2 and update
                for k in range(self.output_size):
                    dk = delta2[k]
                    # b2
                    self.b2[k] -= lr * dk
                    # w2
                    wk = self.w2[k]
                    for i in range(self.hidden_size):
                        wk[i] -= lr * (dk * h[i])

                # Backprop to hidden: delta1 = (W2^T * delta2) * sigmoid'(z1)
                delta1 = [0.0] * self.hidden_size
                for i in range(self.hidden_size):
                    s = 0.0
                    for k in range(self.output_size):
                        s += self.w2[k][i] * delta2[k]
                    hi = h[i]
                    delta1[i] = s * (hi * (1.0 - hi))

                # Gradients for w1, b1 and update
                for i in range(self.hidden_size):
                    di = delta1[i]
                    self.b1[i] -= lr * di
                    wi = self.w1[i]
                    for j in range(self.input_size):
                        wi[j] -= lr * (di * x[j])

    @staticmethod
    def _sigmoid(x: float) -> float:
        # Numerically stable sigmoid
        if x >= 0:
            z = math.exp(-x)
            return 1.0 / (1.0 + z)
        z = math.exp(x)
        return z / (1.0 + z)

    @staticmethod
    def _softmax(logits: Sequence[float]) -> List[float]:
        m = max(logits)
        exps = [math.exp(v - m) for v in logits]
        s = sum(exps)
        if s == 0:
            # Fallback (should not happen with exp), but keep deterministic behavior.
            return [1.0 / len(exps) for _ in exps]
        return [e / s for e in exps]

    def _forward(self, x: Sequence[float]) -> Tuple[List[float], List[float]]:
        if len(x) != self.input_size:
            raise ValueError(f"Expected input vector of length {self.input_size}, got {len(x)}")

        # Hidden layer
        hidden = []
        for i in range(self.hidden_size):
            s = self.b1[i]
            wi = self.w1[i]
            for j in range(self.input_size):
                s += wi[j] * x[j]
            hidden.append(self._sigmoid(s))

        # Output layer logits
        logits = []
        for k in range(self.output_size):
            s = self.b2[k]
            wk = self.w2[k]
            for i in range(self.hidden_size):
                s += wk[i] * hidden[i]
            logits.append(s)

        probs = self._softmax(logits)
        return hidden, probs

    def predict_proba(self, X):
        # Return list of probability lists per sample
        probs_all = []
        for x in X:
            _, probs = self._forward(x)
            probs_all.append(probs)
        return probs_all

    def predict(self, X):
        preds = []
        for x in X:
            _, probs = self._forward(x)
            # argmax
            best_i = 0
            best_v = probs[0]
            for i in range(1, len(probs)):
                if probs[i] > best_v:
                    best_v = probs[i]
                    best_i = i
            preds.append(best_i)
        return preds
