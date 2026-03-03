from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Union

from ccsd_pipeline.data import load_dataset
from ccsd_pipeline.model import EquivariantEnergyModel
from ccsd_pipeline.schema import TrainingConfig


PathLike = Union[str, Path]


@dataclass(frozen=True)
class TrainingResult:
    final_loss: float
    model_path: str


def save_model(model: EquivariantEnergyModel, path: PathLike) -> str:
    """Serialize `model` to JSON at `path`.

    Returns the string path written.
    """
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        json.dump(model.to_dict(), f, indent=2, sort_keys=True)
    return str(p)


def load_model(path: PathLike) -> EquivariantEnergyModel:
    """Load a model previously saved by `save_model`."""
    p = Path(path)
    with p.open("r", encoding="utf-8") as f:
        d = json.load(f)
    return EquivariantEnergyModel.from_dict(d)


def train_model(config: TrainingConfig) -> TrainingResult:
    """Train a model from a TrainingConfig.

    Steps:
      - load dataset
      - infer input_dim from first record density length
      - initialize model
      - run `epochs` over all records calling `train_step`
      - save model JSON to `output_path`
      - return TrainingResult(final_loss, model_path)
    """
    records = load_dataset(config.data_path)
    if len(records) == 0:
        raise ValueError("Dataset is empty")

    input_dim = len(records[0].density)
    model = EquivariantEnergyModel(input_dim=input_dim)

    final_loss = 0.0
    for _ in range(int(config.epochs)):
        for rec in records:
            final_loss = model.train_step(rec.density, rec.energy, lr=config.learning_rate)

    model_path = save_model(model, config.output_path)
    return TrainingResult(final_loss=float(final_loss), model_path=model_path)
