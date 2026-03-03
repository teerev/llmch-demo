from mlp9x9.model import MLP


def test_train_learns_zeros_vs_ones_no_hidden():
    # Two extreme samples: all zeros -> 0, all ones -> 1
    x0 = [0.0] * 81
    x1 = [1.0] * 81
    X = [x0, x1]
    y = [0, 1]

    mlp = MLP(hidden_sizes=(), seed=123)

    epochs = 400
    history = mlp.train(X, y, epochs=epochs, lr=0.5)

    assert isinstance(history, list)
    assert len(history) == epochs

    assert mlp.predict(x0) == 0
    assert mlp.predict(x1) == 1
