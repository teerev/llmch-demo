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


def test_predict_proba_shape_and_normalization():
    clf = MLPClassifier(input_size=3, hidden_sizes=[4], output_size=2, seed=123)
    X = [
        [0.0, 0.0, 0.0],
        [1.0, -1.0, 0.5],
        [2.0, 3.0, -4.0],
    ]
    probs = clf.predict_proba(X)

    assert isinstance(probs, list)
    assert len(probs) == len(X)
    for row in probs:
        assert isinstance(row, list)
        assert len(row) == 2
        s = sum(row)
        assert abs(s - 1.0) < 1e-9
        assert all(0.0 <= p <= 1.0 for p in row)


def test_predict_shape_and_range_and_determinism():
    X = [
        [0.25, -0.5, 1.0],
        [0.0, 0.0, 0.0],
        [10.0, -3.0, 2.0],
    ]

    clf1 = MLPClassifier(input_size=3, hidden_sizes=[4], output_size=3, seed=7)
    clf2 = MLPClassifier(input_size=3, hidden_sizes=[4], output_size=3, seed=7)

    p1 = clf1.predict(X)
    p2 = clf2.predict(X)

    assert isinstance(p1, list)
    assert len(p1) == len(X)
    assert p1 == p2
    assert all(isinstance(v, int) for v in p1)
    assert all(0 <= v < 3 for v in p1)


def test_hidden_sizes_must_be_single_layer():
    try:
        MLPClassifier(input_size=3, hidden_sizes=[4, 4], output_size=2, seed=0)
        assert False, "Expected ValueError for multi-layer hidden_sizes"
    except ValueError:
        pass
