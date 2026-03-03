import json

import pytest

from ccsd_pipeline.data import load_dataset
from ccsd_pipeline.schema import ElectronDensityRecord


def test_load_dataset_roundtrip(tmp_path):
    dataset = [
        {"density": [0.1, 0.2, 0.3], "energy": -1.25, "metadata": {"id": "a"}},
        {"density": [1, 2, 3], "energy": 4, "metadata": {"id": "b", "note": "ok"}},
    ]

    p = tmp_path / "dataset.json"
    p.write_text(json.dumps(dataset), encoding="utf-8")

    records = load_dataset(p)

    assert isinstance(records, list)
    assert len(records) == 2
    assert all(isinstance(r, ElectronDensityRecord) for r in records)

    assert records[0].density == [0.1, 0.2, 0.3]
    assert records[0].energy == -1.25
    assert records[0].metadata == {"id": "a"}

    assert records[1].density == [1.0, 2.0, 3.0]
    assert records[1].energy == 4.0
    assert records[1].metadata["id"] == "b"


def test_load_dataset_requires_list_root(tmp_path):
    p = tmp_path / "dataset.json"
    p.write_text(json.dumps({"not": "a list"}), encoding="utf-8")

    with pytest.raises(TypeError, match="Dataset JSON must be a list"):
        load_dataset(p)


def test_load_dataset_missing_key(tmp_path):
    p = tmp_path / "dataset.json"
    p.write_text(json.dumps([{ "density": [0.0], "energy": 0.0 }]), encoding="utf-8")

    with pytest.raises(KeyError, match="Missing required dataset key: metadata"):
        load_dataset(p)
