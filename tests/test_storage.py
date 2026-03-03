from lights_app.models import LightState
from lights_app.storage import load_state, save_state


def test_load_state_defaults_off_when_missing(tmp_path):
    path = tmp_path / "missing.json"
    state = load_state(str(path))
    assert state == LightState(on=False)


def test_save_and_load_roundtrip(tmp_path):
    path = tmp_path / "state.json"
    original = LightState(on=True)
    save_state(str(path), original)
    loaded = load_state(str(path))
    assert loaded == original
