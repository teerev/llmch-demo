from actividades.catalog import get_activities


def test_get_activities_schema():
    activities = get_activities()
    assert len(activities) >= 3
    for activity in activities:
        assert set(activity.keys()) == {"id", "title", "description"}
        assert all(isinstance(activity[key], str) for key in ["id", "title", "description"])
