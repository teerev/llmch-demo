import sys
import subprocess

from mujer_escuela.activities import Activity, load_activities


def test_load_activities_returns_expected_objects() -> None:
    activities = load_activities()

    assert isinstance(activities, list)
    assert len(activities) == 4
    assert all(isinstance(a, Activity) for a in activities)
    assert activities[0].title == "Mural de Mujeres Inspiradoras"


def test_cli_output_includes_header_and_activity_title() -> None:
    output = subprocess.check_output(
        [sys.executable, "-m", "mujer_escuela"],
        text=True,
    )

    lines = [line.rstrip("\n") for line in output.splitlines() if line.strip()]
    assert lines, "Expected CLI to print at least one line"

    assert lines[0] == "Actividades para conmemorar el Día de la Mujer"

    # Ensure at least one known activity title is present in the output.
    assert "Mural de Mujeres Inspiradoras" in output
