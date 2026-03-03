from __future__ import annotations

from dataclasses import dataclass
import json
from importlib import resources


@dataclass(frozen=True)
class Activity:
    title: str
    description: str
    audience: str
    duration_minutes: int


def load_activities() -> list[Activity]:
    """Load activities from the packaged JSON file and return typed Activity objects."""
    data = resources.files("mujer_escuela.data").joinpath("activities.json").read_text(
        encoding="utf-8"
    )
    items = json.loads(data)
    return [Activity(**item) for item in items]
