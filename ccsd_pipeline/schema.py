from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ElectronDensityRecord:
    density: list[float]
    energy: float
    metadata: dict


@dataclass(frozen=True)
class TrainingConfig:
    data_path: str
    epochs: int
    learning_rate: float
    output_path: str


def _require_key(obj: dict[str, Any], key: str) -> Any:
    if key not in obj:
        raise KeyError(f"Missing required config key: {key}")
    return obj[key]


def load_config(path: str | Path) -> TrainingConfig:
    """Load a JSON training config from `path`.

    Expected JSON keys:
      - data_path (str)
      - epochs (int)
      - learning_rate (float)
      - output_path (str)
    """
    p = Path(path)
    with p.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict):
        raise TypeError("Config JSON must be an object")

    data_path = _require_key(data, "data_path")
    epochs = _require_key(data, "epochs")
    learning_rate = _require_key(data, "learning_rate")
    output_path = _require_key(data, "output_path")

    if not isinstance(data_path, str):
        raise TypeError("data_path must be a string")
    if not isinstance(output_path, str):
        raise TypeError("output_path must be a string")
    if not isinstance(epochs, int):
        raise TypeError("epochs must be an int")
    if not isinstance(learning_rate, (int, float)):
        raise TypeError("learning_rate must be a number")

    return TrainingConfig(
        data_path=data_path,
        epochs=epochs,
        learning_rate=float(learning_rate),
        output_path=output_path,
    )
