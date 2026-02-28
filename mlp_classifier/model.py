class MLPClassifier:
    def __init__(self, input_size=81, hidden_sizes=None, output_size=2, seed=None):
        raise NotImplementedError

    def train(self, X, y, epochs=100, lr=0.1):
        raise NotImplementedError

    def predict(self, X):
        raise NotImplementedError

    def predict_proba(self, X):
        raise NotImplementedError
