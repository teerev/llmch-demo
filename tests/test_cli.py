import sys
import subprocess

from womens_day.activities import listar_actividades
from womens_day.cli import format_activities


EXPECTED = (
    "- Asamblea sobre igualdad de género: Charla guiada con estudiantes sobre derechos y respeto.\n"
    "- Mural colaborativo: Creación de un mural con mensajes de mujeres de la comunidad escolar.\n"
    "- Lectura de biografías: Lectura en clase de mujeres destacadas en ciencia, arte y deporte.\n"
    "- Taller de ciencia con referentes: Actividad práctica mostrando aportes de científicas.\n"
)


def test_format_activities_matches_expected_literal():
    assert format_activities(listar_actividades()) == EXPECTED


def test_python_m_womens_day_prints_expected_output():
    proc = subprocess.run(
        [sys.executable, "-m", "womens_day"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert proc.stdout == EXPECTED
