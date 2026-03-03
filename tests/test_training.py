from __future__ import annotations

import json
from pathlib import Path

import pytest

from ccsd_pipeline.schema import TrainingConfig
from ccsd_pipeline.training import load_model, save_model, train_model


def _write_dataset(path: Path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(records), encoding="utf-8")


def test_train_model_writes_json_and_returns_result(tmp_path: Path) -> None:
    data_path = tmp_path / "data.json"
    out_path = tmp_path / "model.json"

    # Simple linear relation: energy = 2*x0 - 1*x1 + 0.5
    records = [
        {"density": [1.0, 0.0], "energy": 2.5, "metadata": {}},
        {"density": [0.0, 1.0], "energy": -0.5, "metadata": {}},
        {"density": [1.0, 1.0], "energy": 1.5, "metadata": {}},
    ]
    _write_dataset(data_path, records)

    cfg = TrainingConfig(
        data_path=str(data_path),
        epochs=200,
        learning_rate=0.05,
        output_path=str(out_path),
    )

    result = train_model(cfg)

    assert isinstance(result.final_loss, float)
    assert result.final_loss >= 0.0
    assert result.model_path == str(out_path)
    assert out_path.exists()

    # Ensure JSON is readable and has expected keys
    d = json.loads(out_path.read_text(encoding="utf-8"))
    assert set(d.keys()) == {"input_dim", "weights", "bias"}
    assert d["input_dim"] == 2
    assert isinstance(d["weights"], list) and len(d["weights"]) == 2


def test_save_and_load_model_roundtrip(tmp_path: Path) -> None:
    from ccsd_pipeline.model import EquivariantEnergyModel

    model = EquivariantEnergyModel(input_dim=3, weights=[1.0, 2.0, 3.0], bias=-0.25)
    path = tmp_path / "m.json"

    written = save_model(model, path)
    assert written == str(path)
    loaded = load_model(path)

    assert loaded.input_dim == 3
    assert loaded.weights == [1.0, 2.0, 3.0]
    assert loaded.bias == -0.25


def test_train_model_empty_dataset_raises(tmp_path: Path) -> None:
    data_path = tmp_path / "empty.json"
    out_path = tmp_path / "model.json"
    _write_dataset(data_path, [])

    cfg = TrainingConfig(
        data_path=str(data_path),
        epochs=1,
        learning_rate=0.01,
        output_path=str(out_path),
    )

    with pytest.raises(ValueError, match="empty"):
        train_model(cfg)
