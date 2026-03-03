class LinearSVM:
    def __init__(self, learning_rate=0.01, epochs=1000, C=1.0):
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.C = C
        self.weights = None
        self.bias = 0.0

    def fit(self, X, y):
        if not X:
            raise ValueError("X must be a non-empty list of feature lists")
        if len(X) != len(y):
            raise ValueError("X and y must have the same length")

        n_features = len(X[0])
        self.weights = [0.0] * n_features
        self.bias = 0.0

        for _ in range(self.epochs):
            for x, y_i in zip(X, y):
                score = sum(w * x_j for w, x_j in zip(self.weights, x)) + self.bias

                if y_i * score >= 1:
                    gradient_w = self.weights
                    gradient_b = 0.0
                else:
                    gradient_w = [w_j - self.C * y_i * x_j for w_j, x_j in zip(self.weights, x)]
                    gradient_b = -self.C * y_i

                self.weights = [
                    w_j - self.learning_rate * g_j for w_j, g_j in zip(self.weights, gradient_w)
                ]
                self.bias -= self.learning_rate * gradient_b

        return self

    def predict(self, X):
        if self.weights is None:
            raise ValueError("Model is not fitted yet. Call fit before predict.")

        preds = []
        for x in X:
            score = sum(w * x_j for w, x_j in zip(self.weights, x)) + self.bias
            preds.append(1 if score >= 0 else -1)
        return preds
