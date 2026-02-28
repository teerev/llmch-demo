import inspect

from mlp_classifier import MLPClassifier


def test_public_api_exposed():
    assert hasattr(MLPClassifier, "__init__")
    assert hasattr(MLPClassifier, "train")
    assert hasattr(MLPClassifier, "predict")
    assert hasattr(MLPClassifier, "predict_proba")


def test_signatures():
    assert str(inspect.signature(MLPClassifier.__init__)) == "(self, input_size=81, hidden_sizes=None, output_size=2, seed=None)"
    assert str(inspect.signature(MLPClassifier.train)) == "(self, X, y, epochs=100, lr=0.1)"
    assert str(inspect.signature(MLPClassifier.predict)) == "(self, X)"
    assert str(inspect.signature(MLPClassifier.predict_proba)) == "(self, X)"
