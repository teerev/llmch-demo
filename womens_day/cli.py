from __future__ import annotations

import sys
from typing import Iterable, Mapping, Any

from .activities import listar_actividades


def format_activities(activities: Iterable[Mapping[str, Any]]) -> str:
    """Format activities as one line per activity with a trailing newline."""

    lines = [f"- {a['titulo']}: {a['descripcion']}" for a in activities]
    return "\n".join(lines) + "\n"


def main() -> None:
    sys.stdout.write(format_activities(listar_actividades()))
