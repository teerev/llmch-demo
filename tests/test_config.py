from mlp_pipeline.config import TrainConfig


def test_train_config_defaults_and_input_size():
    cfg = TrainConfig()

    assert cfg.input_height == 256
    assert cfg.input_width == 256
    assert cfg.hidden_sizes == (128,)
    assert cfg.learning_rate == 0.01
    assert cfg.epochs == 1
    assert cfg.seed == 0

    assert cfg.input_size == 65536
