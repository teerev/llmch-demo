import json
from dataclasses import FrozenInstanceError

import pytest

from ccsd_pipeline.schema import ElectronDensityRecord, TrainingConfig, load_config


def test_load_config(tmp_path):
    cfg_path = tmp_path / "config.json"
    cfg_data = {
        "data_path": "./data/train.json",
        "epochs": 5,
        "learning_rate": 0.001,
        "output_path": "./out",
    }
    cfg_path.write_text(json.dumps(cfg_data), encoding="utf-8")

    cfg = load_config(cfg_path)
    assert isinstance(cfg, TrainingConfig)
    assert cfg.data_path == cfg_data["data_path"]
    assert cfg.epochs == cfg_data["epochs"]
    assert cfg.learning_rate == pytest.approx(cfg_data["learning_rate"])
    assert cfg.output_path == cfg_data["output_path"]


def test_electron_density_record_construction_and_immutability():
    rec = ElectronDensityRecord(density=[0.1, 0.2, 0.3], energy=-1.23, metadata={"id": "abc"})
    assert rec.density == [0.1, 0.2, 0.3]
    assert rec.energy == -1.23
    assert rec.metadata["id"] == "abc"

    with pytest.raises(FrozenInstanceError):
        rec.energy = 0.0
