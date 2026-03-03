"""Datos de actividades."""
from typing import List, Dict

_ACTIVITIES: List[Dict[str, str]] = []

def get_activities() -> List[Dict[str, str]]:
    """Return list of activity dicts with keys id, title, description."""
    return list(_ACTIVITIES)
