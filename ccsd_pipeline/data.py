from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ccsd_pipeline.schema import ElectronDensityRecord


def _require_key(obj: dict[str, Any], key: str) -> Any:
    if key not in obj:
        raise KeyError(f"Missing required dataset key: {key}")
    return obj[key]


def load_dataset(path: str | Path) -> list[ElectronDensityRecord]:
    """Load a JSON dataset from `path`.

    Expected format: a JSON list of objects, each with keys:
      - density: list[float]
      - energy: float
      - metadata: dict

    Returns:
      List[ElectronDensityRecord]
    """
    p = Path(path)
    with p.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise TypeError("Dataset JSON must be a list")

    records: list[ElectronDensityRecord] = []
    for i, item in enumerate(data):
        if not isinstance(item, dict):
            raise TypeError(f"Dataset record at index {i} must be an object")

        density = _require_key(item, "density")
        energy = _require_key(item, "energy")
        metadata = _require_key(item, "metadata")

        if not isinstance(density, list) or not all(isinstance(x, (int, float)) for x in density):
            raise TypeError(f"Record {i}: density must be a list of numbers")
        if not isinstance(energy, (int, float)):
            raise TypeError(f"Record {i}: energy must be a number")
        if not isinstance(metadata, dict):
            raise TypeError(f"Record {i}: metadata must be an object")

        records.append(
            ElectronDensityRecord(
                density=[float(x) for x in density],
                energy=float(energy),
                metadata=metadata,
            )
        )

    return records
