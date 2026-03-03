from mlp_pipeline.config import TrainConfig
from mlp_pipeline.model import MLP


def test_forward_shape_and_range_on_zeros():
    cfg = TrainConfig(input_height=2, input_width=3, hidden_sizes=(4,), seed=0)
    model = MLP(cfg)

    # batch=1, H=2, W=3
    X = [[[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]]
    probs = model.forward(X)

    assert isinstance(probs, list)
    assert len(probs) == 1
    assert isinstance(probs[0], list)
    assert len(probs[0]) == 1

    p = probs[0][0]
    assert 0.0 <= p <= 1.0
