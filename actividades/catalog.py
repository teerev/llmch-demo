"""Datos de actividades."""
from typing import List, Dict

_ACTIVITIES: List[Dict[str, str]] = [
    {"id": "club_lectura", "title": "Club de lectura", "description": "Reuniones semanales para compartir lecturas y promover liderazgo."},
    {"id": "taller_ciencia", "title": "Taller de ciencia", "description": "Experimentos guiados para fortalecer habilidades STEM en un entorno seguro."},
    {"id": "deporte_inclusivo", "title": "Deporte inclusivo", "description": "Actividad física enfocada en trabajo en equipo y bienestar."}
]


def get_activities() -> List[Dict[str, str]]:
    """Return list of activity dicts with keys id, title, description."""
    return list(_ACTIVITIES)
