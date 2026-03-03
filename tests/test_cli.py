from __future__ import annotations

import json
from pathlib import Path

import pytest

from ccsd_pipeline.cli import build_parser, main


def test_build_parser_requires_subcommand() -> None:
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args([])


def test_train_subcommand_requires_config() -> None:
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["train"])


def test_cli_train_end_to_end(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    # Minimal dataset compatible with ccsd_pipeline.data.load_dataset
    dataset_path = tmp_path / "dataset.json"
    dataset = [
        {"density": [0.1, 0.2, 0.3], "energy": 1.23, "metadata": {"id": "a"}},
        {"density": [0.0, 0.0, 0.1], "energy": 0.5, "metadata": {"id": "b"}},
    ]
    dataset_path.write_text(json.dumps(dataset), encoding="utf-8")

    model_path = tmp_path / "out" / "model.json"
    config_path = tmp_path / "config.json"
    config = {
        "data_path": str(dataset_path),
        "epochs": 1,
        "learning_rate": 0.01,
        "output_path": str(model_path),
    }
    config_path.write_text(json.dumps(config), encoding="utf-8")

    rc = main(["train", "--config", str(config_path)])
    assert rc == 0

    out = capsys.readouterr().out.strip()
    assert out == str(model_path)
    assert model_path.exists()
