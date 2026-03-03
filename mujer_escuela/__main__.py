from __future__ import annotations

from .activities import load_activities


def main() -> None:
    activities = load_activities()

    print("Actividades para conmemorar el Día de la Mujer")
    for activity in activities:
        print(
            f"- {activity.title}: {activity.description} ({activity.duration_minutes} min, {activity.audience})"
        )


if __name__ == "__main__":
    main()
