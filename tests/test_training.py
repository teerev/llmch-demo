import random

from mlp_pipeline.config import TrainConfig
from mlp_pipeline.train import train_mlp


def test_train_mlp_history_and_forward_shape():
    rng = random.Random(0)

    config = TrainConfig(
        input_height=2,
        input_width=3,
        hidden_sizes=(4,),
        learning_rate=0.1,
        epochs=5,
        seed=0,
    )

    batch = 8
    # X: (batch, H, W)
    X = [
        [[rng.random() for _ in range(config.input_width)] for _ in range(config.input_height)]
        for _ in range(batch)
    ]
    y = [rng.randint(0, 1) for _ in range(batch)]

    model, history = train_mlp(X, y, config)

    assert len(history) == config.epochs
    assert all(h >= 0.0 for h in history)

    out = model.forward(X)
    assert isinstance(out, list)
    assert len(out) == batch
    assert all(isinstance(row, list) and len(row) == 1 for row in out)
