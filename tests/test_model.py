import math
import pytest

from ccsd_pipeline.model import EquivariantEnergyModel


def test_default_init_weights_and_bias():
    m = EquivariantEnergyModel(input_dim=3)
    assert m.weights == [0.0, 0.0, 0.0]
    assert m.bias == 0.0


def test_forward_dot_plus_bias():
    m = EquivariantEnergyModel(input_dim=3, weights=[1.0, 2.0, 3.0], bias=0.5)
    y = m.forward([1.0, 1.0, 1.0])
    assert y == pytest.approx(6.5)


def test_train_step_updates_weights_and_bias_and_returns_loss():
    m = EquivariantEnergyModel(input_dim=2)  # weights=[0,0], bias=0
    density = [1.0, 2.0]
    target = 1.0
    lr = 0.1

    # pred=0, err=-1, loss=1
    loss = m.train_step(density, target, lr=lr)
    assert loss == pytest.approx(1.0)

    # grad_common = 2*err = -2
    # w_new = 0 - lr * (-2) * x = 0 + 0.2*x
    assert m.weights[0] == pytest.approx(0.2)
    assert m.weights[1] == pytest.approx(0.4)
    # b_new = 0 - lr * (-2) = 0.2
    assert m.bias == pytest.approx(0.2)

    # After update, prediction should be closer to target
    pred_after = m.forward(density)
    assert abs(pred_after - target) < 1.0


def test_to_dict_from_dict_roundtrip():
    m = EquivariantEnergyModel(input_dim=3, weights=[0.1, -0.2, 0.3], bias=-0.4)
    d = m.to_dict()
    m2 = EquivariantEnergyModel.from_dict(d)
    assert m2.input_dim == 3
    assert m2.weights == pytest.approx([0.1, -0.2, 0.3])
    assert m2.bias == pytest.approx(-0.4)


def test_forward_validates_input_dim():
    m = EquivariantEnergyModel(input_dim=2)
    with pytest.raises(ValueError):
        m.forward([1.0])


def test_train_step_requires_positive_lr():
    m = EquivariantEnergyModel(input_dim=1)
    with pytest.raises(ValueError):
        m.train_step([1.0], 0.0, lr=0.0)
