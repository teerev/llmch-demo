from mlp9x9 import MLP


def test_predict_proba_and_predict_api():
    model = MLP(seed=123)
    x = [0.0] * 81

    p = model.predict_proba(x)
    assert isinstance(p, float)
    assert 0.0 <= p <= 1.0

    y = model.predict(x)
    assert y in (0, 1)
