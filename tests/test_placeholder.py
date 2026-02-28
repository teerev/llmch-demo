from mlp9 import MLP9


def test_forward_and_predict():
    m = MLP9(hidden_size=4, seed=0)
    x = [0.0] * 81
    p = m.predict_proba(x)
    assert 0.0 <= p <= 1.0
    assert m.predict(x) in (0, 1)


def test_invalid_length_raises():
    m = MLP9(hidden_size=4, seed=0)
    try:
        m.predict_proba([0.0] * 80)
    except ValueError:
        pass
    else:
        assert False


def test_training_reduces_loss():
    m = MLP9(hidden_size=4, seed=0)
    x0 = [0.0] * 81
    x1 = [1.0] * 81
    data = [(x0, 0), (x1, 1)]
    losses = m.train(data, epochs=10, lr=0.5)
    assert min(losses[1:]) < losses[0]
